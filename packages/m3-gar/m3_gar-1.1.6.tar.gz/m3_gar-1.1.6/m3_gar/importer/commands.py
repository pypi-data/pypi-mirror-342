import asyncio
import os
import queue
from concurrent.futures import (
    ThreadPoolExecutor,
)
from contextlib import (
    asynccontextmanager,
)
from datetime import (
    timedelta,
)
from operator import (
    attrgetter,
)
from typing import (
    TYPE_CHECKING,
    Optional,
)

import asyncpg
import uvloop
from asgiref.sync import (
    async_to_sync,
)
from django.core.exceptions import (
    ValidationError,
)
from django.core.validators import (
    URLValidator,
)
from django.db import (
    models,
    transaction,
)
from django.utils import (
    timezone,
)

from m3_gar import (
    config,
)
from m3_gar.compat import (
    nullcontext,
)
from m3_gar.consts import (
    VERSION_WITHOUT_URL_TIMEOUT_HOURS,
)
from m3_gar.enums import (
    VersionUpdateStatus,
)
from m3_gar.importer import (
    db_wrapper,
)
from m3_gar.importer.consts import (
    DEFAULT_BULK_LIMIT,
)
from m3_gar.importer.exceptions import (
    DatabaseNotEmptyError,
    ImporterError,
    VersionDoesNotHaveUrl,
)
from m3_gar.importer.loader import (
    TableUpdater,
)
from m3_gar.importer.signals import (
    post_import,
    post_update,
    pre_import,
    pre_update,
)
from m3_gar.importer.source import *
from m3_gar.importer.source.exceptions import (
    TableListLoadingError,
)
from m3_gar.importer.version import (
    check_version_is_processed,
    update_version_status,
)
from m3_gar.models import (
    Version,
)
from m3_gar.util import (
    get_table_names_from_models,
)


if TYPE_CHECKING:
    from m3_gar.importer.source.tablelist import (
        TableList,
    )


def get_tablelist(
    path: str,
    version: Optional[Version] = None,
    tempdir: Optional[str] = None,
) -> 'TableList':
    """Возвращает объект одной из реализаций TableList в зависимости от параметров."""
    if os.path.isfile(path):
        # Путь до файла
        tablelist = LocalArchiveTableList(src=path, version=version, tempdir=tempdir)

    elif os.path.isdir(path):
        # Путь до директории
        tablelist = DirectoryTableList(src=path, version=version, tempdir=tempdir)

    else:
        # Если не файл и не директория, то полагаем, что передан URL
        try:
            URLValidator()(path)
        except ValidationError:
            tablelist = None
        else:
            tablelist = RemoteArchiveTableList(src=path, version=version, tempdir=tempdir)

    if not tablelist:
        raise TableListLoadingError(f'Путь `{path}` не является валидным источником для обновления')

    return tablelist


def get_table_names(tables):
    return tables if tables else get_table_names_from_models()


def load_complete_data(**kwargs):
    no_transaction = kwargs.get('no_transaction', False)

    if no_transaction:
        atomic = nullcontext()
    else:
        atomic = transaction.atomic(using=config.DATABASE_ALIAS)

    with atomic:
        _load_complete_data(**kwargs)


def _load_complete_data(
    *,
    path=None,
    truncate=None,
    no_transaction=False,
    limit=DEFAULT_BULK_LIMIT,
    tables=None,
    tempdir=None,
):
    """
    Загрузка полного архива БД ГАР

    Args:
        path: путь на диске или URL до загруженного архива или директории с
            распакованным архивом. Если передан None, используется известный
            URL до новейшей версии архива.
        truncate: очищать ли уже существующие в БД данные.
            При truncate=None и наличии данных в БД, выбрасывается
            исключение DatabaseNotEmptyError.
            При truncate=True, данные в БД будут предварительно очищены.
            При truncate=False, наличие существующих данных в БД игнорируется.
        no_transaction: отключение заворачивания всего процесса загрузки в транзакцию
        limit: количество записей для пакетного сохранения.
        tables: список импортируемых таблиц. Если передан None, импортируются
            все данные
        tempdir: путь до временной директории для загрузки и распаковки архивов

    """

    tablelist = get_tablelist(
        path=path,
        tempdir=tempdir,
    )

    pre_import.send(
        sender=object.__class__,
        version=tablelist.version,
    )

    table_names = get_table_names(tables)
    table_names = [
        # Пропускаем таблицы, которых нет в архиве
        tbl for tbl in table_names
        if tbl in tablelist.tables
    ]

    if truncate is True:
        Version.objects.update(status=VersionUpdateStatus.NEW)

    if truncate is not False and Version.objects.filter(processed=True).exists():
        raise DatabaseNotEmptyError()

    @async_to_sync
    async def do_the_async_load():

        @asynccontextmanager
        async def make_conn():
            if no_transaction:
                # Если работаем без транзакции, можно делать запросы прямо к
                # пулу соединений, Lock для работы с ним не нужен
                conn = await db_wrapper.get_pool(config.DATABASE_ALIAS)
                conn_lock = nullcontext()

                async with conn:
                    yield conn, conn_lock

            else:
                # Если работаем в транзакции, обязательно захватываем
                # соединение и выдаём Lock на работу с ним
                conn = await db_wrapper.get_connection(config.DATABASE_ALIAS)
                conn_lock = asyncio.Lock()

                async with conn:
                    async with conn.transaction():
                        yield conn, conn_lock

        async with make_conn() as (conn, conn_lock):

            for tbl in table_names:
                table = tablelist.tables[tbl][0]

                if truncate is True:
                    await db_wrapper.truncate_table(conn, table.model)

            read_pool = ThreadPoolExecutor()
            read_queue = queue.Queue(maxsize=limit)
            objects_lists = {}
            objects_counters = {}
            processing_tables = {}
            create_tasks = []
            create_failure: Optional[asyncio.Task] = None

            for tbl in table_names:
                for table in tablelist.tables[tbl]:
                    objects_lists.setdefault(tbl, [])
                    objects_counters.setdefault(tbl, 0)
                    processing_tables.setdefault(tbl, set()).add(table.filename)

                    read_pool.submit(
                        _load_rows_into_queue,
                        tablelist=tablelist,
                        table=table,
                        results=read_queue,
                    )

            async def create(objects):
                nonlocal create_failure

                try:
                    return await _create(objects)

                except Exception:
                    create_failure = asyncio.current_task()
                    raise

                finally:
                    del objects


            async def _create(objects):
                if objects:
                    model = objects[0]._meta.model

                    attnames_columns = [
                        field.get_attname_column()
                        for field in model._meta.concrete_fields
                    ]
                    attnames = [attname for attname, column in attnames_columns]
                    columns = [column for attname, column in attnames_columns]

                    model_attrgetter = attrgetter(*attnames)

                    try:
                        async with conn_lock:
                            await conn.copy_records_to_table(
                                table_name=model._meta.db_table,
                                columns=columns,
                                records=(
                                    model_attrgetter(obj) for obj in objects
                                ),
                            )

                    except asyncpg.exceptions.UniqueViolationError as e:
                        model, field, value = db_wrapper.get_unique_violation_details(e)
                        attname = field.get_attname()
                        new_objects = [
                            object for object in objects
                            if getattr(object, attname) != value
                        ]

                        if len(new_objects) == len(objects):
                            raise

                        print(
                            f'Found duplicate {model.__name__} record {attname}={value}. '
                            f'Retrying skipping this record.'
                        )

                        create_tasks.append(asyncio.create_task(
                            create(new_objects)
                        ))

            while True:
                await asyncio.sleep(0)

                if create_failure:
                    await create_failure

                try:
                    row, table = read_queue.get(block=False)
                except queue.Empty:
                    continue

                if isinstance(row, models.Model):
                    objects_lists[table.name].append(row)
                    objects_counters[table.name] += 1
                    if objects_counters[table.name] % limit == 0:
                        print(f'T: {table.name}\tL: {objects_counters[table.name]}')

                        create_tasks.append(asyncio.create_task(
                            create(objects_lists[table.name])
                        ))
                        objects_lists[table.name] = []

                elif row is StopIteration:
                    processing_tables[table.name].remove(table.filename)
                    print(f'F: {table.filename}\tDONE')

                    if not processing_tables[table.name]:
                        print(f'T: {table.name}\tL: {objects_counters[table.name]}')
                        print(f'T: {table.name}\tDONE')

                        create_tasks.append(asyncio.create_task(
                            create(objects_lists[table.name])
                        ))
                        del processing_tables[table.name]

                    if not processing_tables:
                        print(f'ALL DONE')
                        break

                elif isinstance(row, Exception):
                    raise row

                else:
                    raise RuntimeError

            print('Awaiting pending database write tasks')
            for i, t in enumerate(create_tasks, start=1):
                if not t.done():
                    await t
                    print(f'{i} out of {len(create_tasks)} tasks done')

    uvloop.install()
    do_the_async_load()

    # только если path был равен None - мы имеем право зарегистрировать все версии как обработанные, потому что в этом
    # случае автоматически разворачивается дамп с последней версии. иначе мы этого точно знать не можем, но попробуем
    # определить версию из url (если он был передан)
    if path:
        error_msg = (
            'Unknown uploaded version. Please set attribute status=VersionUpdateStatus.FINISHED to all instances of '
            'Version model that less or equal to uploaded version yourself, or next update will be more time consuming'
        )
        try:
            URLValidator()(path)
        except ValidationError:
            print(error_msg)
        else:
            try:
                url_ver = int(path.split('/')[-2].replace('.', ''))

                Version.objects.filter(
                    ver__lte=url_ver,
                ).exclude(
                    status=VersionUpdateStatus.SKIPPED,
                ).update(
                    status=VersionUpdateStatus.FINISHED,
                )
            except (IndexError, ValueError):
                print(error_msg)

    else:
        Version.objects.exclude(
            status=VersionUpdateStatus.SKIPPED,
        ).update(
            status=VersionUpdateStatus.FINISHED,
        )

    post_import.send(
        sender=object.__class__,
        version=tablelist.version,
    )


def _load_rows_into_queue(tablelist, table, results):
    def put_result(row):
        results.put((row, table))

    try:
        for row in table.rows(tablelist=tablelist):
            put_result(row)
    except Exception as e:
        put_result(e)

    put_result(StopIteration)


@transaction.atomic(using=config.DATABASE_ALIAS)
def update_data(
    version: Version,
    limit: int = 1000,
    tables: Optional[tuple[str, ...]] = None,
    tempdir: Optional[str] = None,
) -> None:
    """
    Загрузка дельта-архива БД ГАР.

    Args:
        version: объект версии архива
        limit: количество записей для пакетного сохранения. Не влияет на
            обновляемые объекты.
        tables: список импортируемых таблиц. Если передан None, импортируются
            все данные
        tempdir: путь до временной директории для загрузки и распаковки архивов
    """
    check_version_is_processed(version)

    tablelist = get_tablelist(path=version.delta_xml_url, version=version, tempdir=tempdir)

    for table_name in get_table_names(tables):
        # Пропускаем таблицы, которых нет в архиве
        if table_name not in tablelist.tables:
            continue

        for table in tablelist.tables[table_name]:
            loader = TableUpdater(limit=limit)
            loader.load(tablelist=tablelist, table=table)

    update_version_status(version, VersionUpdateStatus.FINISHED)

    # удаляем временный файл с архивом обновления
    temp_file_name = tablelist.wrapper.source.filename
    if os.path.exists(temp_file_name):
        os.remove(temp_file_name)


def auto_update_data(
    limit: int = 1000,
    tables: Optional[tuple[str, ...]] = None,
    tempdir: Optional[str] = None,
    skip_versions: Optional[list[int]] = None,
):
    """
    Последовательное обновление БД ГАР на основе текущей версии БД и известных
    новых версий с сайта ФИАС.

    Args:
        limit: количество записей для пакетного сохранения. Не влияет на
            обновляемые объекты.
        tables: список импортируемых таблиц. Если передан None, импортируются
            все данные
        tempdir: путь до временной директории для загрузки и распаковки архивов
        skip_versions: номера версий обновлений, которые не будут выполняться и будут
            отмечены как пропущенные
    """
    last_processed_version = Version.objects.last_processed()

    if last_processed_version is None:
        raise TableListLoadingError('Not available. Please import the data before updating')

    skip_versions = set(skip_versions) if skip_versions is not None else set()

    versions = Version.objects.filter(ver__gt=last_processed_version.ver).order_by('ver')

    for version in versions:
        pre_update.send(sender=object.__class__, before=last_processed_version, after=version)

        if version.ver in skip_versions:
            update_version_status(version, VersionUpdateStatus.SKIPPED)

        elif version.delta_xml_url:
            try:
                update_data(
                    version=version,
                    limit=limit,
                    tables=tables,
                    tempdir=tempdir,
                )
            except ImporterError:
                update_version_status(version, VersionUpdateStatus.ERROR)

                raise
        else:
            # в версии нет ссылки на дельту
            if timezone.now().date() < (version.dumpdate + timedelta(hours=VERSION_WITHOUT_URL_TIMEOUT_HOURS)):
                # Время ожидания, когда ссылка для версии на сайте могла появиться ещё не прошло,
                # поэтому вызываем ошибку обновления
                update_version_status(version, VersionUpdateStatus.ERROR)

                raise VersionDoesNotHaveUrl(f'Версия {version} не имеет ссылки на файл с дельтой!')
            else:
                # Время ожидания, когда ссылка для версии на сайте могла появиться уже прошло,
                # поэтому больше не ждём и пропускаем версию
                update_version_status(version, VersionUpdateStatus.SKIPPED)

        post_update.send(sender=object.__class__, before=last_processed_version, after=version)

        last_processed_version = version


def get_reserve_delta_url(version):
    """
    Возвращает резервную ссылку для скачивания дельты
    """
    version_str = version.dumpdate.strftime('%Y.%m.%d')

    return f'https://file.nalog.ru/Downloads/{version_str}/gar_delta_xml.zip'

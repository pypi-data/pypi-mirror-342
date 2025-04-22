from typing import (
    TYPE_CHECKING,
)

from m3_gar.enums import (
    VersionUpdateStatus,
)
from m3_gar.importer.client import (
    client,
)
from m3_gar.importer.exceptions import (
    VersionAlreadyProcessedError,
)
from m3_gar.importer.signals import (
    post_fetch_version,
    pre_fetch_version,
)
from m3_gar.models import (
    Version,
)


if TYPE_CHECKING:
    from m3_gar.importer.client import (
        DownloadFileInfo,
    )


def get_or_create_version(file_info: 'DownloadFileInfo') -> tuple[Version, bool]:
    """Создаёт и/или возвращает запись Version по информации об обновлении."""
    version, created = Version.objects.get_or_create(
        ver=file_info.version_id,
        defaults={
            'dumpdate': file_info.date,
            'complete_xml_url': file_info.gar_xml_full_url,
            'delta_xml_url': file_info.gar_xml_delta_url,
        }
    )

    return version, created


def check_version_is_processed(version: Version) -> None:
    """Проверка версии на признак обработки.

    Raises:
        VersionAlreadyProcessedError: если версия уже была обработана ранее
    """
    if version.status in VersionUpdateStatus.get_processed_statuses():
        raise VersionAlreadyProcessedError(f'Версия {version} уже была обработана ранее!')


def update_version_status(version: Version, status: VersionUpdateStatus) -> None:
    """Изменение статуса у версии обновления."""
    check_version_is_processed(version)

    version.status = status
    version.save()


def fetch_version_info(update_all: bool = False) -> None:
    """Получение информации о версии файлов обновления.

    Получает информацию о файлах с обновлениями с сайта ФИАС и создаёт по ним
    соответствующие записи модели Version.

    Args:
        update_all: Обновляет информацию по всем существующим записям Version
    """
    pre_fetch_version.send(object.__class__)

    all_download_file_info = client.get_all_download_file_info()

    for file_info in all_download_file_info:
        version, created = get_or_create_version(file_info)

        if update_all and not created:
            version.complete_xml_url = file_info.gar_xml_full_url
            version.delta_xml_url = file_info.gar_xml_delta_url

            if version.dumpdate < file_info.date:
                version.dumpdate = file_info.date

            version.save()

    post_fetch_version.send(object.__class__)

class ImporterError(Exception):
    pass


class DatabaseNotEmptyError(ImporterError):
    pass


class DownloadFileInfoError(ImporterError):
    """Ошибка связанная с обработкой информации о файлах обновлений с сайта ФИАС."""
    pass


class UpdateVersionError(ImporterError):
    """Общая ошибка связанная с обработкой записей обновлений."""
    pass


class VersionAlreadyProcessedError(UpdateVersionError):
    """Ошибка при попытке обработать версию, которая уже была обработана ранее."""
    pass


class VersionDoesNotHaveUrl(UpdateVersionError):
    """У версии обновления отсутствуют ссылки на файл с данными."""
    pass

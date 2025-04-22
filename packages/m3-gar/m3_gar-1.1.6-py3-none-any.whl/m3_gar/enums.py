from django.db.models import (
    TextChoices,
)


class VersionUpdateStatus(TextChoices):
    """Статус обработки версии обновления."""

    NEW = 'new', 'Новое'
    SKIPPED = 'skipped', 'Пропущено'
    ERROR = 'error', 'Ошибка'
    FINISHED = 'finished', 'Завершено'

    @classmethod
    def get_processed_statuses(cls) -> set['VersionUpdateStatus']:
        """Статусы обновлений, которые считаются обработанными."""
        return {cls.FINISHED, cls.SKIPPED}

from django.db import (
    models,
)
from django.db.models import (
    BooleanField,
    Case,
    Value,
    When,
)

from m3_gar.enums import (
    VersionUpdateStatus,
)


__all__ = ['Version']


class VersionManager(models.Manager):

    def get_queryset(self):
        query = super().get_queryset()

        query = query.annotate(
            processed=Case(
                When(
                    status__in=VersionUpdateStatus.get_processed_statuses(),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            )
        )

        return query

    def nearest_by_date(self, date):
        return self.get_queryset().filter(dumpdate__lte=date).latest('dumpdate')

    def last_processed(self):
        """Возвращает самую последнюю обработанную версию."""
        return self.get_queryset().filter(
            processed=True,
        ).last()


class Version(models.Model):

    objects = VersionManager()

    ver = models.IntegerField(primary_key=True)
    date = models.DateField(db_index=True, blank=True, null=True)
    dumpdate = models.DateField(db_index=True)

    complete_xml_url = models.CharField(max_length=255)
    delta_xml_url = models.CharField(max_length=255, blank=True, null=True)

    status = models.CharField(
        'Статус обновления',
        max_length=20,
        choices=VersionUpdateStatus.choices,
        default=VersionUpdateStatus.NEW,
    )

    def __str__(self):
        return f'{self.ver} от {self.dumpdate}'

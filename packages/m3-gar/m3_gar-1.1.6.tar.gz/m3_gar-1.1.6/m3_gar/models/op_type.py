from django.db import (
    models,
)
from m3_gar.base_models import (
    OperationTypes as BaseOperationTypes,
)


__all__ = ['OperationTypes']


class OperationTypes(BaseOperationTypes):
    """
    Сведения по статусу действия
    """

    name = models.CharField(max_length=300, verbose_name='Наименование')
    shortname = models.CharField(max_length=300, verbose_name='Краткое наименование', blank=True, null=True)

    class Meta:
        verbose_name = 'Статус действия'
        verbose_name_plural = 'Статусы действия'

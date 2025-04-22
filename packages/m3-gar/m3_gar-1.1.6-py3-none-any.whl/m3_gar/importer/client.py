import datetime
from dataclasses import (
    dataclass,
)

import requests

from m3_gar.importer.exceptions import (
    DownloadFileInfoError,
)


@dataclass
class DownloadFileInfo:
    """Информация о файле с изменениями с сайта ФИАС."""

    version_id: int
    date: datetime.date
    gar_xml_full_url: str = ''
    gar_xml_delta_url: str = ''

    @classmethod
    def from_raw_info(cls, raw_info: dict) -> 'DownloadFileInfo':
        """Возвращает инстанс по информации скаченной с сайта ФИАС."""
        try:
            file_info = cls(
                version_id=raw_info['VersionId'],
                date=datetime.datetime.strptime(raw_info['Date'], '%d.%m.%Y').date(),
                gar_xml_full_url=raw_info['GarXMLFullURL'] or '',
                gar_xml_delta_url=raw_info['GarXMLDeltaURL'] or '',
            )
        except (KeyError, ValueError) as err:
            raise DownloadFileInfoError(
                f'Ошибка формата информации об обновлении с сайта ФИАС: {err}'
            )

        return file_info


class FIASClient:
    """Клиент к серверу ФИАС"""
    fias_source = 'https://fias.nalog.ru/WebServices/Public/'

    def get_all_download_file_info(self) -> list[DownloadFileInfo]:
        """Скачивает и возвращает перечень информации о файлах с обновлениями."""
        all_raw_info = requests.get(
            f'{self.fias_source}GetAllDownloadFileInfo',
        ).json()

        all_download_file_info = [
            DownloadFileInfo.from_raw_info(raw_info)
            for raw_info in all_raw_info
        ]

        return all_download_file_info


client = FIASClient()

import petl as etl
from django.conf import settings
from petl.util.base import Table
from typing import Any, Tuple, Union
from uuid import uuid4

from .data_fetcher import DataFetcher
from .etl_utils import ETLUtils


class ETLController:
    @classmethod
    def create_empty(cls) -> str:
        filename = cls._generate_filename()
        cls._save(tbl=etl.fromdicts({}), source=filename, is_to_override=True)
        return filename

    @classmethod
    def fetch(cls, filename: str) -> None:
        planets_generator = DataFetcher(url=DataFetcher.PLANETS_URL).async_fetch(limit=10)
        planets = ETLUtils.prepare_planets(planets_generator)
        is_to_override = True
        for people_gen in DataFetcher(url=DataFetcher.PEOPLE_URL).async_fetch(limit=10):
            people = ETLUtils.prepare_people(people_gen, planets)
            cls._save(tbl=people, source=filename, is_to_override=is_to_override)
            is_to_override = False

    @classmethod
    def count(cls, source: str, by: Union[Tuple[Any], Any]) -> Table:
        people_table = cls.load(source)
        return ETLUtils.count(tbl=people_table, by=by)

    @staticmethod
    def load(source: str) -> Table:
        return etl.fromcsv(source=settings.STORAGE_DIR.joinpath(source))

    @staticmethod
    def _save(tbl: Table, source: str, is_to_override: bool) -> None:
        source = settings.STORAGE_DIR.joinpath(source)
        if is_to_override:
            etl.tocsv(table=tbl, source=source)
        else:
            etl.appendcsv(table=tbl, source=source)

    @staticmethod
    def _generate_filename() -> str:
        return f'{uuid4()}.csv'

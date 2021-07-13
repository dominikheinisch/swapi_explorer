import petl as etl
from datetime import datetime
from petl.util.base import Table
from typing import Generator, List, Tuple, Union


class ETLUtils:
    PEOPLE_FIELDS = [
        'name', 'height', 'mass', 'hair_color', 'skin_color', 'eye_color', 'birth_year', 'gender', 'homeworld',
        'edited'
    ]
    PLANETS_FIELDS = ['name', 'url']

    @staticmethod
    # def combine(gen: Generator[dict, None, None]) -> Table:
    def combine(gen: Generator[dict, None, None]) -> Table:
        return etl.cat(*(etl.fromdicts(elem) for elem in gen))

    @staticmethod
    def filter(tbl: Table, fields: List[str]) -> Table:
        return tbl.cut(*fields)

    @staticmethod
    def formatter(elem: str) -> str:
        return datetime.strptime(elem, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d')

    @staticmethod
    def fix_date(tbl: Table) -> Table:
        tbl = etl.rename(tbl, 'edited', 'date')
        return etl.convert(tbl, 'date', lambda elem: ETLUtils.formatter(elem))

    @staticmethod
    def fix_homeworld(people: Table, planets: Table) -> Table:
        people = etl.join(people, planets, lkey='homeworld', rkey='url', rprefix='_')
        people = etl.cutout(people, 'homeworld')
        people = etl.movefield(people, field='_homeworld', index=8)
        people = etl.rename(people, '_homeworld', 'homeworld')
        return people

    @staticmethod
    def prepare_planets(planets_generator: Generator[Generator[dict, None, None], None, None]) -> Table:
        all_planets = etl.fromdicts({})
        for planets in planets_generator:
            planets_table = ETLUtils.combine(planets)
            planets_table = ETLUtils.filter(planets_table, fields=ETLUtils.PLANETS_FIELDS)
            all_planets = etl.cat(all_planets, planets_table)
        all_planets = etl.rename(all_planets, 'name', 'homeworld')
        return all_planets

    @staticmethod
    def prepare_people(people_generator: Generator[dict, None, None], planets: Table) -> Table:
        people_table = ETLUtils.combine(people_generator)
        people_table = ETLUtils.filter(people_table, fields=ETLUtils.PEOPLE_FIELDS)
        people_table = ETLUtils.fix_date(people_table)
        people_table = ETLUtils.fix_homeworld(people=people_table, planets=planets)
        return people_table

    @staticmethod
    def count(tbl: Table, by: Union[str, Tuple[str]]) -> Table:
        tbl = etl.aggregate(table=tbl, key=by, aggregation=len)
        return etl.rename(tbl, 'value', 'Count')

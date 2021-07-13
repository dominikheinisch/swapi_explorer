import petl as etl
import pytest
from django.test import TestCase

from explorer_app.logic.etl_utils import ETLUtils


@pytest.mark.usefixtures('people')
@pytest.mark.usefixtures('people_table')
@pytest.mark.usefixtures('planets')
class ETLUtilsTest(TestCase):
    def test_combine(self):
        tbl = ETLUtils.combine(gen=self.people)
        han = etl.select(tbl, "{name} == 'Han Solo'")
        hen = etl.cut(han, ('name', 'height', 'birth_year', 'homeworld'))[1]
        assert hen == ('Han Solo', '180', '29BBY', 'https://swapi.dev/api/planets/22/')

    def test_formatter(self):
        assert '2000-01-01' == ETLUtils.formatter('2000-01-01T01:01:01.000Z')

    def test_fix_date(self):
        tbl = ETLUtils.fix_date(tbl=self.people_table)
        assert etl.dicts(tbl)[0].get('date') == '2014-12-20'
        assert etl.dicts(tbl)[1].get('date') == '2014-12-20'

    def test_count_one_field(self):
        tbl = ETLUtils.count(tbl=self.people_table, by='gender')
        assert etl.dicts(tbl)[0].get('gender') == 'male'
        assert etl.dicts(tbl)[0].get('Count') == 2

    def test_count_two_field(self):
        tbl = ETLUtils.count(tbl=self.people_table, by=('gender', 'name'))
        assert etl.dicts(tbl)[0].get('gender') == 'male'
        assert etl.dicts(tbl)[0].get('name') == 'Darth Vader'
        assert etl.dicts(tbl)[0].get('Count') == 1
        assert etl.dicts(tbl)[1].get('gender') == 'male'
        assert etl.dicts(tbl)[1].get('name') == 'Han Solo'
        assert etl.dicts(tbl)[1].get('Count') == 1

    def test_prepare_planets(self):
        tbl = ETLUtils.prepare_planets(planets_generator=(self.planets,))
        assert etl.dicts(tbl)[0].get('homeworld') == 'Tatooine'
        assert etl.dicts(tbl)[0].get('url') == 'https://swapi.dev/api/planets/1/'
        assert etl.dicts(tbl)[1].get('homeworld') == 'Corellia'
        assert etl.dicts(tbl)[1].get('url') == 'https://swapi.dev/api/planets/22/'

    def test_fix_homeworld(self):
        planets_table = ETLUtils.prepare_planets(planets_generator=(self.planets,))
        tbl = ETLUtils.fix_homeworld(people=self.people_table, planets=planets_table)
        assert etl.dicts(tbl)[0].get('name') == 'Darth Vader'
        assert etl.dicts(tbl)[0].get('homeworld') == 'Tatooine'
        assert etl.dicts(tbl)[1].get('name') == 'Han Solo'
        assert etl.dicts(tbl)[1].get('homeworld') == 'Corellia'

    def test_prepare_people(self):
        planets_table = ETLUtils.prepare_planets(planets_generator=(self.planets,))
        tbl = ETLUtils.prepare_people(people_generator=self.people, planets=planets_table)
        assert etl.dicts(tbl)[0].get('name') == 'Darth Vader'
        assert etl.dicts(tbl)[0].get('homeworld') == 'Tatooine'
        assert etl.dicts(tbl)[0].get('date') == '2014-12-20'

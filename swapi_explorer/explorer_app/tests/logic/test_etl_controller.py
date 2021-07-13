import petl as etl
import pytest
from django.conf import settings
from django.test import TestCase
from unittest.mock import patch, MagicMock

from explorer_app.logic.etl_controller import ETLController
from explorer_app.tests.utils import WrappedResp


@pytest.mark.usefixtures('planets')
@pytest.mark.usefixtures('people')
class ETLControllerTest(TestCase):
    @patch.object(ETLController, 'load')
    def test_count(self, load_mock: MagicMock):
        source = 'explorer_app/tests/data/people.csv'
        load_mock.return_value = etl.fromcsv(source)
        tbl = ETLController.count(source=source, by='gender')
        assert etl.dicts(tbl)[0].get('gender') == 'male'
        assert etl.dicts(tbl)[0].get('Count') == 2

    @patch('explorer_app.logic.etl_controller.etl.tocsv')
    @patch('explorer_app.logic.etl_controller.uuid4')
    def test_create_empty(self, uuid4_mock: MagicMock, tocsv_mock: MagicMock):
        uuid4_mock.return_value = 'potato'
        filename = ETLController.create_empty()
        assert filename == 'potato.csv'
        assert tocsv_mock.call_args.kwargs['source'] == settings.STORAGE_DIR.joinpath('potato.csv')

    @patch('explorer_app.logic.data_fetcher.grequests')
    @patch('explorer_app.logic.etl_controller.etl.tocsv')
    @patch('explorer_app.logic.etl_controller.etl.appendcsv')
    def test_fetch(self, appendcsv_mock, tocsv_mock, grequests_mock):
        grequests_mock.map.side_effect = [
            [WrappedResp((self.planets[0][0], self.planets[0][1]))],
            [WrappedResp((self.people[0][0], self.people[0][1]))],
        ]
        ETLController.fetch('foobar.csv')
        assert tocsv_mock.call_args.kwargs['source'] == settings.STORAGE_DIR.joinpath('foobar.csv')
        table_to_save = tocsv_mock.call_args.kwargs['table']
        header = (
            'name', 'height', 'mass', 'hair_color', 'skin_color', 'eye_color',
            'birth_year', 'gender', 'homeworld', 'date'
        )
        assert table_to_save[0] == header
        vader = ('Darth Vader', '202', '136', 'none', 'white', 'yellow', '41.9BBY', 'male', 'Tatooine', '2014-12-20')
        assert table_to_save[1] == vader
        han = ('Han Solo', '180', '80', 'brown', 'fair', 'brown', '29BBY', 'male', 'Corellia', '2014-12-20')
        assert table_to_save[2] == han

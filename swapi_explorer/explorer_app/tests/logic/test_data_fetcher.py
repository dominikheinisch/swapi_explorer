from unittest.mock import patch, MagicMock
from django.test import TestCase

from explorer_app.logic.data_fetcher import DataFetcher
from explorer_app.logic.etl_utils import ETLUtils


class Resp:
    def __init__(self, value):
        self._value = value

    def json(self):
        return self._value


json_resp_1 = {'results': 'foo', 'next': 'dummy'}
json_resp_2 = {'results': 'bar', 'next': 'dummy'}
json_resp_3 = {'results': 'baz'}


class DataFetcherTests(TestCase):
    def test_async_fetch_from_api_luke(self):
        fetch_gen = DataFetcher(DataFetcher.PEOPLE_URL).async_fetch(limit=1)
        person = next(next(fetch_gen))[0]
        assert 'Luke Skywalker' == person['name']
        assert set(ETLUtils.PEOPLE_FIELDS).issubset(person.keys())

    def test_async_fetch_from_api_tatooine(self):
        fetch_gen = DataFetcher(DataFetcher.PLANETS_URL).async_fetch(limit=1)
        planet = next(next(fetch_gen))[0]
        assert 'Tatooine' == planet['name']
        assert set(ETLUtils.PLANETS_FIELDS).issubset(planet.keys())

    @patch('explorer_app.logic.data_fetcher.grequests')
    def test_async_fetch_ok(self, grequests_mock: MagicMock):
        grequests_mock.map.return_value = [Resp(json_resp) for json_resp in (json_resp_1, json_resp_2, json_resp_3)]
        fetch_gen = DataFetcher(DataFetcher.PLANETS_URL).async_fetch()
        assert ['foo', 'bar', 'baz'] == [elem for batch in fetch_gen for elem in batch]

    @patch('explorer_app.logic.data_fetcher.grequests')
    def test_async_fetch_empty_resp(self, grequests_mock: MagicMock):
        grequests_mock.map.return_value = [Resp({})]
        fetch_gen = DataFetcher(DataFetcher.PLANETS_URL).async_fetch()
        assert [] == [elem for batch in fetch_gen for elem in batch]

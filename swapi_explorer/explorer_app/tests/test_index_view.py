import pytest
from django.urls import reverse
from django.test import TestCase
from unittest.mock import patch, MagicMock

from explorer_app.logic.etl_controller import ETLController
from explorer_app.logic.etl_utils import ETLUtils
from explorer_app.tests.utils import WrappedResp


@pytest.mark.usefixtures('planets')
@pytest.mark.usefixtures('people')
class IndexViewTests(TestCase):
    def test_index_get(self):
        response = self.client.get(reverse('explorer_app:index'))
        assert response.status_code == 200

    @patch('explorer_app.logic.data_fetcher.grequests')
    @patch.object(ETLController, '_save')
    def test_index_post(self, save_mock: MagicMock, grequests_mock: MagicMock):
        grequests_mock.map.side_effect = [
            [WrappedResp((self.planets[0][0], self.planets[0][1]))],
            [WrappedResp((self.people[0][0], self.people[0][1]))],
        ]
        response = self.client.post(reverse('explorer_app:index'), {'fetch': ''})
        first_call, second_call = save_mock.call_args_list
        assert first_call.kwargs['source'] == second_call.kwargs['source']
        table_to_save = second_call.kwargs['tbl']
        assert list(table_to_save[0][:-1]) == ETLUtils.PEOPLE_FIELDS[:-1]
        assert table_to_save[1][0] == 'Darth Vader'
        assert response.status_code == 302

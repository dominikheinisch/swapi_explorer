import petl as etl
import pytest
from datetime import datetime
from django.urls import reverse
from django.test import TestCase
from unittest.mock import patch, MagicMock

from explorer_app.logic.etl_controller import ETLController
from explorer_app.logic.etl_utils import ETLUtils
from explorer_app.models import File


@pytest.mark.usefixtures('people_table')
class FileViewTests(TestCase):
    def setUp(self):
        File.objects.create(name='foo.csv', creation_date=datetime.now())
        File.objects.create(name='bar.csv', creation_date=datetime.now())

    def test_file_get_no_exist(self):
        with pytest.raises(OSError):
            self.client.get(reverse('explorer_app:file', args=('baz.csv',)))

    @patch.object(ETLController, 'load')
    def test_file_get_ok(self, load_mock: MagicMock):
        load_mock.return_value = etl.fromcsv('explorer_app/tests/data/people.csv')
        response = self.client.get(reverse('explorer_app:file', args=('foo.csv',)))
        assert response.status_code == 200
        assert list(response.context['table_head'][:-1]) == ETLUtils.PEOPLE_FIELDS[:-1]

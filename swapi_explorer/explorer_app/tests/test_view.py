from django.urls import reverse
from django.test import TestCase


class ViewTests(TestCase):
    def test_index_ok(self):
        response = self.client.get(reverse('explorer_app:index'))
        self.assertEqual(response.status_code, 200)

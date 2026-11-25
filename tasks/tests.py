from rest_framework import status
from rest_framework.test import APITestCase

from .models import Task


class TaskApiTests(APITestCase):
    list_url = '/api/tasks/'

    def test_create_and_list_tasks(self):
        response = self.client.post(
            self.list_url,
            {'title': 'First task', 'description': 'Do the work'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'First task')

    def test_invalid_task_returns_bad_request(self):
        response = self.client.post(
            self.list_url,
            {'description': 'Missing title'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

    def test_missing_task_returns_not_found_for_all_detail_methods(self):
        detail_url = self.list_url + '999/'

        for method, data in (
            ('get', None),
            ('put', {'title': 'Updated', 'description': 'Still missing'}),
            ('delete', None),
        ):
            request = getattr(self.client, method)
            response = request(detail_url, data=data, format='json') if data else request(detail_url)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

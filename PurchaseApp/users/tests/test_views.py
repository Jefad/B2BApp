from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from users.models import UserProduct

from django.test import TestCase


class CRUDTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.item_data = {'name': 'Test Item', 'description': 'This is a test item.'}
        self.item = UserProduct.objects.create(**self.item_data)
        self.url = reverse('item-list')

    def test_create_product(self):
        response = self.client.post(self.url, self.item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserProduct.objects.count(), 2)  # Assuming there's already one item created in setUp

    def test_read_product_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.item.name)

    def test_read_product_detail(self):
        detail_url = reverse('item-detail', args=[self.item.id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.item.name)

    def test_update_product(self):
        detail_url = reverse('item-detail', args=[self.item.id])
        updated_data = {'name': 'Updated Item', 'description': 'This is an updated item.'}
        response = self.client.put(detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserProduct.objects.get(id=self.item.id).name, 'Updated Item')

    def test_delete_product(self):
        detail_url = reverse('item-detail', args=[self.item.id])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UserProduct.objects.count(), 0)

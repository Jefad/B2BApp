from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .factories import ProductFactory


class CRUDTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = ProductFactory()
        self.url = reverse('api/myapp')

    def test_create_product(self):
        product_data = {'name': 'Test product', 'description': 'This is a test product.'}
        response = self.client.post(f'{self.url}/create/', product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductFactory.objects.count(), 2)

    def test_read_product_list(self):
        response = self.client.get(f'{self.url}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.product.name)

    def test_read_product_detail(self):
        detail_url = reverse('api/myapp', args=[self.product.id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_update_product(self):
        detail_url = reverse('api/myapp', args=[self.product.id])
        updated_data = {'name': 'Updated product', 'description': 'This is an updated product.'}
        response = self.client.put(detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ProductFactory.objects.get(id=self.product.id).name, 'Updated product')

    def test_delete_product(self):
        detail_url = reverse('api/myapp', args=[self.product.id])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ProductFactory.objects.count(), 0)


if __name__ == "__main__":
    crud_test = CRUDTests()
    crud_test.test_create_product()


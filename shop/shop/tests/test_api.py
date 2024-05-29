from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from shop.models import Specification, Category, Product
from shop.serializers import ProductSerializer


class ProductApiTestCase(APITestCase):
    def setUp(self):
        self.specifications = Specification.objects.create(name='name_spec', value='value_spec')
        self.category = Category.objects.create(name='category_1', slug='category_1')
        self.product_1 = Product.objects.create(slug='product_1',
                                                name='product_1',
                                                price='100.00',
                                                remaining_product=1,
                                                category=self.category)

        self.product_2 = Product.objects.create(slug='product_2',
                                                name='product_2',
                                                price='1090.00',
                                                remaining_product=2,
                                                category=self.category)

        self.product_1.specifications.add(self.specifications)
        self.product_2.specifications.add(self.specifications)

    def test_get(self):
        url = reverse('product-list')
        response = self.client.get(url)
        serializer_data = ProductSerializer([self.product_1, self.product_2], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['result']['results'])


class ProductsByCategoryApiTestCase(APITestCase):
    def setUp(self):
        self.category_1 = Category.objects.create(name='category_1',
                                                  slug='category_1')
        self.category_2 = Category.objects.create(name='category_2',
                                                  slug='category_2',
                                                  parent_category=self.category_1)
        self.category_3 = Category.objects.create(name='category_3',
                                                  slug='category_3',
                                                  parent_category=self.category_2)

        self.specifications = Specification.objects.create(name='name_spec', value='value_spec')
        self.product_1 = Product.objects.create(slug='product_1',
                                                name='product_1',
                                                price='100.00',
                                                remaining_product=1,
                                                category=self.category_1)

        self.product_2 = Product.objects.create(slug='product_2',
                                                name='product_2',
                                                price='1090.00',
                                                remaining_product=2,
                                                category=self.category_1)

        self.product_1.specifications.add(self.specifications)
        self.product_2.specifications.add(self.specifications)

        self.assertEqual(str(self.category_1), self.category_1.name)
        self.assertEqual(str(self.specifications), f"{self.specifications.name}: {self.specifications.value}")

    def test_get(self):
        response = self.client.get('/category/category_1/')
        serializer_data = ProductSerializer([self.product_1, self.product_2], many=True).data
        self.assertEqual(serializer_data, response.data)

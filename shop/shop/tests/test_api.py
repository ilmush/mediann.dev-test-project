from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from shop.models import *
from shop.serializers import *


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

    def test_get(self):
        response = self.client.get('/category/category_1/')
        serializer_data = ProductSerializer([self.product_1, self.product_2], many=True).data

        self.assertEqual(serializer_data, response.data)


class CartViewApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test')
        self.client.force_login(self.user)
        self.customer = Customer.objects.create(user=self.user)
        self.specifications = Specification.objects.create(name='name_spec', value='value_spec')
        self.category = Category.objects.create(name='category_1', slug='category_1')
        self.product_1 = Product.objects.create(slug='product_1',
                                                name='product_1',
                                                price='100.00',
                                                remaining_product=1,
                                                category=self.category)
        self.product_1.specifications.add(self.specifications)

        self.cart = Cart.objects.create(owner=self.customer)
        self.cart_product = CartProduct.objects.create(user=self.customer,
                                                       cart=self.cart,
                                                       product=self.product_1,
                                                       final_price=100.00)
        self.cart.products.add(self.cart_product)

    def test_get(self):
        response = self.client.get('/cart/')
        serializer_data = CartSerializer(self.cart).data

        self.assertEqual(serializer_data, response.data[0])



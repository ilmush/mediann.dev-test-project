from django.test import TestCase
from django.db import models

from shop.models import *
from shop.utils import recalc_cart


class RecalcCartTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test')
        self.client.force_login(self.user)
        self.customer = Customer.objects.create(user=self.user)
        self.specifications = Specification.objects.create(name='name_spec', value='value_spec')
        self.category = Category.objects.create(name='category_1', slug='category_1')
        self.product = Product.objects.create(slug='product_1',
                                              name='product_1',
                                              price='100.00',
                                              remaining_product=1,
                                              category=self.category)
        self.product.specifications.add(self.specifications)

        self.cart = Cart.objects.create(owner=self.customer)
        self.cart_product = CartProduct.objects.create(user=self.customer,
                                                       cart=self.cart,
                                                       product=self.product,
                                                       final_price=100.00)
        self.cart.products.add(self.cart_product)

    def test_recalc_cart(self):
        recalc_cart(self.cart)
        self.assertEqual(self.cart.final_price, 100.00)
        self.assertEqual(self.cart.total_products, 1)

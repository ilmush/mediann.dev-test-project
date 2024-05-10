from rest_framework import status
from rest_framework.test import APITestCase

from cart.models import Cart, CartProduct
from cart.serializers import CartSerializer
from shop.models import User, Customer, Specification, Category, Product


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

        self.assertEqual(str(self.cart), str(self.cart.id))
        self.assertEqual(str(self.cart_product), f"Продукт {self.cart_product.product.name} (для корзины)")

    def test_get(self):
        response = self.client.get('/cart/')
        serializer_data = CartSerializer(self.cart).data

        self.assertEqual(serializer_data, response.data[0])


class AddToCartViewApiTestCase(APITestCase):
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
        response = self.client.get('/add-to-cart/product_1/')
        print(response)

        self.assertEqual(status.HTTP_302_FOUND, response.status_code)

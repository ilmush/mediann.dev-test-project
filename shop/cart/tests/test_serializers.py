from django.test import TestCase

from cart.models import Cart, CartProduct
from cart.serializers import CartProductSerializer
from shop.models import User, Customer, Specification, Category, Product


class CartProductSerializerTestCase(TestCase):
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
        self.cart_product_1 = CartProduct.objects.create(user=self.customer,
                                                         cart=self.cart,
                                                         product=self.product_1,
                                                         final_price=100.00)

    def test_ok(self):
        data = CartProductSerializer(self.cart_product_1).data
        expected_data = {
                'qty': 1,
                'user': str(self.customer),
                'product': 'product_1'
            }
        self.assertEqual(expected_data, data)

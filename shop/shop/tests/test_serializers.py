from django.test import TestCase

from shop.models import Category, Specification, Product, User, Customer, Cart, CartProduct
from shop.serializers import CategorySerializer, SpecificationSerializer, ProductSerializer, CartProductSerializer


class CategorySerializerTestCase(TestCase):
    def setUp(self):
        self.category_1 = Category.objects.create(name='category_1',
                                                  slug='category_1')
        self.category_2 = Category.objects.create(name='category_2',
                                                  slug='category_2',
                                                  parent_category=self.category_1)

    def test_ok(self):
        data = CategorySerializer([self.category_1, self.category_2],
                                  many=True).data
        expected_data = [
            {
                'id': self.category_1.id,
                'name': 'category_1',
                'slug': 'category_1',
                'parent_category': None,
            },
            {
                'id': self.category_2.id,
                'name': 'category_2',
                'slug': 'category_2',
                'parent_category': self.category_1.id,
            },
        ]

        self.assertEqual(expected_data, data)


class SpecificationSerializerTestCase(TestCase):
    def setUp(self):
        self.spec_1 = Specification.objects.create(name='spec_1',
                                                   value='spec_1')
        self.spec_2 = Specification.objects.create(name='spec_2',
                                                   value='spec_2')

    def test_ok(self):
        data = SpecificationSerializer([self.spec_1, self.spec_2],
                                       many=True).data
        expected_data = [
            {
                'id': self.spec_1.id,
                'name': 'spec_1',
                'value': 'spec_1',
            },
            {
                'id': self.spec_2.id,
                'name': 'spec_2',
                'value': 'spec_2',
            },
        ]

        self.assertEqual(expected_data, data)


class ProductSerializerTestCase(TestCase):
    def setUp(self):
        self.specifications = Specification.objects.create(name='name_spec', value='value_spec')
        self.category = Category.objects.create(name='category_1', slug='category_1')
        self.product_1 = Product.objects.create(name='product_1',
                                                slug='product_1',
                                                price='100.00',
                                                discounted_price='99.99',
                                                remaining_product=1,
                                                category=self.category)

        self.product_2 = Product.objects.create(name='product_2',
                                                slug='product_2',
                                                price='1090.00',
                                                remaining_product=2,
                                                category=self.category)

        self.product_1.specifications.add(self.specifications)
        self.product_2.specifications.add(self.specifications)

    def test_ok(self):
        data = ProductSerializer([self.product_1, self.product_2],
                                 many=True).data
        expected_data = [
            {
                'id': self.product_1.id,
                'name': 'product_1',
                'slug': 'product_1',
                'price': '100.00',
                'discounted_price': '99.99',
                'remaining_product': 1,
                'specifications': [{
                    'id': self.specifications.id,
                    'name': 'name_spec',
                    'value': 'value_spec',
                    }],
                'category': self.category.id
            },
            {
                'id': self.product_2.id,
                'name': 'product_2',
                'slug': 'product_2',
                'price': '1090.00',
                'discounted_price': None,
                'remaining_product': 2,
                'specifications': [{
                    'id': self.specifications.id,
                    'name': 'name_spec',
                    'value': 'value_spec',
                }],
                'category': self.category.id
            },
        ]
        self.assertEqual(expected_data, data)


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

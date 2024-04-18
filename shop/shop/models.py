from django.contrib.sites import managers
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,
                            unique=True)
    subcategory = models.ManyToManyField('self',
                                         symmetrical=False,
                                         null=True,
                                         blank=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    slug = models.SlugField(max_length=200,
                            unique=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10,
                                           decimal_places=2)
    remaining_product = models.IntegerField()
    specifications = models.ManyToManyField('Specification',
                                            related_name='related_specification')
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)

    objects: managers

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    phone = models.CharField(max_length=20,
                             null=True,
                             blank=True)
    address = models.CharField(max_length=255,
                               null=True,
                               blank=True)
    orders = models.ManyToManyField('Order',
                                    related_name='related_customer',
                                    null=True,
                                    blank=True)

    class Meta:
        ordering = ['user']

    def __str__(self):
        return f"Покупатель: {self.user.first_name} {self.user.last_name}"


class Specification(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name}: {self.value}"


class CartProduct(models.Model):
    user = models.ForeignKey('Customer',
                             on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart',
                             on_delete=models.CASCADE,
                             related_name='related_products')
    product = models.ForeignKey('Product',
                                on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=10,
                                      decimal_places=2)

    def __str__(self):
        return f"Продукт {self.product.title} (для корзины)"


class Cart(models.Model):
    owner = models.ForeignKey('Customer',
                              null=True,
                              on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct,
                                      blank=True,
                                      related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=10,
                                      default=0,
                                      decimal_places=2)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    customer = models.ForeignKey(Customer,
                                 related_name='related_orders',
                                 on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=1024, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказа',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )

    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')

    def __str__(self):
        return str(self.id)

from django.contrib.sites import managers
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,
                            unique=True)
    parent_category = models.ForeignKey('self',
                                        on_delete=models.CASCADE,
                                        null=True,
                                        blank=True)
    objects: managers

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
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200,
                            unique=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10,
                                           decimal_places=2,
                                           null=True,
                                           blank=True)
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

    objects: managers

    class Meta:
        ordering = ['user']

    def __str__(self):
        return f"Покупатель: {self.user.first_name} {self.user.last_name}"


class Specification(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    objects: managers

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

    objects: managers

    def __str__(self):
        return f"Продукт {self.product.name} (для корзины)"


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

    objects: managers

    def __str__(self):
        return str(self.id)

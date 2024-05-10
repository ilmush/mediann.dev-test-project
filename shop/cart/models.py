from typing import Type

from django.contrib.sites import managers
from django.db import models
from django.db.models import QuerySet

from shop.models import Customer, Product


class CartProduct(models.Model):
    user: Type[Customer] = models.ForeignKey(Customer,
                                             on_delete=models.CASCADE)
    cart: Type['Cart'] = models.ForeignKey('Cart',
                                           on_delete=models.CASCADE,
                                           related_name='related_products')
    product: Type[Product] = models.ForeignKey(Product,
                                               on_delete=models.CASCADE)
    qty: int = models.PositiveIntegerField(default=1)
    final_price: int = models.DecimalField(max_digits=10,
                                           decimal_places=2)

    objects: managers

    def __str__(self):
        return f"Продукт {self.product.name} (для корзины)"


class Cart(models.Model):
    owner: Type[Customer] = models.ForeignKey(Customer,
                                              null=True,
                                              on_delete=models.CASCADE)
    products: QuerySet[CartProduct] = models.ManyToManyField(CartProduct,
                                                             blank=True,
                                                             related_name='related_cart')
    total_products: int = models.PositiveIntegerField(default=0)
    final_price: int = models.DecimalField(max_digits=10,
                                           default=0,
                                           decimal_places=2)
    in_order: bool = models.BooleanField(default=False)
    for_anonymous_user: bool = models.BooleanField(default=False)

    objects: managers

    def __str__(self):
        return str(self.id)

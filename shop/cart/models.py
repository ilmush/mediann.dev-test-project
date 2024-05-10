from django.contrib.sites import managers
from django.db import models


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

from typing import Type

from django.contrib.sites import managers
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

User = get_user_model()


class Category(models.Model):
    name: str = models.CharField(max_length=255)
    slug: str = models.SlugField(max_length=255,
                                 unique=True)
    parent_category: Type['Category'] = models.ForeignKey('self',
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
    name: str = models.CharField(max_length=255)
    slug: str = models.SlugField(max_length=200,
                                 unique=True)
    price: float = models.DecimalField(max_digits=10,
                                       decimal_places=2)
    discounted_price: float = models.DecimalField(max_digits=10,
                                                  decimal_places=2,
                                                  null=True,
                                                  blank=True)
    remaining_product: int = models.IntegerField()
    specifications: QuerySet['Specification'] = models.ManyToManyField('Specification',
                                                                       related_name='related_specification')
    category: Type[Category] = models.ForeignKey(Category,
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
    user: Type[User] = models.ForeignKey(User,
                                         on_delete=models.CASCADE)
    phone: str = models.CharField(max_length=20,
                                  null=True,
                                  blank=True)
    address: str = models.CharField(max_length=255,
                                    null=True,
                                    blank=True)

    objects: managers

    class Meta:
        ordering = ['user']

    def __str__(self):
        return f"Покупатель: {self.user.first_name} {self.user.last_name}"


class Specification(models.Model):
    name: str = models.CharField(max_length=255)
    value: str = models.CharField(max_length=255)

    objects: managers

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name}: {self.value}"

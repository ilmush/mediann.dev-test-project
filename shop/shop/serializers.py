from rest_framework import serializers

from shop.models import Category, Specification, Product


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'parent_category')


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ('id', 'name', 'value')


class ProductSerializer(serializers.ModelSerializer):
    specifications = SpecificationSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'price', 'discounted_price', 'remaining_product', 'specifications', 'category')

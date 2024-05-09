from rest_framework import serializers

from .models import Category, Specification, Product, CartProduct, Cart


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


class CartProductSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = CartProduct
        fields = ('qty', 'user', 'product', )


class CartSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    products = CartProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'

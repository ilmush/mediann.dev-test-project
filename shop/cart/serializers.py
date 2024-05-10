from rest_framework import serializers

from cart.models import CartProduct, Cart


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

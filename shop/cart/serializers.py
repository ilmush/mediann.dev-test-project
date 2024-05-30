from typing import Dict, Iterable

from rest_framework import serializers

from cart.models import CartProduct, Cart


class CartProductSerializer(serializers.ModelSerializer):
    product: Dict[str, str] = serializers.StringRelatedField()
    user: Dict[str, str] = serializers.StringRelatedField()

    class Meta:
        model = CartProduct
        fields = ('qty', 'user', 'product', )


class CartSerializer(serializers.ModelSerializer):
    owner: Dict[str, str] = serializers.StringRelatedField()
    products: Iterable[Dict[str, str]] = CartProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = ('owner', 'products', 'total_products', 'final_price')

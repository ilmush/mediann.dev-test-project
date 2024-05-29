from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from cart.mixins import CartMixin
from cart.models import Cart, CartProduct
from cart.utils import recalc_cart
from cart.serializers import CartSerializer

from shop.models import Product


class CartView(CartMixin, ReadOnlyModelViewSet):
    queryset = Cart.objects.all().prefetch_related('products', 'owner')
    serializer_class = CartSerializer


class AddToCartView(CartMixin, APIView):
    def get(self, request, *args, **kwargs) -> Cart:
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, product=product, final_price=product.price
        )
        if created:
            self.cart.products.add(cart_product)
        recalc_cart(self.cart)

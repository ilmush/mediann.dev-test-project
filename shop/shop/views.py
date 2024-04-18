from django.db.models import Max, Min, Sum
from django.http import HttpResponseRedirect
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from .mixins import CartMixin
from .serializers import *
from .utils import recalc_cart


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)

        response_data = {'result': response.data}
        response_data['max_price'] = queryset.aggregate(total=Max('price'))
        response_data['min_price'] = queryset.aggregate(total=Min('price'))
        response_data['sum_remaining_product'] = queryset.aggregate(total=Sum('remaining_product'))
        response.data = response_data

        return response


class ProductsByCategoryViewSet(ListAPIView):
    queryset = Product.objects.all()

    def list(self, request, *args, **kwargs):
        category = Category.objects.get(slug=self.kwargs['category_slug'])
        products_category = Product.objects.filter(category=category)
        subcategories = category.subcategory.all()

        for subcategory in subcategories:
            subcategory_products = Product.objects.filter(category=subcategory)
            products_category = products_category | subcategory_products

        serializer = ProductSerializer(products_category, many=True)

        return Response(serializer.data)


class CartView(CartMixin, APIView):
    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer)

        serializer = CartSerializer(cart)

        return Response(serializer.data)


class AddToCartView(CartMixin, APIView):
    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, product=product, final_price=product.price
        )
        if created:
            self.cart.products.add(cart_product)
        recalc_cart(self.cart)
        return HttpResponseRedirect('/')


class OrderApiView(CreateAPIView):
    model = Order
    serializer_class = OrderSerializer

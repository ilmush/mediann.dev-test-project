from django.db.models import Max, Min, Sum
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from mainapp import settings
from .mixins import CartMixin
from .serializers import *
from .utils import recalc_cart

import requests


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all().prefetch_related('specifications')
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
    queryset = Product.objects.all().prefetch_related('specifications')

    def list(self, request, *args, **kwargs):
        category = Category.objects.get(slug=self.kwargs['category_slug'])
        products_category = Product.objects.filter(category=category)
        subcategories = Category.objects.filter(parent_category=category)

        for subcategory in subcategories:
            subcategory_products = Product.objects.filter(category=subcategory)
            products_category = products_category | subcategory_products

        serializer = ProductSerializer(products_category, many=True)

        return Response(serializer.data)


class CartView(CartMixin, ReadOnlyModelViewSet):
    queryset = Cart.objects.all().prefetch_related('products', 'owner')
    serializer_class = CartSerializer


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


class MakeOrderApiView(APIView):
    def get(self, request, *args, **kwargs):
        url = settings.PAYMENT_SERVICE_URL
        cart = Cart.objects.get(id=self.kwargs['id'])
        user = cart.owner.user

        data = {
            "amount": str(cart.final_price),
            "items_qty": str(cart.total_products),
            "api_token": settings.PAYMENT_SERVICE_ACCESS_TOKEN,
            "user_email": user.email
        }
        json_data = json.dumps(data)
        response = requests.post(url, data=json_data)
        json_data = response.json()

        send_order_info_mail(json_data, user.email)

        return Response(json_data)


def send_order_info_mail(data, email):
    """
    Функция отправки почтовых сообщений с информацией о заказе
    """
    recipient_email = email
    subject = 'Payment Information'
    message = f"Номер заказа: {data['orderId']}" \
              f"\nСылка на оплату заказа {data['url']}"
    sender_email = 'django.shop@mail.ru'

    send_mail(subject, message, sender_email, [recipient_email])

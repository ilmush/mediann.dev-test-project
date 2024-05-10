from django.db.models import Max, Min, Sum
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from cart.models import Cart
from mainapp import settings
from .emailUtils import send_order_info_mail
from .serializers import ProductSerializer
from .models import Product, Category

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

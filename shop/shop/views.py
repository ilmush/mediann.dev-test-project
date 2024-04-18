from django.db.models import Max, Min, Sum
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import *


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

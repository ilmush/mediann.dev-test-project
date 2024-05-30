"""
URL configuration for mainapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from rest_framework.routers import SimpleRouter

from cart.views import CartViewSet, AddToCartView
from .yasg import urlpatterns as doc_urls
from shop.views import ProductViewSet, MakeOrderApiView, ProductsByCategoryListAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = SimpleRouter()

router.register(r'product', ProductViewSet)
router.register(r'cart', CartViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('make-order/<int:id>/', MakeOrderApiView.as_view()),
    path('category/<slug:category_slug>/', ProductsByCategoryListAPIView.as_view(), name='product_by_category'),
    path('add-to-cart/<str:slug>/', AddToCartView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]

urlpatterns += router.urls
urlpatterns += doc_urls

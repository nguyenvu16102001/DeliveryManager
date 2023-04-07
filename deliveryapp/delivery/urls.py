from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('product', views.ProductViewSet)
router.register('order', views.OrderViewSet)
router.register('order_detail', views.OrderDetailViewSet)
router.register('auction', views.AuctionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
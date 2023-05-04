from django.urls import path, include
from . import views
from rest_framework import routers
from .admin import admin_site


router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('product', views.ProductViewSet)
router.register('order', views.OrderViewSet)
router.register('order_detail', views.OrderDetailViewSet)
router.register('auction', views.AuctionViewSet)
router.register('shipper', views.ShipperViewSet)
router.register('customer', views.CustomerViewSet)
router.register('rating', views.RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin_site.urls),
]
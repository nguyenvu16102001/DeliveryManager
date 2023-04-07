import parser
from rest_framework import viewsets, generics, permissions
from .models import User, Product, Order, OrderDetail, Auction
from .serializers import UserSerializer, ProductSerializer, OrderSerializer, OrderDetailSerializer, AuctionSerializer
from rest_framework.parsers import MultiPartParser


class ProductViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Product.objects.filter(active=True)
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Order.objects.filter(active=True)
    serializer_class = OrderSerializer


class OrderDetailViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = OrderDetail.objects.filter(active=True)
    serializer_class = OrderDetailSerializer


class AuctionViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Auction.objects.filter(active=True)
    serializer_class = AuctionSerializer


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

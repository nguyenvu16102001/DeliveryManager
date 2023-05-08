from django.core.exceptions import ObjectDoesNotExist

from django.core.mail import send_mail
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, generics, permissions, status
from .models import User, Product, Order, OrderDetail, Auction, Shipper, Rating, Customer
from .perms import RatingOwner
from .serializers import UserSerializer, ProductSerializer, OrderSerializer, OrderDetailSerializer, \
    AuctionSerializer, ShipperSerializer, CommentSerializer, RateSerializer, RatingSerializer, CustomerSerializer
from rest_framework.parsers import MultiPartParser

import logging

logger = logging.getLogger(__name__)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.filter(active=True)
    serializer_class = OrderSerializer


class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.filter(active=True)
    serializer_class = OrderDetailSerializer


class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.filter(active=True)
    serializer_class = AuctionSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.filter(active=True)
    serializer_class = CustomerSerializer


class ShipperViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Shipper.objects.filter(active=True)
    serializer_class = ShipperSerializer

    def get_permissions(self):
        if self.action in ['comments', 'rate']:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    @action(methods=['post'], detail=True, url_path='comments')
    def comments(self, request, pk):
        shipper = Shipper.objects.get(pk=pk)
        customer = Customer.objects.get(pk=request.user.id)
        r, _ = Rating.objects.get_or_create(customer=customer, shipper=shipper)
        r.comment = request.data['comment']
        r.save()
        return Response(CommentSerializer(r), status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='rate')
    def rate(self, request, pk):
        shipper = Shipper.objects.get(pk=pk)
        customer = Customer.objects.get(pk=request.user.id)
        r, _ = Rating.objects.get_or_create(customer=customer, shipper=shipper)
        r.rate = request.data['rate']
        r.save()
        return Response(RateSerializer(r), status=status.HTTP_200_OK)


class RatingViewSet(viewsets.ViewSet, generics.ListAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Rating.objects.filter(active=True)
    serializer_class = RatingSerializer

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            return [RatingOwner()]

        return [permissions.AllowAny()]


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.UpdateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]

    def get_permissions(self):
        if self.action == 'current_user':
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    @action(methods=['get'], detail=False, url_path='current-user')
    def current_user(self, request):
        return Response(self.serializer_class(request.user).data)

    @action(methods=['get'], detail=True, url_path="send-mail", url_name="send-mail")
    def send_mail_async(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            type = request.data['type']
            title = ''
            content = ''
            if type == 'auction_win':
                title = 'Dau Gia Thanh Cong'
                content = 'Ban da duoc chon de giao don hang'
            elif type == 'auction_lose':
                title = 'Dau Gia That Bai'
                content = 'Ban khong duoc chon de giao don hang'
            elif type == 'order':
                title = 'Hoan Thanh Don Hang'
                content = 'Don hang cua ban da duoc giao thanh cong'
            send_mail(
                title,
                content,
                '1951012152vu@ou.edu.vn',
                [user.email],
                fail_silently=False,
            )
        except ObjectDoesNotExist:
            return f"User with pk {pk} does not exist"
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_200_OK)

    def send_mail(self, request, pk):
        self.send_mail_async.delay(pk=pk)

        return Response(status=status.HTTP_202_ACCEPTED)

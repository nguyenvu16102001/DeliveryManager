import parser

from django.core.exceptions import ObjectDoesNotExist

from django.core.mail import send_mail
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, generics, permissions, status
from .models import User, Product, Order, OrderDetail, Auction
from .serializers import UserSerializer, ProductSerializer, OrderSerializer, OrderDetailSerializer, AuctionSerializer
from rest_framework.parsers import MultiPartParser

import logging

from ..deliveryapp.settings import EMAIL_HOST_USER

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


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    @action(methods=['get'], detail=True, url_path="send-mail", url_name="send-mail")
    def send_mail_async(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            send_mail(
                'Thong bao don hang',
                'Don hang cua ban da hoan thanh.',
                EMAIL_HOST_USER,
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


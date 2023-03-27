import parser
from rest_framework import viewsets, generics, permissions
from .models import User
from .serializers import UserSerializer
from rest_framework.parsers import MultiPartParser


# Create your views here.
class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

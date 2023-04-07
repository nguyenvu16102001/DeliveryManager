from rest_framework.serializers import ModelSerializer
from .models import User, Product, Order, OrderDetail, Auction


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'product_type', 'image', 'description']


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['customer', 'shipper', 'name', 'delivery_charges', 'delivery_address', 'state', 'delivery_date', 'description']


class OrderDetailSerializer(ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['product', 'order', 'number', 'price']


class OrderDetailSerializer(ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['product', 'order', 'number', 'price']


class AuctionSerializer(ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['order', 'shipper', 'auction_price']


class UserSerializer(ModelSerializer):
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email', 'avatar', 'phone', 'address']
        extra_kwargs = {
            'password': {'write_only': True}
        }
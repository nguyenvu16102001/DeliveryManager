from rest_framework.serializers import ModelSerializer
from .models import User, Product, Order, OrderDetail, Auction, Shipper, Rating, Customer


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'product_type', 'image', 'description']


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'shipper', 'name', 'delivery_charges', 'delivery_address', 'state', 'delivery_date', 'description']


class OrderDetailSerializer(ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['id', 'product', 'order', 'number', 'price']


class AuctionSerializer(ModelSerializer):
    class Meta:
        model = Auction
        fields = ['order', 'shipper', 'auction_price']


class ShipperSerializer(ModelSerializer):
    class Meta:
        model = Shipper
        fields = ['shipper', 'starting_date']


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customer', 'membership_level']


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


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ['customer', 'shipper', 'comment', 'created_date', 'updated_date']


class RateSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ['customer', 'shipper', 'rate', 'created_date', 'updated_date']


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'customer', 'shipper', 'rate', 'comment', 'created_date', 'updated_date']
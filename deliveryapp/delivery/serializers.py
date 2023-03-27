from rest_framework.serializers import ModelSerializer
from .models import User


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
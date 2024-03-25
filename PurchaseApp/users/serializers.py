from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from .models import Transaction, UserProduct

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
            return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('amount', 'transaction_type')


class PurchaseSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = UserProduct
        fields = ('product_id',)

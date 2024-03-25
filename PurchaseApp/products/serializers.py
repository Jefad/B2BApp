from abc import ABC

from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'size', 'price')


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductRatingSerializer(serializers.Serializer):
    score = serializers.ChoiceField(default=0, choices=((0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)))


class ProductCommentSerializer(serializers.Serializer):
    score = serializers.CharField(default='Your Comment')

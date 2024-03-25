from django.shortcuts import render

from rest_framework import generics, mixins, status, permissions
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from .models import Product
from .serializers import ProductSerializer, ProductUpdateSerializer, ProductRatingSerializer, ProductCommentSerializer

from log_reg.classes import TokenChecker

import json


class ProductCreateAPIView(generics.CreateAPIView, generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def create(self, request, *args, **kwargs):
        token_status = TokenChecker()
        data = request.data
        serializer = ProductSerializer(data=data)

        if serializer.is_valid():
            product = Product.objects.create(**serializer.validated_data)
            return Response({'detail': 'The new product was created.',
                             'product features': serializer.validated_data,
                             'access': token_status.access,
                             'refresh': token_status.refresh}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid data.'}, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        filtered_data = Product.objects.filter(id=kwargs.get('pk')).values()
        return Response(data=filtered_data.last())


class ProductUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def update(self, request, *args, **kwargs):


class ProductDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class ProductRatingAPIView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductRatingSerializer
    permission_classes = [permissions.AllowAny]

    def update(self, request, *args, **kwargs):
        user_score = int(request.data.get('score'))
        instance = Product.objects.filter(id=kwargs.get('pk')).last()

        votes = int(instance.votes)
        rating = float(instance.rating)
        new_rating = (rating * votes + user_score)/(votes + 1)

        instance.votes = votes + 1
        instance.rating = new_rating
        instance.save()

        serializer = ProductUpdateSerializer(instance)

        return Response({'detail': f"The rating and votes for the {instance.name} "
                                   f"product were updated.",
                         'product': serializer.data}, status=status.HTTP_200_OK)

        # return Response({'detail': 'Invalid data!'}, status=status.HTTP_400_BAD_REQUEST)


class ProductCommentAPIView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCommentSerializer
    permission_classes = [permissions.AllowAny]

    def update(self, request, *args, **kwargs):
        user_score = int(request.data.get('score'))
        instance = Product.objects.filter(id=kwargs.get('pk')).last()

        votes = int(instance.votes)
        rating = float(instance.rating)
        new_rating = (rating * votes + user_score)/(votes + 1)

        instance.votes = votes + 1
        instance.rating = new_rating
        instance.save()

        serializer = ProductUpdateSerializer(instance)

        return Response({'detail': f"The rating and votes for the {instance.name} "
                                   f"product were updated.",
                         'product': serializer.data}, status=status.HTTP_200_OK)

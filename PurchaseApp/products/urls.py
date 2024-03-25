from django.urls import path
from .views import ProductCreateAPIView, ProductDetailAPIView, ProductUpdateAPIView, ProductDestroyAPIView, ProductRatingAPIView


urlpatterns = [
    path('', ProductDetailAPIView.as_view(), name='product-all-view'),
    path('<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('create/', ProductCreateAPIView.as_view(), name='product-create'),
    path('<int:pk>/update/', ProductUpdateAPIView.as_view(), name='product-update'),
    path('<int:pk>/delete/', ProductDestroyAPIView.as_view(), name='product-destroy'),
    path('<int:pk>/rating/', ProductRatingAPIView.as_view(), name='product-rating'),
]

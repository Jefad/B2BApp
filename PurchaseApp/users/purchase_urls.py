from django.urls import path
from .views import TransactionAPIView, PurchaseAPIView

urlpatterns = [
    path('transaction/', TransactionAPIView.as_view(), name='transaction'),
    path('', PurchaseAPIView.as_view(), name='purchase'),
]

from django.db import models
from django.contrib.auth.models import User

from datetime import datetime


class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    size = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    date_released = models.DateTimeField(default=datetime.now(tz=None))
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    downloads = models.PositiveIntegerField(default=0)
    purchase_count = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    votes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "product"

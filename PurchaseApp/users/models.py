from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import transaction

from products.models import Product


class UserProduct(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_product"
        unique_together = (('user', 'product'),)


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=False, blank=False)
    rating = models.PositiveSmallIntegerField(choices=((0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)), null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "comment"


class Transaction(models.Model):
    class TransactionType(models.Choices):
        Charge = 1
        Purchase = 2

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.PositiveSmallIntegerField(choices=TransactionType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "transaction"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.transaction_type == Transaction.TransactionType.Charge.value:
            with transaction.atomic():
                credit, _ = Credit.objects.select_for_update().get_or_create(user=self.user)
                credit.balance += self.amount
                credit.save(update_fields=['balance', 'updated_at'])
                super().save()
        else:
            with transaction.atomic():
                credit, _ = Credit.objects.select_for_update().get_or_create(user=self.user)
                credit.balance -= self.amount
                if credit.balance >= 0.0:
                    credit.save(update_fields=['balance', 'updated_at'])
                    super().save()
                else:
                    raise Exception("The balance is less than product price!")


class Credit(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "credit"

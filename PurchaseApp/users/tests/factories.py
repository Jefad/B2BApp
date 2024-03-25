from factory.django import DjangoModelFactory

from users.models import UserProduct, Credit, Comment, Transaction


class UserProductFactory(DjangoModelFactory):
    class Meta:
        model = UserProduct


class CreditFactory(DjangoModelFactory):
    class Meta:
        model = Credit


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment


class TransactionFactory(DjangoModelFactory):
    class Meta:
        model = Transaction

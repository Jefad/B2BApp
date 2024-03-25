from factory.django import DjangoModelFactory
import factory

from products.models import Product


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    # name = factory.Faker



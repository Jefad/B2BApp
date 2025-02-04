# Generated by Django 4.0.10 on 2024-02-22 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Charge'), (2, 'Purchase')]),
        ),
    ]

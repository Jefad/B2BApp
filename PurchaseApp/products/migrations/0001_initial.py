# Generated by Django 4.0.10 on 2024-02-22 14:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('size', models.DecimalField(decimal_places=2, max_digits=5)),
                ('date_released', models.DateTimeField(default=datetime.datetime(2024, 2, 22, 17, 31, 23, 858360))),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('downloads', models.PositiveIntegerField(default=0)),
                ('purchase_count', models.PositiveIntegerField(default=0)),
                ('rating', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('votes', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'product',
            },
        ),
    ]

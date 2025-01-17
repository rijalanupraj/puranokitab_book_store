# Generated by Django 3.0.5 on 2020-06-07 05:10

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_your_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='market_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, max_length=240, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='your_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
    ]

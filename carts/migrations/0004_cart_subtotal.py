# Generated by Django 3.0.5 on 2020-06-02 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_auto_20200602_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=60),
        ),
    ]
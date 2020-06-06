# Generated by Django 3.0.5 on 2020-06-04 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0003_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='address_type',
            field=models.CharField(blank=True, choices=[('billing', 'Billing'), ('shipping', 'Shipping')], max_length=120),
        ),
    ]
# Generated by Django 3.0.5 on 2020-06-04 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0005_auto_20200604_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_line_1',
            field=models.CharField(max_length=120),
        ),
    ]
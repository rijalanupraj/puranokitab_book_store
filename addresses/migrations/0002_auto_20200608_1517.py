# Generated by Django 3.0.5 on 2020-06-08 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(max_length=120),
        ),
        migrations.AlterField(
            model_name='address',
            name='district',
            field=models.CharField(max_length=120),
        ),
    ]

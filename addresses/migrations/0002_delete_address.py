# Generated by Django 3.0.5 on 2020-06-03 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Address',
        ),
    ]
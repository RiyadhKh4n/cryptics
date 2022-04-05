# Generated by Django 3.2 on 2022-04-05 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_asset_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='price',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='asset',
            name='ticker',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='name',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
# Generated by Django 3.2 on 2022-03-10 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_auto_20220310_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='PnL',
            field=models.DecimalField(decimal_places=3, default='0.00', max_digits=10),
        ),
    ]
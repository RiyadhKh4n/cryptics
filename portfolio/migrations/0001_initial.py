# Generated by Django 3.2 on 2022-03-10 19:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('coin', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('USDvalue', models.DecimalField(decimal_places=2, default='0.00', max_digits=5)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['USDvalue'],
            },
        ),
        migrations.CreateModel(
            name='Assets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=3)),
                ('AveragePrice', models.DecimalField(decimal_places=2, max_digits=3)),
                ('USDSpent', models.DecimalField(decimal_places=2, max_digits=3)),
                ('USDEarned', models.DecimalField(decimal_places=2, max_digits=3)),
                ('CurrentInvestment', models.DecimalField(decimal_places=2, max_digits=3)),
                ('added_to_portfolio', models.DateTimeField(auto_now_add=True)),
                ('coinID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coin.coin')),
                ('portfolioID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portfolio.portfolio')),
            ],
            options={
                'ordering': ['added_to_portfolio'],
            },
        ),
    ]
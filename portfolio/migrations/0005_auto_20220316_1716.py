# Generated by Django 3.2 on 2022-03-16 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_asset_pnl'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='portfolio',
            options={'ordering': ['-USDvalue']},
        ),
        migrations.RenameField(
            model_name='asset',
            old_name='portfolioID',
            new_name='portfolio_name',
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='USDvalue',
            field=models.DecimalField(blank=True, decimal_places=3, default='0.00', max_digits=10),
        ),
    ]

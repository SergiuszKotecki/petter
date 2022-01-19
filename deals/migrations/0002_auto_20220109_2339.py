# Generated by Django 3.2.11 on 2022-01-09 22:39

from decimal import Decimal

import djmoney.models.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('deals', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='delivery_cost',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default_currency='PLN', max_digits=19,
                                                   null=True),
        ),
        migrations.AlterField(
            model_name='deal',
            name='historical_price',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default=Decimal('0'),
                                                   default_currency='PLN', max_digits=19, null=True),
        ),
    ]
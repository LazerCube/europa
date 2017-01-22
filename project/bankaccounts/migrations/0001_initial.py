# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-01-22 14:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=255)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Current balance')),
                ('inital_balance', models.DecimalField(decimal_places=2, default=0, help_text='Initial balance will automatically update the balance.', max_digits=10, verbose_name='Initial balance')),
                ('owners', models.ManyToManyField(db_table='bankaccounts_owners', related_name='bankaccounts', to=settings.AUTH_USER_MODEL, verbose_name='Owners')),
            ],
            options={
                'db_table': 'bankaccounts',
            },
        ),
    ]
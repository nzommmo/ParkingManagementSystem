# Generated by Django 5.1.5 on 2025-02-01 07:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0017_remove_payment_payment_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]

# Generated by Django 5.1.5 on 2025-01-31 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0013_ticket_stay_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='stay_duration',
        ),
    ]

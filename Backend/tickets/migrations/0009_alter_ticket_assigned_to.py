# Generated by Django 5.1.5 on 2025-01-31 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0008_alter_ticket_assigned_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='assigned_to',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]

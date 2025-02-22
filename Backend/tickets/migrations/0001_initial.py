# Generated by Django 5.1.5 on 2025-01-27 14:19

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PricingRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('role', models.CharField(choices=[('Admin', 'Admin'), ('Parking-lot Attendant', 'Parking-lot Attendant'), ('User', 'User')], default='User', max_length=25)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_to', models.CharField(max_length=255, unique=True)),
                ('guest_email', models.EmailField(blank=True, max_length=255, null=True)),
                ('guest_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Paid', 'Paid'), ('Payment_In_Progress', 'Payment In Progress'), ('Unpaid', 'Unpaid')], default='Unpaid', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('rate', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tickets.pricingrate')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tickets.user')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('payment_method', models.CharField(choices=[('Mpesa', 'Mpesa'), ('Cash', 'Cash'), ('Bank', 'Bank')], default='Cash', max_length=10)),
                ('payment_status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=10)),
                ('payment_date', models.DateField(blank=True, null=True)),
                ('payment_time', models.TimeField(blank=True, null=True)),
                ('ticket', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='tickets.ticket')),
            ],
        ),
        migrations.CreateModel(
            name='LoyaltyPoints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_points_earned', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('last_earned_date', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tickets.user')),
            ],
            options={
                'verbose_name_plural': 'Loyalty Points',
            },
        ),
    ]

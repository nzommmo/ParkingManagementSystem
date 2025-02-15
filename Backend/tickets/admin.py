# tickets/admin.py
from django.contrib import admin
from .models import User, PricingRate, Ticket, Payment, LoyaltyPoints

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'role', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('role', 'created_at')

@admin.register(PricingRate)
class PricingRateAdmin(admin.ModelAdmin):
    list_display = ('rate', 'description')
    search_fields = ('description',)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('assigned_to', 'user', 'status', 'start_time', 'end_time')
    list_filter = ('status', 'created_at')
    search_fields = ('assigned_to', 'guest_email', 'guest_phone')
    readonly_fields = ('stay_duration',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'amount', 'payment_method', 'payment_status', 'payment_date')
    list_filter = ('payment_status', 'payment_method')
    search_fields = ('ticket__assigned_to',)

@admin.register(LoyaltyPoints)
class LoyaltyPointsAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'total_points_earned', 'last_earned_date')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
# serializers.py
from decimal import Decimal
from rest_framework import serializers
from .models import User, Ticket, LoyaltyPoints,PricingRate,Payment
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Hash password before saving
        user = User.objects.create(**validated_data)
        user.password = make_password(validated_data['password'])
        user.save()
        return user

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'assigned_to', 'user', 'guest_email', 'guest_phone', 
                 'start_time', 'end_time', 'stay_duration', 'rate', 'status')

class LoyaltyPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyPoints
        fields = ('points', 'total_points_earned', 'last_earned_date')



class PricingRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingRate
        fields = ['id', 'rate', 'description']

class PaymentSerializer(serializers.ModelSerializer):
    ticket_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Payment
        fields = [
            'id',
            'ticket',
            'ticket_details',
            'amount',
            'payment_method',
            'payment_status',
            'payment_date',
            'payment_time'
        ]
        read_only_fields = []  # Amount is calculated automatically
    
    def get_ticket_details(self, obj):
        return {
            'assigned_to': obj.ticket.assigned_to,
            'start_time': obj.ticket.formatted_start_time,
            'end_time': obj.ticket.formatted_end_time,
            'duration': obj.ticket.stay_duration,
            'rate': str(obj.ticket.rate.rate)
        }
    
    def create(self, validated_data):
        ticket = validated_data['ticket']
        
        # Calculate amount if end_time is available
        if ticket.end_time:
            duration = ticket.end_time - ticket.start_time
            hours = duration.total_seconds() / 3600
            # Round up to nearest hour
            hours = Decimal(str(round(hours + 0.49)))
            amount = ticket.rate.rate * hours
            validated_data['amount'] = amount
        
        return super().create(validated_data)
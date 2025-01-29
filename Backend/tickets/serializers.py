# serializers.py
from rest_framework import serializers
from .models import User, Ticket, LoyaltyPoints,PricingRate
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
                 'start_time', 'end_time', 'rate', 'status')

class LoyaltyPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyPoints
        fields = ('points', 'total_points_earned', 'last_earned_date')


from rest_framework import serializers
from .models import PricingRate

class PricingRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingRate
        fields = ['id', 'rate', 'description']


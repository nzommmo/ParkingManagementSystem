from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import datetime, timedelta

from .models import User, PricingRate, Ticket, Payment, LoyaltyPoints

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="testpass123",
            role="User"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.role, "User")
        self.assertTrue(isinstance(self.user.created_at, datetime))

class PricingRateTest(TestCase):
    def setUp(self):
        self.rate = PricingRate.objects.create(
            rate=Decimal('50.00'),
            description="Hourly rate"
        )

    def test_pricing_rate_creation(self):
        self.assertEqual(self.rate.rate, Decimal('50.00'))
        self.assertEqual(self.rate.description, "Hourly rate")

class TicketTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="testpass123"
        )
        self.rate = PricingRate.objects.create(rate=Decimal('50.00'))
        self.ticket = Ticket.objects.create(
            assigned_to="KAA123",
            user=self.user,
            rate=self.rate
        )

    def test_ticket_creation(self):
        self.assertEqual(self.ticket.assigned_to, "KAA123")
        self.assertEqual(self.ticket.status, "Unpaid")
        self.assertIsNotNone(self.ticket.start_time)

    def test_ticket_validation_user_or_guest(self):
        # Test ticket without user or guest info
        with self.assertRaises(ValidationError):
            invalid_ticket = Ticket.objects.create(
                assigned_to="KAA124",
                rate=self.rate
            )

        # Test ticket with both user and guest info
        with self.assertRaises(ValidationError):
            invalid_ticket = Ticket.objects.create(
                assigned_to="KAA125",
                user=self.user,
                guest_email="guest@example.com",
                rate=self.rate
            )

    def test_stay_duration(self):
        self.ticket.status = 'Payment_In_Progress'
        self.ticket.save()
        self.assertIsNotNone(self.ticket.end_time)
        self.assertIsNotNone(self.ticket.stay_duration)

class PaymentTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com"
        )
        self.rate = PricingRate.objects.create(rate=Decimal('50.00'))
        self.ticket = Ticket.objects.create(
            assigned_to="KAA123",
            user=self.user,
            rate=self.rate
        )

    def test_payment_creation_signal(self):
        # Test that payment was automatically created with ticket
        payment = Payment.objects.filter(ticket=self.ticket).first()
        self.assertIsNotNone(payment)
        self.assertEqual(payment.payment_status, "Pending")
        self.assertEqual(payment.amount, Decimal('0'))

    def test_payment_completion(self):
        payment = Payment.objects.get(ticket=self.ticket)
        payment.amount = Decimal('100.00')
        payment.payment_status = 'Completed'
        payment.save()

        # Refresh ticket from database
        self.ticket.refresh_from_db()
        
        # Check ticket status was updated
        self.assertEqual(self.ticket.status, 'Paid')
        
        # Check payment timestamps were set
        self.assertIsNotNone(payment.payment_date)
        self.assertIsNotNone(payment.payment_time)

class LoyaltyPointsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com"
        )
        self.rate = PricingRate.objects.create(rate=Decimal('50.00'))
        self.ticket = Ticket.objects.create(
            assigned_to="KAA123",
            user=self.user,
            rate=self.rate
        )
        self.payment = Payment.objects.get(ticket=self.ticket)

    def test_loyalty_points_creation(self):
        # Set payment amount and complete it
        self.payment.amount = Decimal('100.00')
        self.payment.payment_status = 'Completed'
        self.payment.save()

        # Check loyalty points were created
        loyalty_points = LoyaltyPoints.objects.get(user=self.user)
        self.assertEqual(loyalty_points.points, Decimal('1.00'))  # 1% of 100
        self.assertEqual(loyalty_points.total_points_earned, Decimal('1.00'))

    def test_loyalty_points_accumulation(self):
        # Complete first payment
        self.payment.amount = Decimal('100.00')
        self.payment.payment_status = 'Completed'
        self.payment.save()

        # Create and complete second payment
        ticket2 = Ticket.objects.create(
            assigned_to="KAA124",
            user=self.user,
            rate=self.rate
        )
        payment2 = Payment.objects.get(ticket=ticket2)
        payment2.amount = Decimal('200.00')
        payment2.payment_status = 'Completed'
        payment2.save()

        # Check loyalty points were accumulated
        loyalty_points = LoyaltyPoints.objects.get(user=self.user)
        self.assertEqual(loyalty_points.points, Decimal('3.00'))  # 1% of 100 + 200
        self.assertEqual(loyalty_points.total_points_earned, Decimal('3.00'))

class SignalTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com"
        )
        self.rate = PricingRate.objects.create(rate=Decimal('50.00'))

    def test_end_time_signal(self):
        ticket = Ticket.objects.create(
            assigned_to="KAA123",
            user=self.user,
            rate=self.rate
        )
        self.assertIsNone(ticket.end_time)

        # Change status to Payment_In_Progress
        ticket.status = 'Payment_In_Progress'
        ticket.save()
        
        # Refresh from database
        ticket.refresh_from_db()
        self.assertIsNotNone(ticket.end_time)

    def test_payment_status_signals(self):
        ticket = Ticket.objects.create(
            assigned_to="KAA123",
            user=self.user,
            rate=self.rate
        )
        payment = Payment.objects.get(ticket=ticket)
        
        # Set payment as completed
        payment.amount = Decimal('100.00')
        payment.payment_status = 'Completed'
        payment.save()
        
        # Refresh both objects from database
        payment.refresh_from_db()
        ticket.refresh_from_db()
        
        # Check all effects of payment completion
        self.assertEqual(ticket.status, 'Paid')
        self.assertIsNotNone(payment.payment_date)
        self.assertIsNotNone(payment.payment_time)
        
        # Check loyalty points
        loyalty_points = LoyaltyPoints.objects.get(user=self.user)
        self.assertEqual(loyalty_points.points, Decimal('1.00'))  # 1% of 100
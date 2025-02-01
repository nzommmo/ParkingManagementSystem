from decimal import Decimal
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import datetime



class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)  # Hash password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(email, first_name, last_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Parking-lot Attendant', 'Parking-lot Attendant'),
        ('User', 'User'),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(max_length=25, choices=ROLE_CHOICES, default='User')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Required for Django admin

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PricingRate(models.Model):
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Rate: {self.rate}"

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Payment_In_Progress', 'Payment In Progress'),
        ('Unpaid', 'Unpaid'),
    ]

    assigned_to = models.CharField(max_length=255)  
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    guest_email = models.EmailField(max_length=255, null=True, blank=True)
    guest_phone = models.CharField(max_length=15, null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    rate = models.ForeignKey(PricingRate, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Unpaid')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def formatted_start_time(self):
        if self.start_time:
            return self.start_time.strftime("%d %b %Y at %H:%M")
        return None

    @property
    def formatted_end_time(self):
        if self.end_time:
            return self.end_time.strftime("%d %b %Y at %H:%M")
        return None

    @property
    def stay_duration(self):
        if self.end_time and self.start_time:
            duration = self.end_time - self.start_time
            total_seconds = duration.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            return f"{hours:02d}:{minutes:02d}"
        return None

    def calculate_amount(self):
        """Calculate the parking amount based on duration and rate"""
        if self.end_time and self.start_time:
            duration = self.end_time - self.start_time
            hours = duration.total_seconds() / 3600
            # Round up to nearest hour
            hours = Decimal(str(round(hours + 0.49)))
            return self.rate.rate * hours
        return Decimal('0')

    def clean(self):
        # Check for existing active tickets
        active_tickets = Ticket.objects.filter(
            assigned_to=self.assigned_to,
            status__in=['Unpaid', 'Payment_In_Progress']
        )
        
        if self.pk:
            active_tickets = active_tickets.exclude(pk=self.pk)
        
        if active_tickets.exists():
            raise ValidationError({
                'assigned_to': 'An active ticket already exists for this vehicle.'
            })
        
        if not self.user and not (self.guest_email or self.guest_phone):
            raise ValidationError("Either a user or guest contact information must be provided")
        
        if self.user and (self.guest_email or self.guest_phone):
            raise ValidationError("User and guest information cannot be provided simultaneously")

    def save(self, *args, **kwargs):
        if not self.pk:  # New ticket
            self.start_time = timezone.now()
        
        # Get the original ticket if it exists
        if self.pk:
            old_ticket = Ticket.objects.get(pk=self.pk)
            end_time_changed = old_ticket.end_time != self.end_time
        else:
            end_time_changed = False

        self.full_clean()
        super().save(*args, **kwargs)

        # Update associated payment amount if end_time has changed
        if end_time_changed and self.end_time:
            try:
                payment = Payment.objects.get(ticket=self)
                payment.amount = self.calculate_amount()
                payment.save()
            except Payment.DoesNotExist:
                pass

    def __str__(self):
        start_time_str = self.formatted_start_time
        end_time_str = self.formatted_end_time if self.end_time else "Active"
        return f"Ticket {self.id} - {self.assigned_to} ({start_time_str} - {end_time_str})"

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Mpesa', 'Mpesa'),
        ('Cash', 'Cash'),
        ('Bank', 'Bank'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]

    ticket = models.OneToOneField(Ticket, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES, default='Cash')
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    payment_date = models.DateField(default=timezone.now)
    payment_time = models.TimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_payment = Payment.objects.get(pk=self.pk)
                # Check if status is being changed to Completed
                if old_payment.payment_status != 'Completed' and self.payment_status == 'Completed':
                    # Get current time in UTC
                    current_utc = timezone.now()
                    # Convert to local timezone
                    local_time = timezone.localtime(current_utc)
                    self.payment_date = local_time.date()
                    self.payment_time = local_time.time()
                    
                    # Update the ticket status
                    self.ticket.status = 'Paid'
                    self.ticket.save()
            except Payment.DoesNotExist:
                pass
        else:
            # For new payments
            current_utc = timezone.now()
            local_time = timezone.localtime(current_utc)
            self.payment_date = local_time.date()
            self.payment_time = local_time.time()

        super().save(*args, **kwargs)

    def get_formatted_time(self):
        """Return time in 12-hour format"""
        return self.payment_time.strftime("%I:%M %p")

    def __str__(self):
        formatted_time = self.get_formatted_time()
        return f"Payment for Ticket {self.ticket.id} - {self.payment_date} {formatted_time}"



class LoyaltyPoints(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_points_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_earned_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Loyalty Points for {self.user}"

    class Meta:
        verbose_name_plural = "Loyalty Points"
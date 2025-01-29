from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from decimal import Decimal
from .models import Ticket, Payment, LoyaltyPoints

@receiver(post_save, sender=Ticket)
def create_payment(sender, instance, created, **kwargs):
    if created:
        Payment.objects.create(
            ticket=instance,
            amount=0,
            payment_method='Cash',
            payment_status='Pending'
        )

@receiver(pre_save, sender=Ticket)
def set_end_time(sender, instance, **kwargs):
    try:
        old_instance = Ticket.objects.get(pk=instance.pk)
        if instance.status == 'Payment_In_Progress' and old_instance.status != 'Payment_In_Progress':
            instance.end_time = timezone.now()
    except Ticket.DoesNotExist:
        pass

@receiver(pre_save, sender=Payment)
def update_payment_timestamp(sender, instance, **kwargs):
    try:
        old_instance = Payment.objects.get(pk=instance.pk)
        if instance.payment_status == 'Completed' and old_instance.payment_status != 'Completed':
            instance.payment_date = timezone.now().date()
            instance.payment_time = timezone.now().time()
    except Payment.DoesNotExist:
        pass

@receiver(post_save, sender=Payment)
def update_ticket_status(sender, instance, **kwargs):
    if instance.payment_status == 'Completed':
        instance.ticket.status = 'Paid'
        instance.ticket.save()

@receiver(post_save, sender=Payment)
def add_loyalty_points(sender, instance, **kwargs):
    if instance.payment_status == 'Completed' and instance.ticket.user:
        loyalty_points = round(Decimal(instance.amount) * Decimal('0.01'), 2)
        
        loyalty_record, created = LoyaltyPoints.objects.get_or_create(
            user=instance.ticket.user,
            defaults={
                'points': loyalty_points,
                'total_points_earned': loyalty_points,
                'last_earned_date': timezone.now()
            }
        )
        
        if not created:
            loyalty_record.points += loyalty_points
            loyalty_record.total_points_earned += loyalty_points
            loyalty_record.last_earned_date = timezone.now()
            loyalty_record.save()
from decimal import Decimal
from rest_framework import status,viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Ticket, LoyaltyPoints, PricingRate,Payment
from .serializers import UserSerializer, TicketSerializer, LoyaltyPointsSerializer, PricingRateSerializer,PaymentSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from django.utils import timezone


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = User.objects.filter(email=email).first()
    
    if user is None:
        return Response(
            {'detail': 'User not found', 'code': 'user_not_found'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not check_password(password, user.password):
        return Response(
            {'detail': 'Invalid credentials', 'code': 'invalid_credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Generate JWT tokens after successful authentication
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': UserSerializer(user).data
    })



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    # Optionally, you can add a check for admin permissions here
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_id(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_by_id(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user_by_id(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Create loyalty points record for new user
        LoyaltyPoints.objects.create(user=user)
        
        return Response({
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_ticket(request):
    assigned_to = request.data.get('assigned_to')
    
    # Check for existing active tickets
    active_tickets = Ticket.objects.filter(
        assigned_to=assigned_to,
        status__in=['Unpaid', 'Payment_In_Progress']
    )
    
    if active_tickets.exists():
        return Response({
            'error': 'An active ticket already exists for this vehicle.',
            'code': 'active_ticket_exists'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Add user to request data if not guest ticket
    if not (request.data.get('guest_email') or request.data.get('guest_phone')):
        request.data['user'] = request.user.id

    serializer = TicketSerializer(data=request.data)
    if serializer.is_valid():
        ticket = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_tickets(request):
    tickets = Ticket.objects.all()
    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ticket_by_id(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)
    except Ticket.DoesNotExist:
        return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_ticket_by_id(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        old_status = ticket.status
        
        # Check if status is being updated to Payment_In_Progress
        new_status = request.data.get('status')
        if new_status == 'Payment_In_Progress' and old_status != 'Payment_In_Progress':
            # Set end_time to current time
            request.data['end_time'] = timezone.now()
        
        serializer = TicketSerializer(ticket, data=request.data, partial=True)
        if serializer.is_valid():
            updated_ticket = serializer.save()
            
            # If status changed to Payment_In_Progress, update or create payment
            if new_status == 'Payment_In_Progress' and old_status != 'Payment_In_Progress':
                duration = updated_ticket.end_time - updated_ticket.start_time
                # Convert to minutes
                minutes = Decimal(str(round(duration.total_seconds() / 60)))
                # Calculate amount (rate per minute * number of minutes)
                amount = (updated_ticket.rate.rate / Decimal('60')) * minutes
                
                # Update or create payment
                payment, created = Payment.objects.get_or_create(
                    ticket=updated_ticket,
                    defaults={
                        'amount': amount,
                        'payment_status': 'Pending'
                    }
                )
                
                if not created:
                    payment.amount = amount
                    payment.save()
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Ticket.DoesNotExist:
        return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_ticket_by_id(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Ticket.DoesNotExist:
        return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_loyalty_points(request):
    try:
        loyalty_points = LoyaltyPoints.objects.get(user=request.user)
        serializer = LoyaltyPointsSerializer(loyalty_points)
        return Response(serializer.data)
    except LoyaltyPoints.DoesNotExist:
        return Response(
            {'error': 'Loyalty points not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_pricing_rates(request):
    pricing_rates = PricingRate.objects.all()
    serializer = PricingRateSerializer(pricing_rates, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_pricing_rate(request):
    serializer = PricingRateSerializer(data=request.data)
    if serializer.is_valid():
        pricing_rate = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_pricing_rate(request, pk):
    try:
        pricing_rate = PricingRate.objects.get(pk=pk)
    except PricingRate.DoesNotExist:
        return Response({'error': 'PricingRate not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = PricingRateSerializer(pricing_rate, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_pricing_rate(request, pk):
    try:
        pricing_rate = PricingRate.objects.get(pk=pk)
        pricing_rate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except PricingRate.DoesNotExist:
        return Response({'error': 'PricingRate not found'}, status=status.HTTP_404_NOT_FOUND)
    


def verify_guest_ownership(ticket, request_data):
    """
    Verify ticket ownership using guest credentials
    """
    guest_email = request_data.get('guest_email')
    guest_phone = request_data.get('guest_phone')
    
    if not (guest_email or guest_phone):
        raise ValidationError('Either guest email or phone number is required for verification')
    
    # Check if the provided credentials match the ticket
    if guest_email and ticket.guest_email != guest_email:
        raise ValidationError('Invalid guest email')
    if guest_phone and ticket.guest_phone != guest_phone:
        raise ValidationError('Invalid guest phone')
    
    return True

@api_view(['PUT'])
@permission_classes([AllowAny])
def update_guest_ticket(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        
        # Verify this is a guest ticket
        if ticket.user is not None:
            return Response(
                {'error': 'This is not a guest ticket'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify ownership
        try:
            verify_guest_ownership(ticket, request.data)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        
        # Prevent changing guest credentials or adding user
        update_data = request.data.copy()
        if 'guest_email' in update_data:
            del update_data['guest_email']
        if 'guest_phone' in update_data:
            del update_data['guest_phone']
        if 'user' in update_data:
            del update_data['user']
        
        serializer = TicketSerializer(ticket, data=update_data, partial=True)
        if serializer.is_valid():
            ticket = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Ticket.DoesNotExist:
        return Response(
            {'error': 'Ticket not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_guest_ticket(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        
        # Verify this is a guest ticket
        if ticket.user is not None:
            return Response(
                {'error': 'This is not a guest ticket'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify ownership
        try:
            verify_guest_ownership(ticket, request.data)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    except Ticket.DoesNotExist:
        return Response(
            {'error': 'Ticket not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def get_guest_ticket(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        
        # Verify this is a guest ticket
        if ticket.user is not None:
            return Response(
                {'error': 'This is not a guest ticket'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify ownership
        try:
            verify_guest_ownership(ticket, request.GET)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)
        
    except Ticket.DoesNotExist:
        return Response(
            {'error': 'Ticket not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
@api_view(['POST'])
@permission_classes([AllowAny])
def create_guest_ticket(request):
    # Validate required guest information
    if not request.data.get('guest_email') and not request.data.get('guest_phone'):
        return Response(
            {'error': 'Either guest email or phone number is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate vehicle registration number
    if not request.data.get('assigned_to'):
        return Response(
            {'error': 'Vehicle registration number is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check for existing active tickets
    assigned_to = request.data.get('assigned_to')
    active_tickets = Ticket.objects.filter(
        assigned_to=assigned_to,
        status__in=['Unpaid', 'Payment_In_Progress']
    )
    
    if active_tickets.exists():
        return Response({
            'error': 'An active ticket already exists for this vehicle.',
            'code': 'active_ticket_exists'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Ensure no user ID is passed for guest tickets
    if 'user' in request.data:
        request.data.pop('user')

    serializer = TicketSerializer(data=request.data)
    if serializer.is_valid():
        ticket = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment(request):
    # Check if payment already exists for the ticket
    ticket_id = request.data.get('ticket')
    if Payment.objects.filter(ticket_id=ticket_id).exists():
        return Response(
            {'error': 'Payment already exists for this ticket'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        
        # Calculate amount if end_time is available
        if ticket.end_time:
            duration = ticket.end_time - ticket.start_time
            hours = duration.total_seconds() / 3600
            # Round up to nearest hour
            hours = Decimal(str(round(hours + 0.49)))
            amount = ticket.rate.rate * hours
            request.data['amount'] = amount
        
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Ticket.DoesNotExist:
        return Response(
            {'error': 'Ticket not found'},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_payments(request):
    payments = Payment.objects.all()
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_payment_by_id(request, payment_id):
    try:
        payment = Payment.objects.get(id=payment_id)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)
    except Payment.DoesNotExist:
        return Response(
            {'error': 'Payment not found'},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_payment_by_id(request, payment_id):
    try:
        payment = Payment.objects.get(id=payment_id)
        
        # Prevent updating amount directly
        if 'amount' in request.data:
            return Response(
                {'error': 'Amount cannot be modified directly'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        serializer = PaymentSerializer(payment, data=request.data, partial=True)
        if serializer.is_valid():
            payment = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Payment.DoesNotExist:
        return Response(
            {'error': 'Payment not found'},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_payment_by_id(request, payment_id):
    try:
        payment = Payment.objects.get(id=payment_id)
        payment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Payment.DoesNotExist:
        return Response(
            {'error': 'Payment not found'},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_payment(request, payment_id):
    try:
        payment = Payment.objects.get(id=payment_id)
        
        if payment.payment_status == 'Completed':
            return Response(
                {'error': 'Payment is already completed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payment.payment_status = 'Completed'
        payment.payment_date = timezone.now().date()
        payment.payment_time = timezone.now().time()
        payment.save()
        
        # Update ticket status
        ticket = payment.ticket
        ticket.status = 'Paid'
        ticket.save()
        
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)
        
    except Payment.DoesNotExist:
        return Response(
            {'error': 'Payment not found'},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_pending_payments(request):
    pending_payments = Payment.objects.filter(payment_status='Pending')
    serializer = PaymentSerializer(pending_payments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_guest_payment(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        
        # Verify this is a guest ticket
        if ticket.user is not None:
            return Response(
                {'error': 'This is not a guest ticket'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify ownership using the helper function from your code
        try:
            verify_guest_ownership(ticket, request.GET)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        
        # Get associated payment
        try:
            payment = Payment.objects.get(ticket=ticket)
            serializer = PaymentSerializer(payment)
            return Response(serializer.data)
        except Payment.DoesNotExist:
            return Response(
                {'error': 'No payment found for this ticket'},
                status=status.HTTP_404_NOT_FOUND
            )
            
    except Ticket.DoesNotExist:
        return Response(
            {'error': 'Ticket not found'},
            status=status.HTTP_404_NOT_FOUND
        )
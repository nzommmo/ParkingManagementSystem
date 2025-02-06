from django.urls import path
from . import views

urlpatterns = [

    path('users/', views.get_all_users, name='get_all_users'),  # Get all users
    path('user/<int:user_id>/', views.get_user_by_id, name='get_user_by_id'),  # Get user by ID
    path('user/<int:user_id>/update/', views.update_user_by_id, name='update_user_by_id'),  # Update user by ID
    path('user/<int:user_id>/delete/', views.delete_user_by_id, name='delete_user_by_id'),  # Delete user by ID
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('loyalty_points/', views.get_loyalty_points, name='loyalty-points'),
    path('pricing-rates/', views.get_pricing_rates, name='get_pricing_rates'),
    path('pricing-rates/create/', views.create_pricing_rate, name='create_pricing_rate'),
    path('pricing-rates/<int:pk>/update/', views.update_pricing_rate, name='update_pricing_rate'),
    path('pricing-rates/<int:pk>/delete/', views.delete_pricing_rate, name='delete_pricing_rate'),
    path('tickets/create/', views.create_ticket, name='create_ticket'),
    path('tickets/', views.get_all_tickets, name='get_all_tickets'),
    path('tickets/<int:ticket_id>', views.get_ticket_by_id),
    path('tickets/<int:ticket_id>/update', views.update_ticket_by_id),
    path('tickets/<int:ticket_id>/delete', views.delete_ticket_by_id),
    path('tickets/guest/', views.create_guest_ticket, name='create-guest-ticket'),
    path('tickets/guest/<int:ticket_id>/', views.get_guest_ticket, name='get-guest-ticket'),
    path('tickets/guest/<int:ticket_id>/update/', views.update_guest_ticket, name='update-guest-ticket'),
    path('tickets/guest/<int:ticket_id>/delete/', views.delete_guest_ticket, name='delete-guest-ticket'),
    path('payments/user/create/', views.create_user_payment, name='create-user-payment'),
    path('payments/user/', views.get_user_payments, name='get-user-payments'),
    path('payments/user/<int:payment_id>/', views.get_user_payment_details, name='get-user-payment-details'),
    path('payments/user/<int:payment_id>/update/', views.update_user_payment, name='update-user-payment'),
    path('payments/user/<int:payment_id>/delete/', views.delete_user_payment, name='delete-user-payment'),
    path('payments/guest/create/', views.create_guest_payment, name='create-guest-payment'),
    path('payments/guest/ticket/<int:ticket_id>/', views.get_guest_payment_details, name='get-guest-payment'),
    # path('payments/guest/<int:payment_id>/', views.get_guest_payment_by_id, name='get-guest-payment-details'),
    path('payments/guest/<int:payment_id>/update/', views.update_guest_payment, name='update-guest-payment'),
    path('payments/guest/<int:payment_id>/delete/', views.delete_guest_payment, name='delete-guest-payment'),
    path('payments/<int:payment_id>/complete/', views.complete_payment, name='complete-payment'),
    path('payments/user/all/', views.get_all_user_payments, name='get-all-user-payments'),
    path('payments/guest/all/', views.get_all_guest_payments, name='get-all-guest-payments'),
    path('payments/all/', views.get_all_payments, name='get-all-payments'),

]
   

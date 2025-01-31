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
]
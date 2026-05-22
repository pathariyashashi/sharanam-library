from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('entry/', views.mark_entry, name='entry'),
    path('exit/', views.mark_exit, name='exit'),
    path('gallery/', views.gallery, name='gallery'),
    path('about/', views.about, name='about'),
    path('address/', views.address, name='address'),
    path('updates/', views.updates, name='updates'),
    path('rules/',views.rules, name='rules'),
    path('attendance-history/', views.attendance_history, name='attendance_history'),
    path('seat-booking/', views.seat_booking, name='seat_booking'),
    path('payment/', views.payment, name='payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('download-receipt/', views.download_receipt, name='download_receipt'),
]
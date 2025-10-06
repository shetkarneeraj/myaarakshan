from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('notifications/', views.notifications, name='notifications'),
    path('premium/', views.premium_services, name='premium_services'),
    path('purchase/<str:service_name>/', views.purchase_service, name='purchase_service'),
    path('process-payment/', views.process_payment, name='process_payment'),
    
    # API endpoints
    path('api/v1/login/', views.api_login, name='api_login'),
    path('api/v1/notifications/<int:user_id>/', views.api_user_notifications, name='api_user_notifications'),
]

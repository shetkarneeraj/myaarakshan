from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('submit/', views.submit_application, name='submit_application'),
    path('track/<str:app_number>/', views.track_application, name='track_application'),
    path('track/', views.public_track, name='public_track'),
    
    # API endpoints
    path('api/v1/applications/<int:user_id>/', views.api_user_applications, name='api_user_applications'),
    path('api/v1/track/<str:app_number>/', views.api_track_application, name='api_track_application'),
]

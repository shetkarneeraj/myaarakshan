from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import datetime, timedelta
import random

from .models import Application, StatusUpdate
from accounts.models import User, Notification
from core.models import Division


@login_required
def submit_application(request):
    """Submit application form"""
    if request.method == 'POST':
        try:
            # Generate unique application number
            app_number = f"MR{datetime.now().year}{random.randint(100000, 999999)}"
            
            user = request.user
            
            # Calculate estimated completion based on subscription
            days_to_complete = 120  # Default 4 months
            if user.subscription_type == 'premium':
                days_to_complete = 60  # 2 months for premium
            elif user.subscription_type == 'pro':
                days_to_complete = 30  # 1 month for pro
            
            application = Application.objects.create(
                application_number=app_number,
                user=user,
                applicant_name=request.POST['applicant_name'],
                applicant_surname=request.POST['applicant_surname'],
                birth_year=int(request.POST['birth_year']) if request.POST['birth_year'] else None,
                village_id=int(request.POST['village_id']),
                contact_number=request.POST.get('contact_number', ''),
                priority='premium' if user.subscription_type != 'free' else 'normal',
                estimated_completion=timezone.now() + timedelta(days=days_to_complete)
            )
            
            # Create initial status update
            StatusUpdate.objects.create(
                application=application,
                stage='gram_committee',
                status='submitted',
                message='अर्ज यशस्वीरित्या सबमिट झाला आहे',
                updated_by='System'
            )
            
            # Create notification
            Notification.objects.create(
                user=user,
                title='अर्ज सबमिट झाला',
                message=f'तुमचा अर्ज क्रमांक {app_number} यशस्वीरित्या सबमिट झाला आहे',
                notification_type='success'
            )
            
            messages.success(request, f'अर्ज यशस्वीरित्या सबमिट झाला! अर्ज क्रमांक: {app_number}')
            return redirect('applications:track_application', app_number=app_number)
            
        except Exception as e:
            messages.error(request, 'अर्ज सबमिट करताना एरर आली')
    
    divisions = Division.objects.all()
    return render(request, 'user/submit_application.html', {'divisions': divisions})


def track_application(request, app_number):
    """Track application status"""
    application = get_object_or_404(Application, application_number=app_number)
    
    # Check if user owns this application or allow public tracking
    if request.user.is_authenticated and application.user != request.user:
        messages.error(request, 'तुम्ही फक्त तुमच्या स्वतःच्या अर्जाची स्थिती पाहू शकता')
        return redirect('accounts:dashboard')
    
    status_updates = StatusUpdate.objects.filter(application=application).order_by('date_updated')
    
    return render(request, 'user/track_application.html', {
        'application': application,
        'status_updates': status_updates
    })


def public_track(request):
    """Public application tracking"""
    if request.method == 'POST':
        app_number = request.POST['application_number']
        phone = request.POST['phone']
        
        try:
            application = Application.objects.get(application_number=app_number, contact_number=phone)
            return redirect('applications:track_application', app_number=app_number)
        except Application.DoesNotExist:
            messages.error(request, 'अर्ज क्रमांक किंवा फोन नंबर चुकीचा आहे')
    
    return render(request, 'user/public_track.html')


# API Views
def api_user_applications(request, user_id):
    """API to get user applications"""
    try:
        applications = Application.objects.filter(user_id=user_id)
        
        apps_data = []
        for app in applications:
            apps_data.append({
                'application_number': app.application_number,
                'status': app.status,
                'current_stage': app.current_stage,
                'progress_percentage': app.progress_percentage,
                'date_submitted': app.date_submitted.isoformat(),
                'estimated_completion': app.estimated_completion.isoformat() if app.estimated_completion else None
            })
        
        return JsonResponse({'success': True, 'applications': apps_data})
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': 'Server error'}, status=500)


def api_track_application(request, app_number):
    """API to track application"""
    try:
        application = get_object_or_404(Application, application_number=app_number)
        status_updates = StatusUpdate.objects.filter(application=application).order_by('date_updated')
        
        updates_data = []
        for update in status_updates:
            updates_data.append({
                'stage': update.stage,
                'status': update.status,
                'message': update.message,
                'date_updated': update.date_updated.isoformat(),
                'updated_by': update.updated_by
            })
        
        app_data = {
            'application_number': application.application_number,
            'status': application.status,
            'current_stage': application.current_stage,
            'progress_percentage': application.progress_percentage,
            'date_submitted': application.date_submitted.isoformat(),
            'estimated_completion': application.estimated_completion.isoformat() if application.estimated_completion else None,
            'status_updates': updates_data
        }
        
        return JsonResponse({'success': True, 'application': app_data})
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': 'Server error'}, status=500)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import datetime, timedelta
import json
import random

from .models import User, Notification, Payment, PremiumService
from core.models import Division
from applications.models import Application


def register(request):
    """User registration"""
    if request.method == 'POST':
        try:
            # Check if user already exists
            if User.objects.filter(email=request.POST['email']).exists():
                messages.error(request, 'या ईमेल पत्त्याने खाते आधीच आहे')
                return redirect('accounts:register')
            
            # Create new user
            user = User.objects.create_user(
                username=request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password'],
                full_name=request.POST['full_name'],
                phone=request.POST.get('phone', ''),
            )
            
            if request.POST.get('village_id'):
                user.village_id = int(request.POST['village_id'])
                user.save()
            
            # Create welcome notification
            Notification.objects.create(
                user=user,
                title='स्वागत आहे!',
                message=f'नमस्कार {user.full_name}, मराठा आरक्षण मंचमध्ये तुमचे स्वागत आहे!',
                notification_type='success'
            )
            
            messages.success(request, 'खाते यशस्वीरित्या तयार झाले! आता लॉगिन करा')
            return redirect('accounts:login')
            
        except Exception as e:
            messages.error(request, 'खाते तयार करताना एरर आली')
    
    divisions = Division.objects.all()
    return render(request, 'auth/register.html', {'divisions': divisions})


def user_login(request):
    """User login"""
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                auth_login(request, user)
                user.last_login = timezone.now()
                user.save()
                
                messages.success(request, f'स्वागत आहे, {user.full_name}!')
                return redirect('accounts:dashboard')
            else:
                messages.error(request, 'चुकीचा ईमेल किंवा पासवर्ड')
        except User.DoesNotExist:
            messages.error(request, 'चुकीचा ईमेल किंवा पासवर्ड')
    
    return render(request, 'auth/login.html')


def user_logout(request):
    """User logout"""
    auth_logout(request)
    messages.info(request, 'तुम्ही लॉग आउट झाला आहात')
    return redirect('core:home')


@login_required
def dashboard(request):
    """User dashboard"""
    user = request.user
    applications = Application.objects.filter(user=user).order_by('-date_submitted')
    notifications = Notification.objects.filter(user=user, is_read=False).order_by('-date_created')[:5]
    
    return render(request, 'user/dashboard.html', {
        'user': user,
        'applications': applications,
        'notifications': notifications
    })


@login_required
def profile(request):
    """User profile"""
    return render(request, 'user/profile.html', {'user': request.user})


@login_required
def notifications(request):
    """User notifications"""
    user_notifications = Notification.objects.filter(user=request.user).order_by('-date_created')
    
    # Mark as read
    user_notifications.filter(is_read=False).update(is_read=True)
    
    return render(request, 'user/notifications.html', {'notifications': user_notifications})


def premium_services(request):
    """Premium services page"""
    services = [
        {
            'name': 'प्रीमियम सब्स्क्रिप्शन',
            'price': 499,
            'duration': '6 महिने',
            'features': ['प्राधान्य प्रक्रिया', 'SMS अपडेट्स', 'डेडिकेटेड सपोर्ट', '24/7 हेल्पलाइन']
        },
        {
            'name': 'प्रो सब्स्क्रिप्शन',
            'price': 999,
            'duration': '1 वर्ष',
            'features': ['जलद प्रक्रिया', 'SMS + Email अपडेट्स', 'व्यक्तिगत सल्लागार', 'डॉक्युमेंट रिव्यू']
        },
        {
            'name': 'तत्काळ प्रक्रिया',
            'price': 1999,
            'duration': 'एकवेळ',
            'features': ['30 दिवसांत प्रक्रिया', 'प्राधान्य हाताळणी', 'डेडिकेटेड केस मॅनेजर']
        }
    ]
    
    user_subscription = None
    if request.user.is_authenticated:
        user_subscription = request.user.subscription_type
    
    return render(request, 'premium/services.html', {
        'services': services,
        'user_subscription': user_subscription
    })


@login_required
def purchase_service(request, service_name):
    """Purchase service page"""
    service_prices = {
        'premium': 499,
        'pro': 999,
        'express': 1999
    }
    
    if service_name not in service_prices:
        messages.error(request, 'अवैध सेवा')
        return redirect('accounts:premium_services')
    
    return render(request, 'premium/payment.html', {
        'service': service_name,
        'price': service_prices[service_name]
    })


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def process_payment(request):
    """Process payment"""
    try:
        data = json.loads(request.body)
        
        # Generate transaction ID
        transaction_id = f"TXN{datetime.now().strftime('%Y%m%d')}{random.randint(10000, 99999)}"
        
        payment = Payment.objects.create(
            user=request.user,
            transaction_id=transaction_id,
            amount=float(data['amount']),
            service=data['service'],
            payment_method=data['payment_method'],
            status='success'  # In real implementation, this would be processed
        )
        
        # Update user subscription
        if data['service'] in ['premium', 'pro']:
            request.user.subscription_type = data['service']
            request.user.save()
        
        # Create notification
        Notification.objects.create(
            user=request.user,
            title='पेमेंट यशस्वी',
            message=f'तुमचा पेमेंट ₹{payment.amount} यशस्वीरित्या प्रक्रिया झाला. Transaction ID: {transaction_id}',
            notification_type='success'
        )
        
        return JsonResponse({'success': True, 'transaction_id': transaction_id})
        
    except Exception as e:
        return JsonResponse({'error': 'Payment failed'}, status=500)


# API Endpoints for mobile app
@csrf_exempt
@require_http_methods(["POST"])
def api_login(request):
    """API login endpoint"""
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                user.last_login = timezone.now()
                user.save()
                
                return JsonResponse({
                    'success': True,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'full_name': user.full_name,
                        'subscription_type': user.subscription_type
                    },
                    'token': f"token_{user.id}_{datetime.now().timestamp()}"  # Simple token for demo
                })
            else:
                return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=401)
            
    except Exception as e:
        return JsonResponse({'success': False, 'message': 'Server error'}, status=500)


def api_user_notifications(request, user_id):
    """API to get user notifications"""
    try:
        notifications = Notification.objects.filter(user_id=user_id).order_by('-date_created')[:20]
        
        notif_data = []
        for notif in notifications:
            notif_data.append({
                'id': notif.id,
                'title': notif.title,
                'message': notif.message,
                'notification_type': notif.notification_type,
                'is_read': notif.is_read,
                'date_created': notif.date_created.isoformat()
            })
        
        return JsonResponse({'success': True, 'notifications': notif_data})
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': 'Server error'}, status=500)
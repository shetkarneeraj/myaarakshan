from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from core.models import Village


class User(AbstractUser):
    SUBSCRIPTION_CHOICES = [
        ('free', 'फ्री'),
        ('premium', 'प्रीमियम'),
        ('pro', 'प्रो'),
    ]
    
    full_name = models.CharField(max_length=100, verbose_name="पूर्ण नाव")
    phone = models.CharField(max_length=15, blank=True, verbose_name="फोन नंबर")
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="गाव")
    subscription_type = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES, default='free', verbose_name="सदस्यता प्रकार")
    email_verified = models.BooleanField(default=False, verbose_name="ईमेल सत्यापित")
    
    class Meta:
        verbose_name = "वापरकर्ता"
        verbose_name_plural = "वापरकर्ते"
        db_table = "user"
    
    def __str__(self):
        return f"{self.full_name} ({self.username})"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('info', 'माहिती'),
        ('success', 'यश'),
        ('warning', 'चेतावणी'),
        ('error', 'त्रुटी'),
    ]
    
    CHANNEL_CHOICES = [
        ('web', 'वेब'),
        ('email', 'ईमेल'),
        ('sms', 'SMS'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name="वापरकर्ता")
    title = models.CharField(max_length=200, verbose_name="शीर्षक")
    message = models.TextField(verbose_name="संदेश")
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='info', verbose_name="प्रकार")
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default='web', verbose_name="चॅनेल")
    is_read = models.BooleanField(default=False, verbose_name="वाचले")
    date_created = models.DateTimeField(default=timezone.now, verbose_name="तयार केले")
    date_sent = models.DateTimeField(null=True, blank=True, verbose_name="पाठवले")
    
    class Meta:
        verbose_name = "सूचना"
        verbose_name_plural = "सूचना"
        db_table = "notification"
        ordering = ['-date_created']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"


class Payment(models.Model):
    PAYMENT_STATUSES = [
        ('pending', 'प्रलंबित'),
        ('success', 'यशस्वी'),
        ('failed', 'अयशस्वी'),
        ('refunded', 'परतावा'),
    ]
    
    PAYMENT_METHODS = [
        ('upi', 'UPI'),
        ('card', 'कार्ड'),
        ('netbanking', 'नेट बँकिंग'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments', verbose_name="वापरकर्ता")
    transaction_id = models.CharField(max_length=50, unique=True, verbose_name="व्यवहार आयडी")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="रक्कम")
    service = models.CharField(max_length=50, verbose_name="सेवा")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, verbose_name="पेमेंट पद्धत")
    status = models.CharField(max_length=20, choices=PAYMENT_STATUSES, default='pending', verbose_name="स्थिती")
    date_created = models.DateTimeField(default=timezone.now, verbose_name="तयार केले")
    date_processed = models.DateTimeField(null=True, blank=True, verbose_name="प्रक्रिया केली")
    
    class Meta:
        verbose_name = "पेमेंट"
        verbose_name_plural = "पेमेंट्स"
        db_table = "payment"
        ordering = ['-date_created']
    
    def __str__(self):
        return f"{self.transaction_id} - ₹{self.amount}"


class PremiumService(models.Model):
    name = models.CharField(max_length=100, verbose_name="सेवेचे नाव")
    description = models.TextField(verbose_name="वर्णन")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="किंमत")
    duration_days = models.IntegerField(verbose_name="कालावधी (दिवस)")
    features = models.TextField(verbose_name="वैशिष्ट्ये")  # JSON string of features
    is_active = models.BooleanField(default=True, verbose_name="सक्रिय")
    
    class Meta:
        verbose_name = "प्रीमियम सेवा"
        verbose_name_plural = "प्रीमियम सेवा"
        db_table = "premium_service"
    
    def __str__(self):
        return self.name
from django.db import models
from django.utils import timezone
from accounts.models import User
from core.models import Village


class Application(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'सबमिट केले'),
        ('under_review', 'तपासणी'),
        ('approved', 'मंजूर'),
        ('rejected', 'नाकारले'),
    ]
    
    PRIORITY_CHOICES = [
        ('normal', 'सामान्य'),
        ('high', 'उच्च'),
        ('premium', 'प्रीमियम'),
    ]
    
    STAGE_CHOICES = [
        ('gram_committee', 'ग्राम समिती'),
        ('taluka_committee', 'तालुका समिती'),
        ('scrutiny_committee', 'छाननी समिती'),
        ('final_approval', 'अंतिम मंजुरी'),
    ]
    
    application_number = models.CharField(max_length=20, unique=True, verbose_name="अर्ज क्रमांक")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications', verbose_name="वापरकर्ता")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted', verbose_name="स्थिती")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal', verbose_name="प्राधान्य")
    
    # Application Details
    applicant_name = models.CharField(max_length=100, verbose_name="अर्जदाराचे नाव")
    applicant_surname = models.CharField(max_length=50, verbose_name="आडनाव")
    birth_year = models.IntegerField(null=True, blank=True, verbose_name="जन्म वर्ष")
    village = models.ForeignKey(Village, on_delete=models.CASCADE, verbose_name="गाव")
    contact_number = models.CharField(max_length=15, blank=True, verbose_name="संपर्क क्रमांक")
    
    # Timestamps
    date_submitted = models.DateTimeField(default=timezone.now, verbose_name="सबमिट दिनांक")
    estimated_completion = models.DateTimeField(null=True, blank=True, verbose_name="अंदाजित पूर्णता")
    actual_completion = models.DateTimeField(null=True, blank=True, verbose_name="वास्तविक पूर्णता")
    
    # Progress tracking
    current_stage = models.CharField(max_length=50, choices=STAGE_CHOICES, default='gram_committee', verbose_name="सध्याचा टप्पा")
    progress_percentage = models.IntegerField(default=20, verbose_name="प्रगती टक्केवारी")
    
    class Meta:
        verbose_name = "अर्ज"
        verbose_name_plural = "अर्ज"
        db_table = "application"
        ordering = ['-date_submitted']
    
    def __str__(self):
        return f"{self.application_number} - {self.applicant_name} {self.applicant_surname}"


class StatusUpdate(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='status_updates', verbose_name="अर्ज")
    stage = models.CharField(max_length=50, verbose_name="टप्पा")
    status = models.CharField(max_length=20, verbose_name="स्थिती")
    message = models.TextField(null=True, blank=True, verbose_name="संदेश")
    updated_by = models.CharField(max_length=100, null=True, blank=True, verbose_name="अपडेट करणारा")
    date_updated = models.DateTimeField(default=timezone.now, verbose_name="अपडेट दिनांक")
    
    class Meta:
        verbose_name = "स्थिती अपडेट"
        verbose_name_plural = "स्थिती अपडेट्स"
        db_table = "status_update"
        ordering = ['-date_updated']
    
    def __str__(self):
        return f"{self.application.application_number} - {self.stage}"
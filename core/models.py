from django.db import models
from django.utils import timezone


class Division(models.Model):
    name = models.CharField(max_length=100, verbose_name="विभागाचे नाव")
    
    class Meta:
        verbose_name = "विभाग"
        verbose_name_plural = "विभाग"
        db_table = "division"
    
    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100, verbose_name="जिल्ह्याचे नाव")
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='districts', verbose_name="विभाग")
    
    class Meta:
        verbose_name = "जिल्हा"
        verbose_name_plural = "जिल्हे"
        db_table = "district"
    
    def __str__(self):
        return f"{self.name}, {self.division.name}"


class Village(models.Model):
    name = models.CharField(max_length=100, verbose_name="गावाचे नाव")
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='villages', verbose_name="जिल्हा")
    
    class Meta:
        verbose_name = "गाव"
        verbose_name_plural = "गावे"
        db_table = "village"
    
    def __str__(self):
        return f"{self.name}, {self.district.name}"


class Person(models.Model):
    name = models.CharField(max_length=100, verbose_name="नाव")
    surname = models.CharField(max_length=50, verbose_name="आडनाव")
    birth_year = models.IntegerField(null=True, blank=True, verbose_name="जन्म वर्ष")
    reservation_number = models.CharField(max_length=50, unique=True, verbose_name="आरक्षण क्रमांक")
    village = models.ForeignKey(Village, on_delete=models.CASCADE, related_name='people', verbose_name="गाव")
    contact_number = models.CharField(max_length=15, blank=True, verbose_name="संपर्क क्रमांक")
    date_added = models.DateTimeField(default=timezone.now, verbose_name="जोडलेला दिनांक")
    is_verified = models.BooleanField(default=False, verbose_name="सत्यापित")
    
    class Meta:
        verbose_name = "व्यक्ती"
        verbose_name_plural = "लोक"
        db_table = "person"
        ordering = ['-date_added']
    
    def __str__(self):
        return f"{self.name} {self.surname} - {self.village.name}"
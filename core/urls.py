from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('division/<int:division_id>/', views.view_division, name='view_division'),
    path('district/<int:district_id>/', views.view_district, name='view_district'),
    path('village/<int:village_id>/', views.view_village, name='view_village'),
    path('search/', views.search, name='search'),
    path('submit-details/', views.submit_details, name='submit_details'),
    path('submit-person/', views.submit_person, name='submit_person'),
    
    # API endpoints
    path('api/districts/<int:division_id>/', views.get_districts_api, name='api_districts'),
    path('api/villages/<int:district_id>/', views.get_villages_api, name='api_villages'),
    
    # Static pages
    path('guide/', views.guide, name='guide'),
    path('flowchart/', views.flowchart, name='flowchart'),
    path('eligibility-check/', views.eligibility_check, name='eligibility_check'),
    path('check-eligibility/', views.check_eligibility, name='check_eligibility'),
    path('documents/', views.documents, name='documents'),
    path('file-preparation/', views.file_preparation, name='file_preparation'),
    path('contact/', views.contact, name='contact'),
    path('documents-explained/', views.documents_explained, name='documents_explained'),
    path('district-wise-records/', views.district_wise_records, name='district_wise_records'),
    path('pre1967-records/', views.pre1967_records, name='pre1967_records'),
    path('phases/', views.phases, name='phases'),
    path('faq/', views.faq, name='faq'),
    path('nearest-office/', views.nearest_office, name='nearest_office'),
    path('testimonials/', views.testimonials, name='testimonials'),
]

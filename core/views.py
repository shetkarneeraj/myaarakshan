from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.core.paginator import Paginator
import json

from .models import Division, District, Village, Person
from news.models import News


def home(request):
    """Home page view"""
    latest_news = News.objects.filter(is_featured=True).order_by('-date_posted')[:3]
    divisions = Division.objects.all()
    return render(request, 'index.html', {
        'news': latest_news,
        'divisions': divisions
    })


def view_division(request, division_id):
    """Division view"""
    division = get_object_or_404(Division, id=division_id)
    districts = District.objects.filter(division=division)
    return render(request, 'division.html', {
        'division': division,
        'districts': districts
    })


def view_district(request, district_id):
    """District view"""
    district = get_object_or_404(District, id=district_id)
    villages = Village.objects.filter(district=district)
    return render(request, 'district.html', {
        'district': district,
        'villages': villages
    })


def view_village(request, village_id):
    """Village view"""
    village = get_object_or_404(Village, id=village_id)
    people = Person.objects.filter(village=village, is_verified=True)
    return render(request, 'village.html', {
        'village': village,
        'people': people
    })


def search(request):
    """Search for people"""
    query = request.GET.get('q', '')
    village_name = request.GET.get('village', '')
    surname = request.GET.get('surname', '')
    
    results = []
    if query or village_name or surname:
        people_query = Person.objects.filter(is_verified=True)
        
        if query:
            people_query = people_query.filter(
                Q(name__icontains=query) | Q(surname__icontains=query)
            )
        
        if village_name:
            people_query = people_query.filter(village__name__icontains=village_name)
        
        if surname:
            people_query = people_query.filter(surname__icontains=surname)
        
        results = people_query.select_related('village__district')
    
    return render(request, 'search.html', {
        'results': results,
        'query': query,
        'village_name': village_name,
        'surname': surname
    })


def submit_details(request):
    """Submit person details form"""
    divisions = Division.objects.all()
    return render(request, 'submit_details.html', {'divisions': divisions})


@require_http_methods(["POST"])
@csrf_exempt
def submit_person(request):
    """Submit person details"""
    try:
        person = Person.objects.create(
            name=request.POST['name'],
            surname=request.POST['surname'],
            birth_year=int(request.POST['birth_year']) if request.POST['birth_year'] else None,
            reservation_number=request.POST['reservation_number'],
            village_id=int(request.POST['village_id']),
            contact_number=request.POST.get('contact_number', '')
        )
        messages.success(request, 'तुमची माहिती यशस्वीरित्या सबमिट झाली आहे. वेरिफिकेशननंतर ती दिसेल.')
    except Exception as e:
        messages.error(request, 'एरर आली आहे. कृपया पुन्हा प्रयत्न करा.')
    
    return redirect('core:submit_details')


# API Views
def get_districts_api(request, division_id):
    """API to get districts by division"""
    districts = District.objects.filter(division_id=division_id)
    return JsonResponse([{'id': d.id, 'name': d.name} for d in districts], safe=False)


def get_villages_api(request, district_id):
    """API to get villages by district"""
    villages = Village.objects.filter(district_id=district_id)
    return JsonResponse([{'id': v.id, 'name': v.name} for v in villages], safe=False)


# Static Page Views
def guide(request):
    """Guide page"""
    return render(request, 'guide.html')


def flowchart(request):
    """Flowchart page"""
    return render(request, 'flowchart.html')


def eligibility_check(request):
    """Eligibility check page with server-side processing"""
    if request.method == 'POST':
        # Read form fields
        residence_proof = request.POST.get('residence_proof')
        kunbi_relatives = request.POST.get('kunbi_relatives')
        land_records = request.POST.get('land_records')
        school_records = request.POST.get('school_records')
        caste_records = request.POST.get('caste_records')
        gazette_record = request.POST.get('gazette_record')

        # Validation: all questions answered
        missing = [
            f for f, v in [
                ('residence_proof', residence_proof),
                ('kunbi_relatives', kunbi_relatives),
                ('land_records', land_records),
                ('school_records', school_records),
                ('caste_records', caste_records),
                ('gazette_record', gazette_record),
            ] if not v
        ]

        if missing:
            return render(request, 'eligibility_check.html', {
                'error': 'कृपया सर्व प्रश्नांची उत्तरे द्या',
                'form_values': request.POST,
            })

        # Apply eligibility logic (same as client-side)
        reasons = []
        eligible = True

        if residence_proof != 'yes':
            eligible = False
            reasons.append('१३ ऑक्टोबर १९६७ पूर्वीचा वास्तव्य पुरावा अनिवार्य आहे')

        if caste_records == 'maratha':
            eligible = False
            reasons.append('फक्त "मराठा" जात पुरेशी नाही - "कुणबी" उल्लेख आवश्यक')
        elif caste_records == 'other':
            eligible = False
            reasons.append('कागदपत्रांमध्ये कुणबी/मराठा-कुणबी नमूद असणे आवश्यक')

        has_evidence = (
            kunbi_relatives == 'yes' or
            gazette_record == 'yes' or
            land_records == 'yes' or
            school_records == 'yes'
        )
        if not has_evidence:
            eligible = False
            reasons.append('कमीत कमी एक पुरावा आवश्यक: नातेवाईकांचे प्रमाणपत्र, गॅझेट नोंद, जमीन कागदपत्रे किंवा शाळा दाखले')

        if eligible:
            if kunbi_relatives == 'yes' or gazette_record == 'yes':
                reasons.append('तुमच्याकडे मजबूत पुरावे आहेत')
            else:
                reasons.append('अधिक मजबूत पुरावे (गॅझेट नोंद/नातेवाईकांचे प्रमाणपत्र) मिळवण्याचा प्रयत्न करा')

        return render(request, 'eligibility_check.html', {
            'result': {
                'eligible': eligible,
                'reasons': reasons,
            },
            'form_values': request.POST,
        })

    return render(request, 'eligibility_check.html')


@require_http_methods(["POST"])
@csrf_exempt
def check_eligibility(request):
    """Check eligibility API"""
    try:
        # Get form data
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
        
        residence_proof = data.get('residence_proof')
        kunbi_relatives = data.get('kunbi_relatives') 
        land_records = data.get('land_records')
        school_records = data.get('school_records')
        caste_records = data.get('caste_records')
        gazette_record = data.get('gazette_record')
        
        # Flowchart Logic:
        # 1. Must have residence proof before 1967
        if residence_proof != 'yes':
            return JsonResponse({
                'status': 'success',
                'eligible': False,
                'reasons': ['१३ ऑक्टोबर १९६७ पूर्वीचा वास्तव्य पुरावा अनिवार्य आहे']
            })
        
        # 2. Must have Kunbi in caste records
        if caste_records == 'maratha':
            return JsonResponse({
                'status': 'success',
                'eligible': False,
                'reasons': ['फक्त "मराठा" जात पुरेशी नाही - "कुणबी" उल्लेख आवश्यक']
            })
        elif caste_records == 'other':
            return JsonResponse({
                'status': 'success',
                'eligible': False,
                'reasons': ['कागदपत्रांमध्ये कुणबी/मराठा-कुणबी नमूद असणे आवश्यक']
            })
        
        # 3. Must have at least one evidence
        has_relatives = kunbi_relatives == 'yes'
        has_gazette = gazette_record == 'yes'
        has_land = land_records == 'yes'
        has_school = school_records == 'yes'
        
        if not (has_relatives or has_gazette or has_land or has_school):
            return JsonResponse({
                'status': 'success',
                'eligible': False,
                'reasons': ['कमीत कमी एक पुरावा आवश्यक: नातेवाईकांचे प्रमाणपत्र, गॅझेट नोंद, जमीन कागदपत्रे किंवा शाळा दाखले']
            })
        
        # All checks passed - eligible
        guidance = []
        if has_relatives or has_gazette:
            guidance.append('तुमच्याकडे मजबूत पुरावे आहेत')
        else:
            guidance.append('अधिक मजबूत पुरावे (गॅझेट नोंद/नातेवाईकांचे प्रमाणपत्र) मिळवण्याचा प्रयत्न करा')
            
        return JsonResponse({
            'status': 'success',
            'eligible': True,
            'reasons': guidance
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': 'Server error occurred'
        })


def documents(request):
    """Documents page"""
    documents = [
        {
            'title': 'GR - मराठा आरक्षण योजना',
            'description': 'नवीनतम सरकारी निर्णय',
            'type': 'PDF',
            'size': '2.5 MB',
            'url': '/static/docs/maratha_reservation_gr.pdf'
        },
        {
            'title': 'अर्ज फॉर्म',
            'description': 'कुणबी प्रमाणपत्रासाठी अर्ज',
            'type': 'PDF',
            'size': '1.2 MB',
            'url': '/static/docs/application_form.pdf'
        },
        {
            'title': 'आवश्यक कागदपत्रांची यादी',
            'description': 'सर्व आवश्यक दस्तऐवज',
            'type': 'PDF',
            'size': '800 KB',
            'url': '/static/docs/required_documents.pdf'
        }
    ]
    return render(request, 'documents.html', {'documents': documents})


def contact(request):
    """Contact page"""
    return render(request, 'contact.html')


def documents_explained(request):
    """Documents explained page"""
    return render(request, 'documents_explained.html')


def district_wise_records(request):
    """District wise records page"""
    districts = [
        {"name": "अकोला", "url": "https://akola.gov.in/en/kunbi-maratha-documents/"},
        {"name": "अमरावती", "url": "https://amravati.gov.in/en/kunbi-maratha-documents/"},
        {"name": "अहिल्यानगर", "url": "https://ahilyanagar.maharashtra.gov.in/en/kunbi-documents/"},
        {"name": "छत्रपती संभाजीनगर", "url": "https://aurangabad.gov.in/en/kunbi-maratha-documents/"},
        {"name": "बीड", "url": "https://beed.gov.in/?&s=कुणबी"},
        {"name": "भंडारा", "url": "https://bhandara.gov.in/mr/?&s=कुणबी"},
        {"name": "बुलढाणा", "url": "https://buldhana.nic.in/en/home-new-mr/kunbi-record"},
        {"name": "चंद्रपुर", "url": "https://chanda.nic.in/en/kunbi-records/"},
        {"name": "धुळे", "url": "https://dhule.gov.in/en/kunbi-documents/"},
        {"name": "धाराशिव", "url": "https://dharashiv.maharashtra.gov.in/kunbi-maratha-documents/"},
        {"name": "गडचिरोली", "url": "https://gadchiroli.gov.in/mr/?&s=कुणबी"},
        {"name": "गोंदिया", "url": "https://gondia.gov.in/en/kunbi-maratha-kunbi-kunbi-maratha-record/"},
        {"name": "हिंगोली", "url": "https://hingoli.nic.in/en/"},
        {"name": "जळगाव", "url": "https://jalgaon.gov.in/en/kunbi-maratha-documents/"},
        {"name": "जालना", "url": "https://jalna.gov.in/en/kunbi/"},
        {"name": "कोल्हापूर", "url": "https://kolhapur.gov.in/?&s=कुणबी"},
        {"name": "लातूर", "url": "https://latur.gov.in/mr/kunbhi/"},
        {"name": "मुंबई शहर", "url": "https://mumbaicity.gov.in/en/kunbi-maratha-recordes/"},
        {"name": "मुंबई उपनगर", "url": "https://mumbaisuburban.gov.in/en/kunbi-records/"},
        {"name": "नागपूर", "url": "https://nagpur.gov.in/mr/?&s=कुणबी"},
        {"name": "नांदेड", "url": "https://nanded.gov.in/?&s=कुणबी"},
        {"name": "नंदुरबार", "url": "https://nandurbar.gov.in/en/kunbi-record-found-in-revenue-records/"},
        {"name": "नाशिक", "url": "https://nashik.gov.in/en/documents/kunbi-maratha-documents-2024/"},
        {"name": "उस्मानाबाद", "url": "https://osmanabad.gov.in/en/kunbi-maratha-documents/"},
        {"name": "पालघर", "url": "https://palghar.gov.in/document-category/marathakunbi2024/"},
        {"name": "परभणी", "url": "https://parbhani.gov.in/mr/?&s=कुणबी"},
        {"name": "पुणे", "url": "https://pune.gov.in/en/kunbi-records-found-in-revenue-records/"},
        {"name": "रायगड", "url": "https://raigad.gov.in/?&s=कुणबी"},
        {"name": "रत्नागिरी", "url": "https://ratnagiri.gov.in/en/"},
        {"name": "सांगली", "url": "https://sangli.nic.in/kunabi-maratha-records/"},
        {"name": "सातारा", "url": "https://www.satara.gov.in/?&s=कुणबी"},
        {"name": "सिंधुदुर्ग", "url": "https://sindhudurg.nic.in/?&s=कुणबी"},
        {"name": "सोलापूर", "url": "https://solapur.gov.in/?&s=कुणबी"},
        {"name": "वर्धा", "url": "https://wardha.gov.in/?&s=कुणबी"},
        {"name": "वाशिम", "url": "https://washim.gov.in/?&s=कुणबी"},
        {"name": "यवतमाळ", "url": "https://yavatmal.gov.in/en/maratha-kunbi-records/"},
    ]
    return render(request, 'district_wise_records.html', {"districts": districts})


def pre1967_records(request):
    """Pre-1967 records page"""
    return render(request, 'pre1967_records.html')


def phases(request):
    """Phases page"""
    return render(request, 'phases.html')


def faq(request):
    """FAQ page"""
    faqs = [
        {
            'question': 'कुणबी प्रमाणपत्रासाठी कोण अर्ज करू शकतो?',
            'answer': 'कुणबी, मराठा-कुणबी किंवा कुणबी-मराठा जातीचे लोक अर्ज करू शकतात. त्यांच्याकडे १३ ऑक्टोबर १९६७ पूर्वीचा निवास दाखला असणे आवश्यक आहे.'
        },
        {
            'question': 'कोणती कागदपत्रे लागतात?',
            'answer': 'जन्म प्रमाणपत्र, ७/१२ उतारा, निवासी दाखला, नातेवाईकांचे कुणबी प्रमाणपत्र (असल्यास), शाळा दाखले आणि स्थानीय पुरावे.'
        },
        {
            'question': 'अर्ज कुठे द्यावा?',
            'answer': 'ग्रामस्तर समितीकडे अर्ज दाखल करावा. ग्राम महसूल अधिकारी, ग्रामपंचायत अधिकारी यांच्याकडे संपर्क साधा.'
        },
        {
            'question': 'प्रक्रियेला किती वेळ लागतो?',
            'answer': 'सामान्यतः ३०-९० दिवस लागतात. ग्राम समिती, तालुका समिती आणि Scrutiny Committee तपासणी केल्यानंतर निर्णय घेतला जातो.'
        }
    ]
    return render(request, 'faq.html', {'faqs': faqs})


def nearest_office(request):
    """Nearest office page"""
    offices = [
        {
            'name': 'औरंगाबाद जिल्हा कलेक्टर कार्यालय',
            'address': 'जिल्हा कलेक्टर कार्यालय, औरंगाबाद',
            'phone': '0240-2123456',
            'email': 'collector.aurangabad@maharashtra.gov.in',
            'hours': 'सकाळी १०:०० ते संध्याकाळी ५:००'
        },
        {
            'name': 'जालना जिल्हा कलेक्टर कार्यालय',
            'address': 'जिल्हा कलेक्टर कार्यालय, जालना',
            'phone': '02482-123456',
            'email': 'collector.jalna@maharashtra.gov.in',
            'hours': 'सकाळी १०:०० ते संध्याकाळी ५:००'
        }
    ]
    return render(request, 'nearest_office.html', {'offices': offices})


def file_preparation(request):
    """File preparation static page"""
    return render(request, 'file_preparation.html')


def testimonials(request):
    """Testimonials page"""
    testimonials_data = [
        {
            'name': 'राहुल पाटील',
            'village': 'पैठण, औरंगाबाद',
            'message': 'या वेबसाइटच्या मदतीने मला माझ्या गावातील लाभार्थी सापडले आणि मला आरक्षण मिळाले.',
            'rating': 5
        },
        {
            'name': 'सुनिता जाधव',
            'village': 'भोकरदन, जालना',
            'message': 'खूप सोपी प्रक्रिया आणि सर्व माहिती एकाच ठिकाणी मिळते.',
            'rating': 5
        }
    ]
    return render(request, 'testimonials.html', {'testimonials': testimonials_data})
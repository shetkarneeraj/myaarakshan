from django.core.management.base import BaseCommand
from core.models import Division, District, Village
from news.models import News


class Command(BaseCommand):
    help = 'Initialize database with sample data'
    
    def handle(self, *args, **options):
        # Create divisions and districts if they don't exist
        if Division.objects.count() == 0:
            self.stdout.write('Creating initial data...')
            
            # Add Aurangabad Division
            aurangabad_div = Division.objects.create(name='औरंगाबाद विभाग')
            
            # Add districts
            districts = ['औरंगाबाद', 'जालना', 'हिंगोली', 'परभणी', 'नांदेड', 'लातूर', 'उस्मानाबाद', 'बीड']
            district_objects = []
            for district_name in districts:
                district = District.objects.create(name=district_name, division=aurangabad_div)
                district_objects.append(district)
            
            # Add Satara Division
            satara_div = Division.objects.create(name='सातारा विभाग')
            
            # Add sample villages for each district
            sample_villages = {
                'औरंगाबाद': ['वलुज', 'पैठण', 'कन्नड', 'सोयगाव', 'खुलताबाद'],
                'जालना': ['जालना शहर', 'भोकरदन', 'परतूर', 'अंबड', 'जाफराबाद'],
                'हिंगोली': ['हिंगोली शहर', 'कल्याणी', 'औंढा नागनाथ', 'वशीम', 'सेंधवा'],
                'परभणी': ['परभणी शहर', 'पुरना', 'सोनपेठ', 'जिंतूर', 'गंगाखेड'],
                'नांदेड': ['नांदेड शहर', 'लोहा', 'भोकर', 'बिलोली', 'कंधार'],
                'लातूर': ['लातूर शहर', 'उदगीर', 'अहमदपुर', 'निलंगा', 'जलकोट'],
                'उस्मानाबाद': ['उस्मानाबाद शहर', 'तुळजापुर', 'ओमेरगा', 'परांडा', 'कलम'],
                'बीड': ['बीड शहर', 'गेवराई', 'पारली', 'अश्टी', 'वडवणी']
            }
            
            for district in district_objects:
                if district.name in sample_villages:
                    for village_name in sample_villages[district.name]:
                        Village.objects.create(name=village_name, district=district)
            
            # Add some sample news
            sample_news = [
                {
                    'title': 'मराठा आरक्षणाचा नवीन GR जारी',
                    'content': 'महाराष्ट्र सरकारने मराठा समुदायासाठी नवीन आरक्षण योजना जाहीर केली आहे. या योजनेअंतर्गत शिक्षण आणि नोकऱ्यांमध्ये आरक्षण दिले जाणार आहे.',
                    'is_featured': True
                },
                {
                    'title': 'आरक्षण प्रमाणपत्रासाठी अर्ज सुरू',
                    'content': 'मराठा समुदायातील व्यक्ती आता ऑनलाइन आणि ऑफलाइन पद्धतीने आरक्षण प्रमाणपत्रासाठी अर्ज करू शकतात.',
                    'is_featured': True
                },
                {
                    'title': 'रेफरल सिस्टमची माहिती',
                    'content': 'आरक्षण मिळवण्यासाठी तुमच्या गावातील किंवा कुटुंबातील आधीपासून आरक्षण असणाऱ्या व्यक्तीचा रेफरल आवश्यक आहे.',
                    'is_featured': False
                }
            ]
            
            for news_data in sample_news:
                News.objects.create(**news_data)
            
            self.stdout.write(
                self.style.SUCCESS('Successfully created initial data')
            )
        else:
            self.stdout.write('Data already exists. Skipping initialization.')

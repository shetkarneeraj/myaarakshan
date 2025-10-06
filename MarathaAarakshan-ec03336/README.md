# मराठा आरक्षण मंच (Maratha Arakshan Manch)

**आम्ही तुम्हाला तुमचे आरक्षण मिळवण्यासाठी मदत करण्यासाठी येथे आहोत**

एक comprehensive web platform जो महाराष्ट्रातील मराठा समुदायाला आरक्षण प्रक्रियेत मदत करण्यासाठी बनविला गेला आहे.

## 🌟 Features

### 🏠 **Horizontally Scrollable Cards** (मुख्य सेवा):
1. **आरक्षण माहिती** - पात्रता, कागदपत्रे आणि प्रक्रिया
2. **लाभार्थी यादी** - तुमच्या गावातील लाभार्थी शोधा  
3. **ताज्या बातम्या** - नवीनतम सरकारी निर्णय आणि अपडेट्स
4. **संपर्क** - मदतीसाठी आमच्याशी संपर्क साधा
5. **पात्रता तपासणी** - तुम्ही पात्र आहात का ते तपासा
6. **प्रक्रिया फ्लोचार्ट** - step-by-step प्रक्रिया समजून घ्या

### 📅 **Phase 1 Features** (पूर्ण):
- **🟢 OBC (कुणबी) जात प्रमाणपत्र मार्गदर्शक**: संपूर्ण A-Z माहिती
- **📊 प्रक्रिया फ्लोचार्ट**: दृश्य स्वरूपात step-by-step मार्गदर्शन
- **🔍 पात्रता तपासणी**: इंटरैक्टिव्ह eligibility checker
- **📚 शासन निर्णय गॅलरी**: सर्व GRs, फॉर्म्स आणि डॉक्युमेंट्स
- **👥 लाभार्थी यादी**: विभाग → जिल्हा → गाव → व्यक्ती हायरार्की  
- **📰 न्यूज सेक्शन**: ताज्या अपडेट्स आणि सरकारी निर्णय

### 📅 **Phase 2 Features** (पूर्ण):
- **✅ चेकलिस्ट PDF**: डाउनलोड करण्यायोग्य interactive checklist
- **❓ FAQ**: 20+ सामान्य प्रश्नांची तपशीलवार उत्तरे
- **🏢 जवळील कार्यालय**: जिल्हानिहाय सर्व संबंधित कार्यालये
- **🌟 यशोगाथा**: वापरकर्त्यांचे अनुभव आणि टिप्स  
- **🌐 भाषा बदल**: मराठी आणि इंग्रजी (partial)

### 📅 **Phase 3 Features** (पूर्ण):
- **👤 वापरकर्ता खाते**: Registration, Login, Profile management, Session handling
- **📊 स्टेटस ट्रॅकर**: Real-time application tracking with progress visualization
- **🔔 सूचना सेवा**: Web notifications, SMS/Email integration framework
- **📱 मोबाइल अॅप API**: Complete REST API for mobile app development
- **💰 व्यावसायिक सेवा**: Premium subscriptions, Payment gateway, Monetization

### 🔧 **Phase 3 Technical Implementation**:
- **User Authentication**: Password hashing, session management, role-based access
- **Application Management**: Submit applications, track progress, status updates
- **Payment Integration**: UPI, Cards, Net Banking support with security
- **Notification System**: Multi-channel notifications (Web, SMS, Email)
- **Mobile API**: RESTful endpoints for mobile app integration
- **Premium Services**: Subscription tiers (Free, Premium, Pro), Priority processing

### Technical Features:
- Flask web framework
- SQLite database
- Bootstrap 5 UI
- Marathi language support
- Real-time search functionality
- Admin verification system
- Mobile-responsive design

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Quick Start
1. **Clone/Download** करा:
```bash
cd /Users/ineerajrajeev/Desktop/MarathaAarakshan
```

2. **Virtual Environment** बनवा (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# किंवा Windows पर: venv\Scripts\activate
```

3. **Dependencies Install** करा:
```bash
pip install -r requirements.txt
```

4. **Application चालू** करा:
```bash
python app.py
```

5. **Browser** मध्ये जा: http://localhost:5000

## 🗂️ Project Structure

```
MarathaAarakshan/
├── app.py                 # मुख्य Flask application
├── requirements.txt       # Python dependencies
├── maratha_arakshan.db   # SQLite database (auto-created)
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # होम पेज
│   ├── search.html       # Search page
│   ├── news.html         # News page
│   ├── submit_details.html # माहिती submission
│   ├── division.html     # Division view
│   ├── district.html     # District view
│   ├── village.html      # Village view
│   └── admin/           # Admin templates
│       ├── dashboard.html
│       ├── people.html
│       ├── add_news.html
│       └── ...
├── static/              # Static files
│   ├── css/
│   │   └── style.css    # Custom styling
│   ├── js/
│   │   └── script.js    # JavaScript functionality
│   └── images/          # Image assets
└── README.md           # This file
```

## 📊 Database Schema

### Tables:
1. **Division** - विभाग (औरंगाबाद, सातारा)
2. **District** - जिल्हे (8 districts in औरंगाबाद)
3. **Village** - गावे (40+ villages)
4. **Person** - आरक्षण धारक
5. **News** - बातम्या

### Sample Data:
Application पहिल्यांदा चालू करताना sample data automatic load होतो:
- 2 Divisions
- 8 Districts in औरंगाबाद
- 40+ Villages
- 3 Sample news items

## 🔧 Usage Guide

### For Users:
1. **होम पेज** - विभाग निवडा
2. **जिल्हा** निवडा
3. **गाव** निवडा
4. **आरक्षण धारकांची यादी** पहा
5. **संपर्क** करा referral साठी
6. **माहिती भरा** तुमची details

### For Admins:
1. `/admin` URL वर जा
2. **Dashboard** - overview पहा
3. **People Management** - verify/delete submissions
4. **News Management** - बातम्या add करा
5. **Location Management** - नवीन गावे add करा

## 🛠️ Customization

### Adding New Villages:
```python
# Admin panel द्वारे किंवा directly database मध्ये
village = Village(name='नवीन गाव', district_id=district_id)
```

### Adding News:
```python
# Admin panel वापरा किंवा
news = News(title='शीर्षक', content='सामग्री', is_featured=True)
```

### Styling Changes:
- `static/css/style.css` मध्ये CSS modify करा
- Bootstrap classes use करा
- Orange color scheme (मराठा flag colors)

## 🔒 Security Notes

### Production Deployment:
1. **SECRET_KEY** बदला:
```python
app.config['SECRET_KEY'] = 'your-secure-secret-key'
```

2. **Database** PostgreSQL वापरा:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://...'
```

3. **Environment Variables** वापरा
4. **HTTPS** enable करा
5. **Admin Authentication** add करा

## 🌐 Features for Commercial Use

### Monetization Options:
1. **Premium Listings** - priority placement
2. **Verification Services** - faster processing
3. **Advertising Space** - banner ads
4. **Data Analytics** - insights for NGOs
5. **Mobile App** - extended features

### Scaling:
1. **Redis** for caching
2. **Celery** for background tasks
3. **Load Balancer** for high traffic
4. **CDN** for static files
5. **Database Clustering**

## 📱 Mobile App Integration

### API Endpoints Ready:
- `/api/districts/<division_id>`
- `/api/villages/<district_id>`
- JSON responses for mobile app

## 🤝 Contributing

### How to Contribute:
1. **Bug Reports** - issue tracker use करा
2. **Feature Requests** - detailed description द्या
3. **Code Contributions** - pull requests welcome
4. **Data Contributions** - village/district data

### Contact:
- **Email**: info@marathaarakshan.com
- **Phone**: +91 XXXXXXXXXX
- **Website**: https://marathaarakshan.com (future)

## 📄 License

© 2024 मराठा आरक्षण मंच. सर्व हक्क राखीव.

## 🎯 **Comprehensive Eligibility System**

### 📌 **पात्रता निकष (Eligibility Criteria)**:
- **अर्जदार कुणबी, मराठा-कुणबी किंवा कुणबी-मराठा** असल्याचे सिद्ध करणे आवश्यक
- **१३ ऑक्टोबर १९६७ पूर्वीचा** वास्तव्य दाखला असणे गरजेचे
- **नातेवाईकांकडे आधीपासून कुणबी प्रमाणपत्र** असल्यास त्याचा वापर
- **शेतीजमिनीची मालकी** अथवा कसोशीचा दाखला
- **शाळा दाखले/जन्म दाखले** ज्यामध्ये जात नमूद आहे

### ❌ **कोणाला मिळणार नाही**:
- १३ ऑक्टोबर १९६७ **नंतरचा दाखला** असलेले
- **कोणताही नातेवाईक किंवा पुरावा नसलेले**
- **बनावट/चुकीची कागदपत्रे** सादर करणारे  
- फक्त **"मराठा"** नोंदणी असलेले (कुणबी नसलेले)
- **Scrutiny Committee तपासणीमध्ये** अपूर्ण/चुकीची माहिती

### 📋 **Step-by-Step Workflow**:
1. **अर्ज दाखल** → ग्रामस्तर समितीकडे
2. **ग्राम समिती तपासणी** → महसूल अधिकारी + ग्रामपंचायत + कृषी अधिकारी  
3. **तालुका समिती** → अहवाल तपासून प्राथमिक निर्णय
4. **Scrutiny Committee** → अंतिम तपासणी आणि निर्णय
5. **प्रमाणपत्र जारी** → पात्रता सिद्ध झाल्यास

### 🎯 **वेबसाइट सुविधा**:
- **Interactive Eligibility Checker** → तुम्ही पात्र आहात का तपासा
- **Document Gallery** → सर्व GRs/Orders एकाच ठिकाणी
- **Step-by-step Flowchart** → प्रक्रिया visual स्वरूपात
- **Village-wise Beneficiary List** → रेफरलसाठी लाभार्थी शोधा
- **Warning System** → चुकीची माहिती देऊ नये याची जागृती

---

**Made with ❤️ for the Maratha Community**

*आम्ही तुम्हाला तुमचे आरक्षण मिळवण्यासाठी मदत करण्यासाठी येथे आहोत*
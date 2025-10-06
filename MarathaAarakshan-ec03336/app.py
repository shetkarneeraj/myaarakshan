from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    flash,
    session,
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import uuid
import random
import string

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key-here"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///maratha_arakshan.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Database Models
class Division(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    districts = db.relationship("District", backref="division", lazy=True)


class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    division_id = db.Column(db.Integer, db.ForeignKey("division.id"), nullable=False)
    villages = db.relationship("Village", backref="district", lazy=True)


class Village(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    district_id = db.Column(db.Integer, db.ForeignKey("district.id"), nullable=False)
    people = db.relationship("Person", backref="village", lazy=True)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    birth_year = db.Column(db.Integer, nullable=True)
    reservation_number = db.Column(db.String(50), unique=True, nullable=False)
    village_id = db.Column(db.Integer, db.ForeignKey("village.id"), nullable=False)
    contact_number = db.Column(db.String(15), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    is_verified = db.Column(db.Boolean, default=False)


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    is_featured = db.Column(db.Boolean, default=False)


# Phase 3 Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    village_id = db.Column(db.Integer, db.ForeignKey("village.id"), nullable=True)
    subscription_type = db.Column(db.String(20), default="free")  # free, premium, pro
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=False)

    # Relationships
    applications = db.relationship("Application", backref="user", lazy=True)
    notifications = db.relationship("Notification", backref="user", lazy=True)
    payments = db.relationship("Payment", backref="user", lazy=True)


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_number = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    status = db.Column(
        db.String(20), default="submitted"
    )  # submitted, under_review, approved, rejected
    priority = db.Column(db.String(20), default="normal")  # normal, high, premium

    # Application Details
    applicant_name = db.Column(db.String(100), nullable=False)
    applicant_surname = db.Column(db.String(50), nullable=False)
    birth_year = db.Column(db.Integer, nullable=True)
    village_id = db.Column(db.Integer, db.ForeignKey("village.id"), nullable=False)
    contact_number = db.Column(db.String(15), nullable=True)

    # Timestamps
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)
    estimated_completion = db.Column(db.DateTime, nullable=True)
    actual_completion = db.Column(db.DateTime, nullable=True)

    # Progress tracking
    current_stage = db.Column(db.String(50), default="gram_committee")
    progress_percentage = db.Column(db.Integer, default=20)

    # Relationships
    status_updates = db.relationship("StatusUpdate", backref="application", lazy=True)


class StatusUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(
        db.Integer, db.ForeignKey("application.id"), nullable=False
    )
    stage = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=True)
    updated_by = db.Column(db.String(100), nullable=True)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(
        db.String(20), default="info"
    )  # info, success, warning, error
    channel = db.Column(db.String(20), default="web")  # web, email, sms
    is_read = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_sent = db.Column(db.DateTime, nullable=True)


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    transaction_id = db.Column(db.String(50), unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    service = db.Column(
        db.String(50), nullable=False
    )  # premium_subscription, priority_processing, etc.
    payment_method = db.Column(db.String(20), nullable=False)  # upi, card, netbanking
    status = db.Column(
        db.String(20), default="pending"
    )  # pending, success, failed, refunded
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_processed = db.Column(db.DateTime, nullable=True)


class PremiumService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    duration_days = db.Column(db.Integer, nullable=False)
    features = db.Column(db.Text, nullable=False)  # JSON string of features
    is_active = db.Column(db.Boolean, default=True)


# Routes
@app.route("/")
def home():
    latest_news = (
        News.query.filter_by(is_featured=True)
        .order_by(News.date_posted.desc())
        .limit(3)
        .all()
    )
    divisions = Division.query.all()
    return render_template("index.html", news=latest_news, divisions=divisions)


@app.route("/division/<int:division_id>")
def view_division(division_id):
    division = Division.query.get_or_404(division_id)
    districts = District.query.filter_by(division_id=division_id).all()
    return render_template("division.html", division=division, districts=districts)


@app.route("/district/<int:district_id>")
def view_district(district_id):
    district = District.query.get_or_404(district_id)
    villages = Village.query.filter_by(district_id=district_id).all()
    return render_template("district.html", district=district, villages=villages)


@app.route("/village/<int:village_id>")
def view_village(village_id):
    village = Village.query.get_or_404(village_id)
    people = Person.query.filter_by(village_id=village_id, is_verified=True).all()
    return render_template("village.html", village=village, people=people)


@app.route("/search")
def search():
    query = request.args.get("q", "")
    village_name = request.args.get("village", "")
    surname = request.args.get("surname", "")

    results = []
    if query or village_name or surname:
        people_query = Person.query.filter_by(is_verified=True)

        if query:
            people_query = people_query.filter(
                (Person.name.contains(query)) | (Person.surname.contains(query))
            )

        if village_name:
            people_query = people_query.join(Village).filter(
                Village.name.contains(village_name)
            )

        if surname:
            people_query = people_query.filter(Person.surname.contains(surname))

        results = people_query.all()

    return render_template(
        "search.html",
        results=results,
        query=query,
        village_name=village_name,
        surname=surname,
    )


@app.route("/news")
def news():
    page = request.args.get("page", 1, type=int)
    news_items = News.query.order_by(News.date_posted.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template("news.html", news_items=news_items)


@app.route("/submit_details")
def submit_details():
    divisions = Division.query.all()
    return render_template("submit_details.html", divisions=divisions)


@app.route("/api/districts/<int:division_id>")
def get_districts(division_id):
    districts = District.query.filter_by(division_id=division_id).all()
    return jsonify([{"id": d.id, "name": d.name} for d in districts])


@app.route("/api/villages/<int:district_id>")
def get_villages(district_id):
    villages = Village.query.filter_by(district_id=district_id).all()
    return jsonify([{"id": v.id, "name": v.name} for v in villages])


@app.route("/submit_person", methods=["POST"])
def submit_person():
    try:
        person = Person(
            name=request.form["name"],
            surname=request.form["surname"],
            birth_year=(
                int(request.form["birth_year"]) if request.form["birth_year"] else None
            ),
            reservation_number=request.form["reservation_number"],
            village_id=int(request.form["village_id"]),
            contact_number=request.form.get("contact_number", ""),
        )
        db.session.add(person)
        db.session.commit()
        flash("तुमची माहिती यशस्वीरित्या सबमिट झाली आहे. वेरिफिकेशननंतर ती दिसेल.", "success")
    except Exception as e:
        flash("एरर आली आहे. कृपया पुन्हा प्रयत्न करा.", "error")
        db.session.rollback()

    return redirect(url_for("submit_details"))


# Admin Routes
@app.route("/admin")
def admin_dashboard():
    total_people = Person.query.count()
    verified_people = Person.query.filter_by(is_verified=True).count()
    pending_people = Person.query.filter_by(is_verified=False).count()
    total_news = News.query.count()

    recent_submissions = (
        Person.query.filter_by(is_verified=False)
        .order_by(Person.date_added.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "admin/dashboard.html",
        total_people=total_people,
        verified_people=verified_people,
        pending_people=pending_people,
        total_news=total_news,
        recent_submissions=recent_submissions,
    )


@app.route("/admin/people")
def admin_people():
    page = request.args.get("page", 1, type=int)
    status = request.args.get("status", "all")

    query = Person.query
    if status == "verified":
        query = query.filter_by(is_verified=True)
    elif status == "pending":
        query = query.filter_by(is_verified=False)

    people = query.order_by(Person.date_added.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template("admin/people.html", people=people, status=status)


@app.route("/admin/verify_person/<int:person_id>")
def verify_person(person_id):
    person = Person.query.get_or_404(person_id)
    person.is_verified = True
    db.session.commit()
    flash(f"{person.name} {person.surname} को वेरिफाई कर दिया गया।", "success")
    return redirect(url_for("admin_people"))


@app.route("/admin/delete_person/<int:person_id>")
def delete_person(person_id):
    person = Person.query.get_or_404(person_id)
    db.session.delete(person)
    db.session.commit()
    flash(f"{person.name} {person.surname} की जानकारी हटा दी गई।", "success")
    return redirect(url_for("admin_people"))


@app.route("/admin/news")
def admin_news():
    page = request.args.get("page", 1, type=int)
    news_items = News.query.order_by(News.date_posted.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template("admin/news.html", news_items=news_items)


@app.route("/admin/news/add", methods=["GET", "POST"])
def add_news():
    if request.method == "POST":
        try:
            news_item = News(
                title=request.form["title"],
                content=request.form["content"],
                image_url=request.form.get("image_url", ""),
                is_featured=bool(request.form.get("is_featured")),
            )
            db.session.add(news_item)
            db.session.commit()
            flash("बातमी सफलतापूर्वक जोड़ी गई।", "success")
            return redirect(url_for("admin_news"))
        except Exception as e:
            flash("एरर आई है। कृपया फिर से कोशिश करें।", "error")
            db.session.rollback()

    return render_template("admin/add_news.html")


@app.route("/admin/locations")
def admin_locations():
    divisions = Division.query.all()
    return render_template("admin/locations.html", divisions=divisions)


@app.route("/admin/add_village", methods=["POST"])
def add_village():
    try:
        village = Village(
            name=request.form["name"], district_id=int(request.form["district_id"])
        )
        db.session.add(village)
        db.session.commit()
        flash("गाव सफलतापूर्वक जोड़ा गया।", "success")
    except Exception as e:
        flash("एरर आई है।", "error")
        db.session.rollback()

    return redirect(url_for("admin_locations"))


# Phase 1 Features
@app.route("/guide")
def guide():
    return render_template("guide.html")


@app.route("/flowchart")
def flowchart():
    return render_template("flowchart.html")


@app.route("/eligibility-check")
def eligibility_check():
    return render_template("eligibility_check.html")


@app.route("/check-eligibility", methods=["POST"])
def check_eligibility():
    try:
        # Get form data
        residence_proof = request.form.get("residence_proof")
        kunbi_relatives = request.form.get("kunbi_relatives")
        land_records = request.form.get("land_records")
        school_records = request.form.get("school_records")
        caste_records = request.form.get("caste_records")
        gazette_record = request.form.get("gazette_record")

        print(
            f"Received form data: residence={residence_proof}, relatives={kunbi_relatives}, land={land_records}, school={school_records}, caste={caste_records}, gazette={gazette_record}"
        )

        # Flowchart Logic:
        # 1. Must have residence proof before 1967
        if residence_proof != "yes":
            return jsonify(
                {
                    "status": "success",
                    "eligible": False,
                    "reasons": ["१३ ऑक्टोबर १९६७ पूर्वीचा वास्तव्य पुरावा अनिवार्य आहे"],
                }
            )

        # 2. Must have Kunbi in caste records
        if caste_records == "maratha":
            return jsonify(
                {
                    "status": "success",
                    "eligible": False,
                    "reasons": ['फक्त "मराठा" जात पुरेशी नाही - "कुणबी" उल्लेख आवश्यक'],
                }
            )
        elif caste_records == "other":
            return jsonify(
                {
                    "status": "success",
                    "eligible": False,
                    "reasons": ["कागदपत्रांमध्ये कुणबी/मराठा-कुणबी नमूद असणे आवश्यक"],
                }
            )

        # 3. Must have at least one evidence
        has_relatives = kunbi_relatives == "yes"
        has_gazette = gazette_record == "yes"
        has_land = land_records == "yes"
        has_school = school_records == "yes"

        if not (has_relatives or has_gazette or has_land or has_school):
            return jsonify(
                {
                    "status": "success",
                    "eligible": False,
                    "reasons": [
                        "कमीत कमी एक पुरावा आवश्यक: नातेवाईकांचे प्रमाणपत्र, गॅझेट नोंद, जमीन कागदपत्रे किंवा शाळा दाखले"
                    ],
                }
            )

        # All checks passed - eligible
        guidance = []
        if has_relatives or has_gazette:
            guidance.append("तुमच्याकडे मजबूत पुरावे आहेत")
        else:
            guidance.append(
                "अधिक मजबूत पुरावे (गॅझेट नोंद/नातेवाईकांचे प्रमाणपत्र) मिळवण्याचा प्रयत्न करा"
            )

        return jsonify({"status": "success", "eligible": True, "reasons": guidance})

    except Exception as e:
        print(f"Error in check_eligibility: {e}")
        return jsonify({"status": "error", "message": "Server error occurred"})


@app.route("/documents")
def documents():
    documents = [
        {
            "title": "GR - मराठा आरक्षण योजना",
            "description": "नवीनतम सरकारी निर्णय",
            "type": "PDF",
            "size": "2.5 MB",
            "url": "/static/docs/maratha_reservation_gr.pdf",
        },
        {
            "title": "अर्ज फॉर्म",
            "description": "कुणबी प्रमाणपत्रासाठी अर्ज",
            "type": "PDF",
            "size": "1.2 MB",
            "url": "/static/docs/application_form.pdf",
        },
        {
            "title": "आवश्यक कागदपत्रांची यादी",
            "description": "सर्व आवश्यक दस्तऐवज",
            "type": "PDF",
            "size": "800 KB",
            "url": "/static/docs/required_documents.pdf",
        },
    ]
    return render_template("documents.html", documents=documents)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/documents-explained")
def documents_explained():
    return render_template("documents_explained.html")


@app.route("/district-wise-records")
def district_wise_records():
    return render_template("district_wise_records.html")


@app.route("/pre1967-records")
def pre1967_records():
    return render_template("pre1967_records.html")


@app.route("/phases")
def phases():
    return render_template("phases.html")


# Phase 2 Features
@app.route("/faq")
def faq():
    faqs = [
        {
            "question": "कुणबी प्रमाणपत्रासाठी कोण अर्ज करू शकतो?",
            "answer": "कुणबी, मराठा-कुणबी किंवा कुणबी-मराठा जातीचे लोक अर्ज करू शकतात. त्यांच्याकडे १३ ऑक्टोबर १९६७ पूर्वीचा निवास दाखला असणे आवश्यक आहे.",
        },
        {
            "question": "कोणती कागदपत्रे लागतात?",
            "answer": "जन्म प्रमाणपत्र, ७/१२ उतारा, निवासी दाखला, नातेवाईकांचे कुणबी प्रमाणपत्र (असल्यास), शाळा दाखले आणि स्थानीय पुरावे.",
        },
        {
            "question": "अर्ज कुठे द्यावा?",
            "answer": "ग्रामस्तर समितीकडे अर्ज दाखल करावा. ग्राम महसूल अधिकारी, ग्रामपंचायत अधिकारी यांच्याकडे संपर्क साधा.",
        },
        {
            "question": "प्रक्रियेला किती वेळ लागतो?",
            "answer": "सामान्यतः ३०-९० दिवस लागतात. ग्राम समिती, तालुका समिती आणि Scrutiny Committee तपासणी केल्यानंतर निर्णय घेतला जातो.",
        },
    ]
    return render_template("faq.html", faqs=faqs)


@app.route("/nearest-office")
def nearest_office():
    offices = [
        {
            "name": "औरंगाबाद जिल्हा कलेक्टर कार्यालय",
            "address": "जिल्हा कलेक्टर कार्यालय, औरंगाबाद",
            "phone": "0240-2123456",
            "email": "collector.aurangabad@maharashtra.gov.in",
            "hours": "सकाळी १०:०० ते संध्याकाळी ५:००",
        },
        {
            "name": "जालना जिल्हा कलेक्टर कार्यालय",
            "address": "जिल्हा कलेक्टर कार्यालय, जालना",
            "phone": "02482-123456",
            "email": "collector.jalna@maharashtra.gov.in",
            "hours": "सकाळी १०:०० ते संध्याकाळी ५:००",
        },
    ]
    return render_template("nearest_office.html", offices=offices)


@app.route("/testimonials")
def testimonials():
    testimonials_data = [
        {
            "name": "राहुल पाटील",
            "village": "पैठण, औरंगाबाद",
            "message": "या वेबसाइटच्या मदतीने मला माझ्या गावातील लाभार्थी सापडले आणि मला आरक्षण मिळाले.",
            "rating": 5,
        },
        {
            "name": "सुनिता जाधव",
            "village": "भोकरदन, जालना",
            "message": "खूप सोपी प्रक्रिया आणि सर्व माहिती एकाच ठिकाणी मिळते.",
            "rating": 5,
        },
    ]
    return render_template("testimonials.html", testimonials=testimonials_data)


# Phase 3 Routes - User Authentication
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            # Check if user already exists
            existing_user = User.query.filter_by(email=request.form["email"]).first()
            if existing_user:
                flash("या ईमेल पत्त्याने खाते आधीच आहे", "error")
                return redirect(url_for("register"))

            # Create new user
            user = User(
                username=request.form["username"],
                email=request.form["email"],
                password_hash=generate_password_hash(request.form["password"]),
                full_name=request.form["full_name"],
                phone=request.form.get("phone", ""),
                village_id=(
                    int(request.form["village_id"])
                    if request.form.get("village_id")
                    else None
                ),
            )

            db.session.add(user)
            db.session.commit()

            # Create welcome notification
            notification = Notification(
                user_id=user.id,
                title="स्वागत आहे!",
                message=f"नमस्कार {user.full_name}, मराठा आरक्षण मंचमध्ये तुमचे स्वागत आहे!",
                notification_type="success",
            )
            db.session.add(notification)
            db.session.commit()

            flash("खाते यशस्वीरित्या तयार झाले! आता लॉगिन करा", "success")
            return redirect(url_for("login"))

        except Exception as e:
            flash("खाते तयार करताना एरर आली", "error")
            db.session.rollback()

    divisions = Division.query.all()
    return render_template("auth/register.html", divisions=divisions)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            session["username"] = user.username
            user.last_login = datetime.utcnow()
            db.session.commit()

            flash(f"स्वागत आहे, {user.full_name}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("चुकीचा ईमेल किंवा पासवर्ड", "error")

    return render_template("auth/login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("तुम्ही लॉग आउट झाला आहात", "info")
    return redirect(url_for("home"))


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("कृपया पहिले लॉगिन करा", "warning")
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])
    applications = (
        Application.query.filter_by(user_id=user.id)
        .order_by(Application.date_submitted.desc())
        .all()
    )
    notifications = (
        Notification.query.filter_by(user_id=user.id, is_read=False)
        .order_by(Notification.date_created.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "user/dashboard.html",
        user=user,
        applications=applications,
        notifications=notifications,
    )


@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])
    return render_template("user/profile.html", user=user)


# Application Management
@app.route("/submit-application", methods=["GET", "POST"])
def submit_application():
    if "user_id" not in session:
        flash("कृपया पहिले लॉगिन करा", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            # Generate unique application number
            app_number = f"MR{datetime.now().year}{random.randint(100000, 999999)}"

            user = User.query.get(session["user_id"])

            # Calculate estimated completion based on subscription
            days_to_complete = 120  # Default 4 months
            if user.subscription_type == "premium":
                days_to_complete = 60  # 2 months for premium
            elif user.subscription_type == "pro":
                days_to_complete = 30  # 1 month for pro

            application = Application(
                application_number=app_number,
                user_id=user.id,
                applicant_name=request.form["applicant_name"],
                applicant_surname=request.form["applicant_surname"],
                birth_year=(
                    int(request.form["birth_year"])
                    if request.form["birth_year"]
                    else None
                ),
                village_id=int(request.form["village_id"]),
                contact_number=request.form.get("contact_number", ""),
                priority="premium" if user.subscription_type != "free" else "normal",
                estimated_completion=datetime.utcnow()
                + timedelta(days=days_to_complete),
            )

            db.session.add(application)
            db.session.commit()

            # Create initial status update
            status_update = StatusUpdate(
                application_id=application.id,
                stage="gram_committee",
                status="submitted",
                message="अर्ज यशस्वीरित्या सबमिट झाला आहे",
                updated_by="System",
            )
            db.session.add(status_update)

            # Create notification
            notification = Notification(
                user_id=user.id,
                title="अर्ज सबमिट झाला",
                message=f"तुमचा अर्ज क्रमांक {app_number} यशस्वीरित्या सबमिट झाला आहे",
                notification_type="success",
            )
            db.session.add(notification)
            db.session.commit()

            flash(f"अर्ज यशस्वीरित्या सबमिट झाला! अर्ज क्रमांक: {app_number}", "success")
            return redirect(url_for("track_application", app_number=app_number))

        except Exception as e:
            flash("अर्ज सबमिट करताना एरर आली", "error")
            db.session.rollback()

    divisions = Division.query.all()
    return render_template("user/submit_application.html", divisions=divisions)


# Status Tracker
@app.route("/track-application/<app_number>")
def track_application(app_number):
    application = Application.query.filter_by(
        application_number=app_number
    ).first_or_404()

    # Check if user owns this application or allow public tracking
    if "user_id" in session and application.user_id != session["user_id"]:
        flash("तुम्ही फक्त तुमच्या स्वतःच्या अर्जाची स्थिती पाहू शकता", "error")
        return redirect(url_for("dashboard"))

    status_updates = (
        StatusUpdate.query.filter_by(application_id=application.id)
        .order_by(StatusUpdate.date_updated.asc())
        .all()
    )

    return render_template(
        "user/track_application.html",
        application=application,
        status_updates=status_updates,
    )


@app.route("/track", methods=["GET", "POST"])
def public_track():
    if request.method == "POST":
        app_number = request.form["application_number"]
        phone = request.form["phone"]

        application = Application.query.filter_by(
            application_number=app_number, contact_number=phone
        ).first()

        if application:
            return redirect(url_for("track_application", app_number=app_number))
        else:
            flash("अर्ज क्रमांक किंवा फोन नंबर चुकीचा आहे", "error")

    return render_template("user/public_track.html")


# Notifications
@app.route("/notifications")
def notifications():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_notifications = (
        Notification.query.filter_by(user_id=session["user_id"])
        .order_by(Notification.date_created.desc())
        .all()
    )

    # Mark as read
    for notification in user_notifications:
        if not notification.is_read:
            notification.is_read = True
    db.session.commit()

    return render_template("user/notifications.html", notifications=user_notifications)


# Premium Services and Monetization
@app.route("/premium")
def premium_services():
    services = [
        {
            "name": "प्रीमियम सब्स्क्रिप्शन",
            "price": 499,
            "duration": "6 महिने",
            "features": [
                "प्राधान्य प्रक्रिया",
                "SMS अपडेट्स",
                "डेडिकेटेड सपोर्ट",
                "24/7 हेल्पलाइन",
            ],
        },
        {
            "name": "प्रो सब्स्क्रिप्शन",
            "price": 999,
            "duration": "1 वर्ष",
            "features": [
                "जलद प्रक्रिया",
                "SMS + Email अपडेट्स",
                "व्यक्तिगत सल्लागार",
                "डॉक्युमेंट रिव्यू",
            ],
        },
        {
            "name": "तत्काळ प्रक्रिया",
            "price": 1999,
            "duration": "एकवेळ",
            "features": ["30 दिवसांत प्रक्रिया", "प्राधान्य हाताळणी", "डेडिकेटेड केस मॅनेजर"],
        },
    ]

    user_subscription = None
    if "user_id" in session:
        user = User.query.get(session["user_id"])
        user_subscription = user.subscription_type

    return render_template(
        "premium/services.html", services=services, user_subscription=user_subscription
    )


@app.route("/purchase/<service_name>")
def purchase_service(service_name):
    if "user_id" not in session:
        flash("कृपया पहिले लॉगिन करा", "warning")
        return redirect(url_for("login"))

    service_prices = {"premium": 499, "pro": 999, "express": 1999}

    if service_name not in service_prices:
        flash("अवैध सेवा", "error")
        return redirect(url_for("premium_services"))

    return render_template(
        "premium/payment.html", service=service_name, price=service_prices[service_name]
    )


@app.route("/process-payment", methods=["POST"])
def process_payment():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        # Generate transaction ID
        transaction_id = (
            f"TXN{datetime.now().strftime('%Y%m%d')}{random.randint(10000, 99999)}"
        )

        payment = Payment(
            user_id=session["user_id"],
            transaction_id=transaction_id,
            amount=float(request.json["amount"]),
            service=request.json["service"],
            payment_method=request.json["payment_method"],
            status="success",  # In real implementation, this would be processed
        )

        db.session.add(payment)

        # Update user subscription
        user = User.query.get(session["user_id"])
        if request.json["service"] in ["premium", "pro"]:
            user.subscription_type = request.json["service"]

        # Create notification
        notification = Notification(
            user_id=user.id,
            title="पेमेंट यशस्वी",
            message=f"तुमचा पेमेंट ₹{payment.amount} यशस्वीरित्या प्रक्रिया झाला. Transaction ID: {transaction_id}",
            notification_type="success",
        )
        db.session.add(notification)
        db.session.commit()

        return jsonify({"success": True, "transaction_id": transaction_id})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Payment failed"}), 500


# Mobile App API Endpoints
@app.route("/api/v1/login", methods=["POST"])
def api_login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            user.last_login = datetime.utcnow()
            db.session.commit()

            return jsonify(
                {
                    "success": True,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "full_name": user.full_name,
                        "subscription_type": user.subscription_type,
                    },
                    "token": f"token_{user.id}_{datetime.now().timestamp()}",  # Simple token for demo
                }
            )
        else:
            return jsonify({"success": False, "message": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"success": False, "message": "Server error"}), 500


@app.route("/api/v1/applications/<int:user_id>")
def api_user_applications(user_id):
    try:
        applications = Application.query.filter_by(user_id=user_id).all()

        apps_data = []
        for app in applications:
            apps_data.append(
                {
                    "application_number": app.application_number,
                    "status": app.status,
                    "current_stage": app.current_stage,
                    "progress_percentage": app.progress_percentage,
                    "date_submitted": app.date_submitted.isoformat(),
                    "estimated_completion": (
                        app.estimated_completion.isoformat()
                        if app.estimated_completion
                        else None
                    ),
                }
            )

        return jsonify({"success": True, "applications": apps_data})

    except Exception as e:
        return jsonify({"success": False, "message": "Server error"}), 500


@app.route("/api/v1/track/<app_number>")
def api_track_application(app_number):
    try:
        application = Application.query.filter_by(application_number=app_number).first()

        if not application:
            return jsonify({"success": False, "message": "Application not found"}), 404

        status_updates = (
            StatusUpdate.query.filter_by(application_id=application.id)
            .order_by(StatusUpdate.date_updated.asc())
            .all()
        )

        updates_data = []
        for update in status_updates:
            updates_data.append(
                {
                    "stage": update.stage,
                    "status": update.status,
                    "message": update.message,
                    "date_updated": update.date_updated.isoformat(),
                    "updated_by": update.updated_by,
                }
            )

        app_data = {
            "application_number": application.application_number,
            "status": application.status,
            "current_stage": application.current_stage,
            "progress_percentage": application.progress_percentage,
            "date_submitted": application.date_submitted.isoformat(),
            "estimated_completion": (
                application.estimated_completion.isoformat()
                if application.estimated_completion
                else None
            ),
            "status_updates": updates_data,
        }

        return jsonify({"success": True, "application": app_data})

    except Exception as e:
        return jsonify({"success": False, "message": "Server error"}), 500


@app.route("/api/v1/notifications/<int:user_id>")
def api_user_notifications(user_id):
    try:
        notifications = (
            Notification.query.filter_by(user_id=user_id)
            .order_by(Notification.date_created.desc())
            .limit(20)
            .all()
        )

        notif_data = []
        for notif in notifications:
            notif_data.append(
                {
                    "id": notif.id,
                    "title": notif.title,
                    "message": notif.message,
                    "notification_type": notif.notification_type,
                    "is_read": notif.is_read,
                    "date_created": notif.date_created.isoformat(),
                }
            )

        return jsonify({"success": True, "notifications": notif_data})

    except Exception as e:
        return jsonify({"success": False, "message": "Server error"}), 500


@app.route("/api/v1/villages/<int:district_id>")
def api_villages(district_id):
    try:
        villages = Village.query.filter_by(district_id=district_id).all()
        villages_data = [{"id": v.id, "name": v.name} for v in villages]
        return jsonify({"success": True, "villages": villages_data})
    except Exception as e:
        return jsonify({"success": False, "message": "Server error"}), 500


@app.route("/api/districts/<int:division_id>")
def api_districts(division_id):
    try:
        districts = District.query.filter_by(division_id=division_id).all()
        districts_data = [{"id": d.id, "name": d.name} for d in districts]
        return jsonify(districts_data)
    except Exception as e:
        return jsonify({"error": "Server error"}), 500


@app.route("/api/villages/<int:district_id>")
def api_villages_simple(district_id):
    try:
        villages = Village.query.filter_by(district_id=district_id).all()
        villages_data = [{"id": v.id, "name": v.name} for v in villages]
        return jsonify(villages_data)
    except Exception as e:
        return jsonify({"error": "Server error"}), 500


# Notification Services
def send_sms_notification(phone, message):
    """Mock SMS service - integrate with real SMS provider"""
    print(f"SMS to {phone}: {message}")
    return True


def send_email_notification(email, subject, message):
    """Mock Email service - integrate with real email provider"""
    print(f"Email to {email}: {subject} - {message}")
    return True


@app.route("/api/send-notification", methods=["POST"])
def send_notification():
    """API endpoint to send notifications - for admin use"""
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        title = data.get("title")
        message = data.get("message")
        channels = data.get("channels", ["web"])  # web, sms, email

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Create web notification
        notification = Notification(
            user_id=user_id, title=title, message=message, notification_type="info"
        )
        db.session.add(notification)

        # Send SMS if requested
        if "sms" in channels and user.phone:
            send_sms_notification(user.phone, f"{title}: {message}")

        # Send Email if requested
        if "email" in channels:
            send_email_notification(user.email, title, message)

        db.session.commit()
        return jsonify({"success": True})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to send notification"}), 500


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # Initialize sample data if tables are empty
        if Division.query.count() == 0:
            # Add Aurangabad Division
            aurangabad_div = Division(name="औरंगाबाद विभाग")
            db.session.add(aurangabad_div)
            db.session.commit()

            # Add districts
            districts = [
                "औरंगाबाद",
                "जालना",
                "हिंगोली",
                "परभणी",
                "नांदेड",
                "लातूर",
                "उस्मानाबाद",
                "बीड",
            ]
            district_objects = []
            for district_name in districts:
                district = District(name=district_name, division_id=aurangabad_div.id)
                db.session.add(district)
                district_objects.append(district)

            # Add Satara Division
            satara_div = Division(name="सातारा विभाग")
            db.session.add(satara_div)

            db.session.commit()

            # Add sample villages for each district
            sample_villages = {
                "औरंगाबाद": ["वलुज", "पैठण", "कन्नड", "सोयगाव", "खुलताबाद"],
                "जालना": ["जालना शहर", "भोकरदन", "परतूर", "अंबड", "जाफराबाद"],
                "हिंगोली": ["हिंगोली शहर", "कल्याणी", "औंढा नागनाथ", "वशीम", "सेंधवा"],
                "परभणी": ["परभणी शहर", "पुरना", "सोनपेठ", "जिंतूर", "गंगाखेड"],
                "नांदेड": ["नांदेड शहर", "लोहा", "भोकर", "बिलोली", "कंधार"],
                "लातूर": ["लातूर शहर", "उदगीर", "अहमदपुर", "निलंगा", "जलकोट"],
                "उस्मानाबाद": ["उस्मानाबाद शहर", "तुळजापुर", "ओमेरगा", "परांडा", "कलम"],
                "बीड": ["बीड शहर", "गेवराई", "पारली", "अश्टी", "वडवणी"],
            }

            for district in district_objects:
                if district.name in sample_villages:
                    for village_name in sample_villages[district.name]:
                        village = Village(name=village_name, district_id=district.id)
                        db.session.add(village)

            db.session.commit()

            # Add some sample news
            sample_news = [
                {
                    "title": "मराठा आरक्षणाचा नवीन GR जारी",
                    "content": "महाराष्ट्र सरकारने मराठा समुदायासाठी नवीन आरक्षण योजना जाहीर केली आहे. या योजनेअंतर्गत शिक्षण आणि नोकऱ्यांमध्ये आरक्षण दिले जाणार आहे.",
                    "is_featured": True,
                },
                {
                    "title": "आरक्षण प्रमाणपत्रासाठी अर्ज सुरू",
                    "content": "मराठा समुदायातील व्यक्ती आता ऑनलाइन आणि ऑफलाइन पद्धतीने आरक्षण प्रमाणपत्रासाठी अर्ज करू शकतात.",
                    "is_featured": True,
                },
                {
                    "title": "रेफरल सिस्टमची माहिती",
                    "content": "आरक्षण मिळवण्यासाठी तुमच्या गावातील किंवा कुटुंबातील आधीपासून आरक्षण असणाऱ्या व्यक्तीचा रेफरल आवश्यक आहे.",
                    "is_featured": False,
                },
            ]

            for news_data in sample_news:
                news = News(**news_data)
                db.session.add(news)

            db.session.commit()

    app.run(debug=True)

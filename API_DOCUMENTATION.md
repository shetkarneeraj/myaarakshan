# 📱 मराठा आरक्षण मंच - Mobile App API Documentation

## 🔗 Base URL
```
http://localhost:5000/api/v1
```

## 🔐 Authentication
Currently using simple token-based authentication for demo purposes.

## 📋 API Endpoints

### 1. User Authentication

#### Login
```http
POST /api/v1/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "user@example.com",
    "full_name": "John Doe",
    "subscription_type": "premium"
  },
  "token": "token_1_1694123456.789"
}
```

### 2. User Applications

#### Get User Applications
```http
GET /api/v1/applications/{user_id}
```

**Response:**
```json
{
  "success": true,
  "applications": [
    {
      "application_number": "MR2024123456",
      "status": "under_review",
      "current_stage": "gram_committee",
      "progress_percentage": 40,
      "date_submitted": "2024-09-11T10:30:00",
      "estimated_completion": "2024-12-11T10:30:00"
    }
  ]
}
```

### 3. Application Tracking

#### Track Specific Application
```http
GET /api/v1/track/{application_number}
```

**Response:**
```json
{
  "success": true,
  "application": {
    "application_number": "MR2024123456",
    "status": "under_review",
    "current_stage": "gram_committee",
    "progress_percentage": 40,
    "date_submitted": "2024-09-11T10:30:00",
    "estimated_completion": "2024-12-11T10:30:00",
    "status_updates": [
      {
        "stage": "gram_committee",
        "status": "submitted",
        "message": "अर्ज यशस्वीरित्या सबमिट झाला आहे",
        "date_updated": "2024-09-11T10:30:00",
        "updated_by": "System"
      }
    ]
  }
}
```

### 4. Notifications

#### Get User Notifications
```http
GET /api/v1/notifications/{user_id}
```

**Response:**
```json
{
  "success": true,
  "notifications": [
    {
      "id": 1,
      "title": "अर्ज सबमिट झाला",
      "message": "तुमचा अर्ज क्रमांक MR2024123456 यशस्वीरित्या सबमिट झाला आहे",
      "notification_type": "success",
      "is_read": false,
      "date_created": "2024-09-11T10:30:00"
    }
  ]
}
```

### 5. Location Data

#### Get Villages by District
```http
GET /api/v1/villages/{district_id}
```

**Response:**
```json
{
  "success": true,
  "villages": [
    {
      "id": 1,
      "name": "वलुज"
    },
    {
      "id": 2,
      "name": "पैठण"
    }
  ]
}
```

## 📝 Error Responses

All API endpoints return errors in this format:
```json
{
  "success": false,
  "message": "Error description"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `401` - Unauthorized
- `404` - Not Found
- `500` - Server Error

## 🔔 Notification API (Admin)

#### Send Notification
```http
POST /api/send-notification
Content-Type: application/json

{
  "user_id": 1,
  "title": "Status Update",
  "message": "Your application has been approved",
  "channels": ["web", "sms", "email"]
}
```

## 📱 Mobile App Features Supported

### 1. **User Management**
- User registration
- Login/Logout
- Profile management
- Session handling

### 2. **Application Management**
- Submit new applications
- Track application status
- View application history
- Progress visualization

### 3. **Real-time Notifications**
- Push notifications
- In-app notifications
- SMS/Email notifications
- Read/unread status

### 4. **Location Services**
- Division/District/Village hierarchy
- Location-based search
- Beneficiary search by location

### 5. **Premium Features**
- Subscription management
- Premium service access
- Priority processing
- Payment integration

## 🔧 Technical Implementation Notes

### Database Models
- `User` - User accounts with subscription info
- `Application` - Application submissions and tracking
- `StatusUpdate` - Application progress updates
- `Notification` - User notifications
- `Payment` - Payment transactions

### Security Features
- Password hashing with Werkzeug
- Session-based authentication
- Input validation and sanitization
- SQL injection protection

### Mobile App Development Tips

1. **Authentication Flow**
   ```
   Login → Store Token → Include in Headers → API Calls
   ```

2. **Real-time Updates**
   - Implement periodic polling for status updates
   - Use push notifications for important updates
   - Cache data locally for offline viewing

3. **User Experience**
   - Progress indicators for application status
   - Offline mode for viewing cached data
   - Push notifications for status changes

4. **Payment Integration**
   - Use secure payment gateways
   - Implement receipt management
   - Handle payment failures gracefully

## 🚀 Getting Started

1. **Setup Backend**
   ```bash
   cd MarathaAarakshan
   python app.py
   ```

2. **Test API**
   ```bash
   curl -X POST http://localhost:5000/api/v1/login \
     -H "Content-Type: application/json" \
     -d '{"email":"demo@marathaarakshan.com","password":"demo123"}'
   ```

3. **Mobile App Integration**
   - Use HTTP client library (Retrofit, Axios, etc.)
   - Implement token-based authentication
   - Handle API errors gracefully
   - Implement offline data caching

## 📞 Support

For API support and mobile app development queries:
- **Email**: developer@marathaarakshan.com
- **Phone**: +91 98765 43210
- **Documentation**: [GitHub Repository]

---

**Note**: This API is designed for the Maratha Arakshan mobile application. All endpoints support JSON format and follow REST conventions.

# 📧 Email Automation System - Complete Documentation

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Installation & Setup](#installation--setup)
4. [How to Use](#how-to-use)
5. [API Documentation](#api-documentation)
6. [Email Template System](#email-template-system)
7. [Database Schema](#database-schema)
8. [Technical Architecture](#technical-architecture)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 Project Overview

**Innovative Skills BD Email Automation System** - A Django-based email automation platform for sending personalized course enrollment emails to students.

### Key Highlights:
- ✅ Manual email control (no auto-send on upload)
- ✅ Custom email templates with placeholders
- ✅ Real-time table updates
- ✅ Mobile-optimized email design
- ✅ Brand-consistent colors (Dark Navy + Orange)
- ✅ Excel file upload support

### Technology Stack:
- **Backend:** Django 5.2.1, Django REST Framework
- **Database:** SQLite (development)
- **Email:** Gmail SMTP with TLS
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Data Processing:** pandas, openpyxl

---

## ✨ Features

### 1. Excel File Upload
- Drag & drop or click to upload
- Flexible column detection (case-insensitive)
- Supports columns: Name, Email, Mobile, Course Name, Link
- Replace all data option
- Validates data before import

### 2. Custom Email Templates
- Create custom subject and message
- Use placeholders: `{name}`, `{course_name}`, `{link}`
- `{link}` automatically converts to clickable button
- Beautiful HTML email design
- Mobile-responsive layout

### 3. Manual Email Control
- Excel upload only saves data (NO auto-send)
- Emails sent ONLY when custom template submitted
- Full control over when emails are sent
- Send to all students with one click

### 4. Real-Time Updates
- Table auto-refreshes every 1 second after sending
- See email status update in real-time
- Progressive "✓ Sent" status display
- Auto-stops after 30 seconds

### 5. Email Design
- **Header:** Dark navy blue (#0a1628)
- **Button:** Orange/coral (#ff6b35)
- **Mobile-optimized:** Works on all devices
- **Professional:** Clean and modern design
- **Accessible:** High contrast ratios

### 6. Data Management
- View all students in table
- Delete individual records
- Delete all data with confirmation
- Track email status per student
- Statistics dashboard

---

## 🚀 Installation & Setup

### Prerequisites:
```bash
- Python 3.8+
- pip (Python package manager)
- Gmail account with App Password
```

### Step 1: Clone Repository
```bash
git clone https://github.com/Raihanroo/Email_tamplate.git
cd Email_tamplate/email_project
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**Requirements:**
```
Django==5.2.1
djangorestframework==3.14.0
pandas==2.0.3
openpyxl==3.1.2
```

### Step 3: Configure Email Settings

Edit `email_project/settings.py`:

```python
# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'  # Change this
EMAIL_HOST_PASSWORD = 'your-app-password'  # Change this
```

**Get Gmail App Password:**
1. Go to: https://myaccount.google.com/apppasswords
2. Create app password for "Mail"
3. Copy 16-character password
4. Paste in settings.py

### Step 4: Run Migrations
```bash
python manage.py migrate
```

### Step 5: Start Server
```bash
python manage.py runserver
```

### Step 6: Open Browser
```
http://127.0.0.1:8000/
```

---

## 📖 How to Use

### Workflow:

```
1. Upload Excel File
   ↓
2. Data Saved (NO email sent)
   ↓
3. Click "Create Template"
   ↓
4. Write Subject & Message
   ↓
5. Use Placeholders: {name}, {course_name}, {link}
   ↓
6. Click "Send to All Students"
   ↓
7. Emails Sent Immediately
   ↓
8. Table Auto-Refreshes (Real-time updates)
```

### Step-by-Step Guide:

#### 1. Upload Excel File

**Excel Format:**
| Name | Email | Mobile | Course Name | Link |
|------|-------|--------|-------------|------|
| Raihan Islam | raihan@example.com | 01712345678 | Python Programming | https://course-link.com |

**Steps:**
1. Drag & drop Excel file OR click upload area
2. (Optional) Check "Replace all existing data"
3. Click "Upload & Import"
4. Data saved to database
5. **NO emails sent yet**

#### 2. Create Custom Template

**Steps:**
1. Click "Create Template" button
2. Enter Subject (e.g., "Welcome to Python Course")
3. Enter Message:
   ```
   Hello {name},
   
   You are interested in {course_name}. 
   Click the button below to enroll:
   
   {link}
   
   Best regards,
   Innovative Skills BD
   ```
4. Click placeholder buttons to insert: 👤 Name, 📚 Course Name, 🔗 Link
5. Click "Send to All Students"
6. Confirm: "Send to ALL students?"
7. Emails sent immediately!

#### 3. Monitor Progress

**Real-Time Updates:**
- Table refreshes every 1 second
- See "✓ Sent" status appear progressively
- Statistics update automatically
- Auto-refresh stops after 30 seconds

**Manual Refresh:**
- Click "🔄 Refresh" button anytime
- Stops auto-refresh
- Updates table immediately

#### 4. Manage Data

**Delete Single Student:**
- Click 🗑️ button next to student
- Confirm deletion

**Delete All Data:**
- Click "Delete All Data" button
- Double confirmation required
- All students removed

---

## 🔌 API Documentation

### Base URL:
```
http://127.0.0.1:8000/api/
```

### Endpoints:

#### 1. Upload Excel File
```http
POST /api/upload/
Content-Type: multipart/form-data

Parameters:
- file: Excel file (.xlsx, .xls)
- replace_all: boolean (optional, default: false)

Response:
{
  "message": "11 new students imported successfully!",
  "pending": 11,
  "info": "Use 'Create Template' button to send emails to 11 students."
}
```

**Example (cURL):**
```bash
curl -X POST http://127.0.0.1:8000/api/upload/ \
  -F "file=@students.xlsx" \
  -F "replace_all=false"
```

#### 2. Get All Students
```http
GET /api/students/

Response:
[
  {
    "id": 1,
    "name": "Raihan Islam",
    "email": "raihan@example.com",
    "mobile": "01712345678",
    "course_name": "Python Programming",
    "link": "https://course-link.com",
    "email_sent": false,
    "sms_sent": false,
    "template_sent": false
  },
  ...
]
```

#### 3. Send Custom Template
```http
POST /api/send-template/
Content-Type: application/json

Body:
{
  "subject": "Welcome to Python Course",
  "message": "Hello {name}, you are interested in {course_name}. Click {link}"
}

Response:
{
  "message": "Custom template sent to 11 students successfully!",
  "sent_count": 11,
  "template_id": 1
}
```

**Example (JavaScript):**
```javascript
fetch('/api/send-template/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    subject: 'Welcome to Python Course',
    message: 'Hello {name}, click {link}'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

#### 4. Delete Student
```http
DELETE /api/delete-student/<id>/

Response:
{
  "message": "Student Raihan Islam deleted successfully"
}
```

#### 5. Delete All Students
```http
DELETE /api/delete-all/

Response:
{
  "message": "All 11 students deleted successfully"
}
```

#### 6. Send All Emails (DISABLED)
```http
POST /api/send-emails/

Response:
{
  "error": "This feature is disabled. Please use 'Create Template' button to send custom emails.",
  "info": "Click 'Create Template' button, write your subject and message, then submit."
}
```

---

## 📧 Email Template System

### Placeholder System:

| Placeholder | Replaced With | Example |
|-------------|---------------|---------|
| `{name}` | Student name | Raihan Islam |
| `{course_name}` | Course name | Python Programming |
| `{link}` | Course link (as button) | 🚀 Click Here to Continue |

### Email Structure:

```html
┌─────────────────────────────────────┐
│         DARK NAVY HEADER            │
│    Innovative Skills BD             │
│    Transform Your Career...         │
├─────────────────────────────────────┤
│ ━━━━ Orange Decorative Line        │
│                                     │
│ Your custom message here...         │
│ with {name} and {course_name}       │
│                                     │
│ ┌───────────────────────────────┐  │
│ │  🚀 Click Here to Continue    │  │ ← {link} becomes button
│ └───────────────────────────────┘  │
│                                     │
│ ┌───────────────────────────────┐  │
│ │ 💡 Need Help?                 │  │
│ │ Contact us for assistance     │  │
│ └───────────────────────────────┘  │
├─────────────────────────────────────┤
│         DARK NAVY FOOTER            │
│                                     │
│ Best regards,                       │
│ Innovative Skills BD Team           │
│                                     │
│ 📧 info@innovativeskillsbd.com     │
│ 🌐 www.innovativeskillsbd.com      │
│                                     │
│ © 2026 Innovative Skills BD         │
└─────────────────────────────────────┘
```

### Design Specifications:

**Colors:**
- Header Background: `#0a1628` (Dark Navy Blue)
- Footer Background: `#0a1628` (Dark Navy Blue)
- Button Color: `#ff6b35` (Orange/Coral)
- Accent Color: `#ff6b35` (Orange/Coral)
- Text on Dark: `#ffffff` (White)
- Body Text: `#1a202c` (Dark Gray)

**Typography:**
- Heading: 34px, Bold
- Body: 17px, Regular
- Button: 18px, Bold
- Footer: 14px, Regular

**Responsive:**
- Desktop: 600px width
- Mobile: 100% width with adjusted padding
- Button: Large tap target (18px padding)

### Mobile Optimization:

```css
@media only screen and (max-width: 600px) {
  .email-container { width: 100% !important; }
  .mobile-padding { padding: 25px 20px !important; }
  .mobile-text { font-size: 15px !important; }
  .mobile-header { padding: 35px 20px !important; }
  .mobile-header h1 { font-size: 26px !important; }
}
```

---

## 🗄️ Database Schema

### Student Model:

```python
class Student(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    mobile = models.CharField(max_length=20, blank=True, null=True)
    course_name = models.CharField(max_length=200)
    link = models.URLField()
    email_sent = models.BooleanField(default=False)
    sms_sent = models.BooleanField(default=False)
    template_sent = models.BooleanField(default=False)
```

**Fields:**
- `name`: Student's full name
- `email`: Student's email address (unique identifier)
- `mobile`: Optional phone number
- `course_name`: Name of the course
- `link`: Course enrollment link
- `email_sent`: Email delivery status
- `sms_sent`: SMS delivery status (future feature)
- `template_sent`: Custom template sent status

### EmailTemplate Model:

```python
class EmailTemplate(models.Model):
    subject = models.CharField(max_length=500)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sent_count = models.IntegerField(default=0)
```

**Fields:**
- `subject`: Email subject line
- `message`: Email body with placeholders
- `created_at`: Template creation timestamp
- `sent_count`: Number of emails sent with this template

---

## 🏗️ Technical Architecture

### Project Structure:

```
email_project/
├── email_project/          # Main project settings
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # WSGI config
├── emails/                # Main app
│   ├── models.py          # Database models
│   ├── views.py           # API views
│   ├── serializers.py     # DRF serializers
│   ├── urls.py            # App URL routing
│   ├── templates/         # HTML templates
│   │   ├── index.html     # Main UI
│   │   └── emails/
│   │       └── course_enrollment.html
│   └── migrations/        # Database migrations
├── db.sqlite3             # SQLite database
├── manage.py              # Django management
└── requirements.txt       # Python dependencies
```

### Key Components:

#### 1. Views (emails/views.py):

**Main Views:**
- `home()` - Renders main UI
- `UploadStudentsView` - Handles Excel upload
- `StudentListView` - Returns student list
- `SendCustomTemplateView` - Sends custom emails
- `DeleteStudentView` - Deletes single student
- `DeleteAllStudentsView` - Deletes all students

**Helper Functions:**
- `send_course_email()` - Sends individual email
- `send_admin_confirmation()` - Admin notification
- `send_sms()` - SMS sending (placeholder)

#### 2. Frontend (templates/index.html):

**JavaScript Functions:**
- `loadStudents()` - Fetches and displays students
- `renderTable()` - Renders student table
- `updateStats()` - Updates statistics
- `startAutoRefresh()` - Starts real-time updates
- `stopAutoRefresh()` - Stops auto-refresh
- `showAlert()` - Displays notifications

**Features:**
- Drag & drop file upload
- Modal for custom templates
- Placeholder insertion buttons
- Auto-refresh mechanism
- Real-time table updates

#### 3. Email System:

**SMTP Configuration:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

**Email Sending:**
```python
email = EmailMultiAlternatives(
    subject=subject,
    body=text_message,
    from_email=settings.EMAIL_HOST_USER,
    to=[student.email]
)
email.attach_alternative(html_message, "text/html")
email.send(fail_silently=False)
```

### Data Flow:

```
User Action → Frontend (JavaScript)
     ↓
API Request → Backend (Django Views)
     ↓
Database Operation → SQLite
     ↓
Email Sending → Gmail SMTP
     ↓
Response → Frontend
     ↓
UI Update → User Sees Result
```

### Real-Time Update Mechanism:

```javascript
// Auto-refresh every 1 second for 30 seconds
setInterval(() => {
    loadStudents(); // Fetch updated data
    refreshCount++;
    if (refreshCount >= 30) {
        stopAutoRefresh();
    }
}, 1000);
```

---

## 🔧 Troubleshooting

### Common Issues:

#### 1. Emails Not Sending

**Problem:** Emails not being sent after template submission

**Solutions:**
- Check Gmail credentials in settings.py
- Verify App Password is correct
- Check internet connection
- Look for errors in terminal
- Verify Gmail account allows less secure apps

**Debug:**
```bash
# Check terminal output
python manage.py runserver
# Look for: ✅ Email sent to: email@example.com
```

#### 2. Excel Upload Fails

**Problem:** "Missing columns" error

**Solutions:**
- Ensure Excel has columns: Name, Email, Course Name, Link
- Column names are case-insensitive
- Check for empty rows
- Verify file format (.xlsx or .xls)

**Valid Column Names:**
- Name: "Name", "name", "NAME", "Student Name"
- Email: "Email", "email", "E-mail", "Mail"
- Course: "Course Name", "course_name", "Course"
- Link: "Link", "link", "URL", "Course Link"

#### 3. Table Not Updating

**Problem:** Real-time updates not working

**Solutions:**
- Check browser console for errors (F12)
- Verify JavaScript is enabled
- Clear browser cache
- Try manual refresh button
- Check network tab for API calls

#### 4. Button Not Clickable on Mobile

**Problem:** Email button not working on mobile devices

**Solutions:**
- Already fixed with table-based button structure
- Ensure email client shows images
- Check if link is valid URL
- Test in different email apps

#### 5. Database Errors

**Problem:** "no such table" error

**Solution:**
```bash
python manage.py migrate
```

**Problem:** Database locked

**Solution:**
```bash
# Stop server (Ctrl+C)
# Delete db.sqlite3
# Run migrations again
python manage.py migrate
python manage.py runserver
```

### Debug Mode:

Enable detailed logging in views.py:

```python
print(f"📧 Template submission received:")
print(f"   Subject: {subject}")
print(f"   Message: {message[:50]}...")
print(f"📊 Found {students.count()} students")
print(f"✅ Email sent to: {student.email}")
```

### Testing Checklist:

- [ ] Server running without errors
- [ ] Excel file uploads successfully
- [ ] Students appear in table
- [ ] Create template modal opens
- [ ] Placeholders insert correctly
- [ ] Template submits successfully
- [ ] Emails send (check terminal)
- [ ] Table updates in real-time
- [ ] Email received in inbox
- [ ] Button clickable on mobile
- [ ] Design looks good on all devices

---

## 📊 Performance & Scalability

### Current Limits:
- **Students:** Tested with 100+ students
- **Email Speed:** ~1 email per second
- **Database:** SQLite (suitable for < 1000 students)
- **Concurrent Users:** 1-5 (development server)

### Production Recommendations:

**For 1000+ Students:**
- Use PostgreSQL instead of SQLite
- Implement Celery for background tasks
- Use Redis for caching
- Deploy with Gunicorn + Nginx

**For High Volume:**
- Use email service (SendGrid, AWS SES)
- Implement rate limiting
- Add email queue system
- Monitor delivery rates

---

## 🔐 Security Best Practices

### Current Implementation:
- ✅ CSRF protection enabled
- ✅ TLS encryption for emails
- ✅ App Password (not plain password)
- ✅ Input validation
- ✅ XSS protection

### Recommendations:
- Use environment variables for secrets
- Enable HTTPS in production
- Implement user authentication
- Add API rate limiting
- Regular security updates

---

## 📝 License

MIT License - Free for personal and commercial use

---

## 👨‍💻 Developer Information

**Project:** Email Automation System
**Organization:** Innovative Skills BD
**Repository:** https://github.com/Raihanroo/Email_tamplate
**Developer:** Raihan
**Email:** raihanroo21@gmail.com
**Version:** 2.0
**Last Updated:** April 15, 2026

---

## 🎯 Quick Reference

### Start Server:
```bash
python manage.py runserver
```

### Access Application:
```
http://127.0.0.1:8000/
```

### API Base URL:
```
http://127.0.0.1:8000/api/
```

### Email Placeholders:
- `{name}` - Student name
- `{course_name}` - Course name
- `{link}` - Clickable button

### Brand Colors:
- Header/Footer: `#0a1628`
- Button/Accents: `#ff6b35`

---

**End of Documentation**

For additional support or questions, contact: raihanroo21@gmail.com

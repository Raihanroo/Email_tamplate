# 📧 Email Automation System - Complete Documentation

## 📋 Table of Contents
1. [Complete Project Summary](#complete-project-summary)
2. [Project Overview](#project-overview)
3. [Features](#features)
4. [Installation & Setup](#installation--setup)
5. [How to Use](#how-to-use)
6. [API Documentation](#api-documentation)
7. [Email Template System](#email-template-system)
8. [Database Schema](#database-schema)
9. [Technical Architecture](#technical-architecture)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 Complete Project Summary

### What This System Does:
Email Automation System for **Innovative Skills LTD** - Sends personalized course enrollment emails to students with complete manual control, custom templates, and real-time tracking.

### Core Workflow:

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERACTION FLOW                         │
└─────────────────────────────────────────────────────────────────┘

1. DATA INPUT (Two Methods):
   
   Method A: Excel Upload
   ├─ User uploads Excel file (.xlsx/.xls)
   ├─ Frontend: JavaScript reads file
   ├─ API Call: POST /api/upload/
   ├─ Backend: Django processes with pandas
   ├─ Database: Students saved to SQLite
   └─ Response: "11 students imported" (NO emails sent)
   
   Method B: Manual Data Entry (NEW)
   ├─ User clicks "Default Data Entry" button
   ├─ Modal opens with form
   ├─ Dropdowns show courses/links from existing data
   ├─ API Call: POST /api/add-student/
   ├─ Backend: Validates and saves single student
   └─ Response: Student added to table

2. DATA DISPLAY:
   ├─ API Call: GET /api/students/
   ├─ Backend: Fetches all students from database
   ├─ Frontend: Renders table with 8 columns
   ├─ Shows: Name, Email, Mobile, Course, Link, Status, Actions
   └─ Statistics: Total, Sent, Pending

3. EMAIL SENDING:
   ├─ User clicks "Create Template" button
   ├─ Modal opens with Subject + Message fields
   ├─ User writes: "Hello {name}, interested in {course_name}? {link}"
   ├─ Clicks placeholder buttons to insert: {name}, {course_name}, {link}
   ├─ Clicks "Send to All Students"
   ├─ API Call: POST /api/send-template/
   ├─ Backend Process:
   │  ├─ Fetches all students from database
   │  ├─ For each student:
   │  │  ├─ Replace {name} with student.name
   │  │  ├─ Replace {course_name} with student.course_name
   │  │  ├─ Replace {link} with HTML button containing student.link
   │  │  ├─ Create beautiful HTML email
   │  │  ├─ Send via Gmail SMTP
   │  │  ├─ Update student.template_sent = True
   │  │  └─ Sleep 0.5 seconds (database commit)
   │  └─ Return: "Sent to 11 students"
   └─ Frontend: Starts auto-refresh

4. REAL-TIME UPDATES:
   ├─ Auto-refresh starts (every 1 second)
   ├─ API Call: GET /api/students/ (repeated)
   ├─ Backend: Returns updated student list
   ├─ Frontend: Updates table progressively
   ├─ Shows: "✓ Sent" status appearing one by one
   └─ Stops after 30 seconds

5. DATA MANAGEMENT:
   ├─ Delete Single: DELETE /api/delete-student/<id>/
   ├─ Delete All: DELETE /api/delete-all/
   └─ Refresh: GET /api/students/
```

### Complete API Flow Diagram:

```
┌──────────────┐
│   FRONTEND   │ (HTML + JavaScript)
│  index.html  │
└──────┬───────┘
       │
       │ HTTP Requests (Fetch API)
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│                    DJANGO BACKEND                         │
│                                                           │
│  ┌────────────────────────────────────────────────────┐  │
│  │              URL ROUTING (urls.py)                 │  │
│  │                                                     │  │
│  │  /                    → home()                     │  │
│  │  /api/upload/         → UploadStudentsView        │  │
│  │  /api/students/       → StudentListView           │  │
│  │  /api/send-template/  → SendCustomTemplateView    │  │
│  │  /api/add-student/    → AddStudentView (NEW)      │  │
│  │  /api/delete-student/ → DeleteStudentView         │  │
│  │  /api/delete-all/     → DeleteAllStudentsView     │  │
│  └────────────────────────────────────────────────────┘  │
│                          │                                │
│                          ▼                                │
│  ┌────────────────────────────────────────────────────┐  │
│  │              VIEWS (views.py)                      │  │
│  │                                                     │  │
│  │  Class UploadStudentsView:                        │  │
│  │    - Receives Excel file                          │  │
│  │    - Uses pandas to read data                     │  │
│  │    - Validates columns                            │  │
│  │    - Creates Student objects                      │  │
│  │    - Returns success message                      │  │
│  │                                                     │  │
│  │  Class StudentListView:                           │  │
│  │    - Queries all students                         │  │
│  │    - Serializes data                              │  │
│  │    - Returns JSON array                           │  │
│  │                                                     │  │
│  │  Class SendCustomTemplateView:                    │  │
│  │    - Receives subject + message                   │  │
│  │    - Fetches all students                         │  │
│  │    - For each student:                            │  │
│  │      • Replace placeholders                       │  │
│  │      • Convert {link} to HTML button              │  │
│  │      • Create HTML email                          │  │
│  │      • Send via SMTP                              │  │
│  │      • Update template_sent flag                  │  │
│  │    - Returns sent count                           │  │
│  │                                                     │  │
│  │  Class AddStudentView (NEW):                      │  │
│  │    - Receives student data (JSON)                 │  │
│  │    - Validates required fields                    │  │
│  │    - Checks duplicate email                       │  │
│  │    - Creates Student object                       │  │
│  │    - Returns success + student data               │  │
│  │                                                     │  │
│  │  Class DeleteStudentView:                         │  │
│  │    - Receives student ID                          │  │
│  │    - Deletes from database                        │  │
│  │    - Returns confirmation                         │  │
│  │                                                     │  │
│  │  Class DeleteAllStudentsView:                     │  │
│  │    - Deletes all students                         │  │
│  │    - Returns deleted count                        │  │
│  └────────────────────────────────────────────────────┘  │
│                          │                                │
│                          ▼                                │
│  ┌────────────────────────────────────────────────────┐  │
│  │           DATABASE (models.py)                     │  │
│  │                                                     │  │
│  │  Student Model:                                    │  │
│  │    - id (Primary Key)                             │  │
│  │    - name (CharField)                             │  │
│  │    - email (EmailField)                           │  │
│  │    - mobile (CharField, optional)                 │  │
│  │    - course_name (CharField)                      │  │
│  │    - link (URLField)                              │  │
│  │    - email_sent (Boolean, default=False)          │  │
│  │    - sms_sent (Boolean, default=False)            │  │
│  │    - template_sent (Boolean, default=False)       │  │
│  │                                                     │  │
│  │  EmailTemplate Model:                             │  │
│  │    - id (Primary Key)                             │  │
│  │    - subject (CharField)                          │  │
│  │    - message (TextField)                          │  │
│  │    - created_at (DateTime)                        │  │
│  │    - sent_count (Integer)                         │  │
│  └────────────────────────────────────────────────────┘  │
│                          │                                │
│                          ▼                                │
│                   SQLite Database                         │
│                    (db.sqlite3)                           │
└───────────────────────────────────────────────────────────┘
                           │
                           │ SMTP Connection
                           ▼
                  ┌─────────────────┐
                  │   Gmail SMTP    │
                  │  smtp.gmail.com │
                  │    Port: 587    │
                  │   TLS Enabled   │
                  └────────┬────────┘
                           │
                           │ Email Delivery
                           ▼
                  ┌─────────────────┐
                  │  Student Inbox  │
                  │  (Recipient)    │
                  └─────────────────┘
```

### All Features & Functions:

#### 1. Excel Upload Feature
**Frontend:**
- Drag & drop area with visual feedback
- File validation (.xlsx, .xls only)
- Replace all checkbox option
- Upload button (disabled until file selected)

**Backend (UploadStudentsView):**
```python
def post(self, request):
    1. Receive file from request.FILES
    2. Read Excel with pandas.read_excel()
    3. Normalize column names (lowercase, strip spaces)
    4. Validate required columns exist
    5. Check replace_all flag
    6. If replace_all: Delete all existing students
    7. For each row:
       - Extract: name, email, mobile, course_name, link
       - Create Student object
       - Save to database
    8. Return: success message + count
```

**API Call:**
```javascript
const formData = new FormData();
formData.append('file', selectedFile);
formData.append('replace_all', replaceAll);

fetch('/api/upload/', {
    method: 'POST',
    body: formData
})
```

#### 2. Manual Data Entry Feature (NEW)
**Frontend:**
- "Default Data Entry" button
- Modal with form fields
- Dropdowns populated from existing data
- Submit button with validation

**Backend (AddStudentView):**
```python
def post(self, request):
    1. Receive JSON data
    2. Validate required fields (name, email, course_name, link)
    3. Check if email already exists
    4. Create new Student object
    5. Save to database
    6. Return: success + student data
```

**API Call:**
```javascript
fetch('/api/add-student/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        name: 'Raihan',
        email: 'raihan@example.com',
        mobile: '01712345678',
        course_name: 'Python Programming',
        link: 'https://course-link.com'
    })
})
```

**Dropdown Population:**
```javascript
function populateDropdowns() {
    // Collect unique courses from loaded students
    availableCourses.forEach(course => {
        courseSelect.add(new Option(course, course));
    });
    
    // Collect unique links from loaded students
    availableLinks.forEach(link => {
        linkSelect.add(new Option(link, link));
    });
}
```

#### 3. Student List Display
**Frontend:**
- Table with 8 columns
- Status badges (✓ Sent / ⏳ Not Sent)
- Action buttons (Delete)
- Empty state when no data

**Backend (StudentListView):**
```python
def get(self, request):
    1. Query all students: Student.objects.all()
    2. Serialize with StudentSerializer
    3. Return JSON array
```

**API Call:**
```javascript
fetch('/api/students/')
    .then(response => response.json())
    .then(students => {
        renderTable(students);
        updateStats(students);
        collectCoursesAndLinks(students);
    })
```

#### 4. Custom Email Template
**Frontend:**
- "Create Template" button
- Modal with Subject + Message fields
- Placeholder buttons: {name}, {course_name}, {link}
- Insert placeholders at cursor position
- Send to All Students button

**Backend (SendCustomTemplateView):**
```python
def post(self, request):
    1. Receive subject + message
    2. Save to EmailTemplate model
    3. Fetch all students
    4. For each student:
       a. Replace {name} with student.name
       b. Replace {course_name} with student.course_name
       c. Replace {link} with HTML button:
          <table><tr><td>
            <a href="student.link">
              🚀 Click Here to Continue
            </a>
          </td></tr></table>
       d. Create full HTML email with:
          - Dark navy header (#0a1628)
          - Orange button (#ff6b35)
          - Professional design
          - Mobile-responsive
       e. Send via EmailMultiAlternatives
       f. Update student.template_sent = True
       g. Sleep 0.5 seconds (database commit)
    5. Return: sent count
```

**Email HTML Structure:**
```html
<html>
  <head>
    <meta name="viewport" content="width=device-width">
    <style>/* Mobile-responsive CSS */</style>
  </head>
  <body>
    <table width="600" style="max-width:600px">
      <!-- Header: Dark Navy -->
      <tr bgcolor="#0a1628">
        <td>
          <h1>Innovative Skills LTD</h1>
          <p>Transform Your Career</p>
        </td>
      </tr>
      
      <!-- Body: White -->
      <tr bgcolor="#ffffff">
        <td>
          <p>Hello Raihan,</p>
          <p>Your custom message here...</p>
          
          <!-- Button: Orange -->
          <table>
            <tr>
              <td bgcolor="#ff6b35" style="border-radius:50px">
                <a href="https://course-link.com">
                  🚀 Click Here to Continue
                </a>
              </td>
            </tr>
          </table>
        </td>
      </tr>
      
      <!-- Footer: Dark Navy -->
      <tr bgcolor="#0a1628">
        <td>
          <p>Best regards,<br>Innovative Skills LTD Team</p>
          <p>© 2026 Innovative Skills LTD</p>
        </td>
      </tr>
    </table>
  </body>
</html>
```

**API Call:**
```javascript
fetch('/api/send-template/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        subject: 'Welcome to Python Course',
        message: 'Hello {name}, click {link}'
    })
})
```

#### 5. Real-Time Table Updates
**Frontend:**
```javascript
function startAutoRefresh() {
    let refreshCount = 0;
    autoRefreshInterval = setInterval(() => {
        loadStudents(); // Fetch updated data
        refreshCount++;
        if (refreshCount >= 30) {
            stopAutoRefresh(); // Stop after 30 seconds
        }
    }, 1000); // Every 1 second
}
```

**Flow:**
```
Template Submitted
    ↓
Backend starts sending emails
    ↓
Frontend starts auto-refresh (1 second interval)
    ↓
Every second:
  - Fetch /api/students/
  - Update table
  - Show "✓ Sent" for completed emails
    ↓
After 30 seconds: Stop auto-refresh
```

#### 6. Delete Operations
**Single Delete:**
```python
# Backend
def delete(self, request, student_id):
    student = Student.objects.get(id=student_id)
    name = student.name
    student.delete()
    return Response({'message': f'Student {name} deleted'})
```

```javascript
// Frontend
function deleteStudent(id, name) {
    if (!confirm(`Delete ${name}?`)) return;
    fetch(`/api/delete-student/${id}/`, {method: 'DELETE'})
        .then(() => loadStudents());
}
```

**Delete All:**
```python
# Backend
def delete(self, request):
    count = Student.objects.count()
    Student.objects.all().delete()
    return Response({'message': f'All {count} students deleted'})
```

### Key Technical Decisions:

1. **Manual Control (No Auto-Send):**
   - Excel upload ONLY saves data
   - Emails sent ONLY via "Create Template"
   - Gives user complete control

2. **Real-Time Updates:**
   - Auto-refresh every 1 second
   - Shows progressive status updates
   - Stops after 30 seconds to save resources

3. **{link} as Button:**
   - Converts to HTML table-based button
   - Mobile-friendly (large tap target)
   - Professional design with brand colors

4. **Brand Colors:**
   - Header/Footer: Dark Navy (#0a1628)
   - Button/Accents: Orange (#ff6b35)
   - Consistent across all emails

5. **Dropdown Population (NEW):**
   - Collects unique courses/links from existing students
   - Populates dropdowns automatically
   - Reduces typing errors

### Data Flow Summary:

```
USER INPUT → FRONTEND (JavaScript) → API (Django REST) → 
DATABASE (SQLite) → BACKEND PROCESSING → EMAIL (SMTP) → 
RECIPIENT INBOX → FRONTEND UPDATE → USER SEES RESULT
```

### Complete Feature List:

✅ Excel file upload (drag & drop)
✅ Manual data entry with dropdowns (NEW)
✅ Student list display (table)
✅ Custom email templates
✅ Placeholder system ({name}, {course_name}, {link})
✅ {link} converts to clickable button
✅ Real-time table updates
✅ Email status tracking
✅ Statistics dashboard
✅ Delete single student
✅ Delete all students
✅ Mobile-responsive emails
✅ Brand-consistent design
✅ Manual email control
✅ Error handling
✅ Input validation
✅ Duplicate email check (NEW)

---

## 🎯 Project Overview

**Innovative Skills LTD Email Automation System** - A Django-based email automation platform for sending personalized course enrollment emails to students.

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
   Innovative Skills LTD
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
│    Innovative Skills LTD            │
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
│ Innovative Skills LTD Team          │
│                                     │
│ 📧 info@innovativeskillsbd.com     │
│ 🌐 www.innovativeskillsbd.com      │
│                                     │
│ © 2026 Innovative Skills LTD        │
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
**Organization:** Innovative Skills LTD
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

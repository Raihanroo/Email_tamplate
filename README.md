# 📧 Email Automation System - Innovative Skills BD

Professional email automation system for sending personalized course enrollment emails with custom templates and real-time tracking.

![Django](https://img.shields.io/badge/Django-5.2.1-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

---

## ✨ Key Features

- 📤 **Excel Upload** - Import student data instantly
- ✉️ **Custom Templates** - Create personalized emails with placeholders
- 🔘 **Smart Buttons** - `{link}` placeholder becomes clickable button
- 📱 **Mobile Optimized** - Perfect on all devices
- 🔄 **Real-Time Updates** - See email status update live
- 🎨 **Brand Colors** - Dark navy blue + orange design
- 🎯 **Manual Control** - Send emails only when you want

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Email
Edit `email_project/settings.py`:
```python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

Get App Password: https://myaccount.google.com/apppasswords

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Start Server
```bash
python manage.py runserver
```

### 5. Open Browser
```
http://127.0.0.1:8000/
```

---

## 📖 How to Use

### Step 1: Upload Excel File
- Drag & drop Excel file with columns: Name, Email, Mobile, Course Name, Link
- Data saved to database
- **NO emails sent yet**

### Step 2: Create Custom Template
- Click "Create Template" button
- Write subject and message
- Use placeholders:
  - `{name}` → Student name
  - `{course_name}` → Course name
  - `{link}` → Clickable button
- Click "Send to All Students"

### Step 3: Monitor Progress
- Table auto-refreshes every 1 second
- See "✓ Sent" status appear in real-time
- Statistics update automatically

---

## 📋 Excel File Format

| Name | Email | Mobile | Course Name | Link |
|------|-------|--------|-------------|------|
| Raihan Islam | raihan@example.com | 01712345678 | Python Programming | https://... |
| Kabir Hossain | kabir@example.com | 01812345678 | Web Development | https://... |

**Required:** Name, Email, Course Name, Link  
**Optional:** Mobile

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main UI page |
| `/api/upload/` | POST | Upload Excel file |
| `/api/students/` | GET | Get all students |
| `/api/send-template/` | POST | Send custom template |
| `/api/delete-student/<id>/` | DELETE | Delete student |
| `/api/delete-all/` | DELETE | Delete all students |

---

## 📧 Email Template

### Design:
```
┌─────────────────────────────┐
│   DARK NAVY HEADER          │
│   Innovative Skills BD      │
├─────────────────────────────┤
│ Your custom message...      │
│                             │
│ [🚀 Click Here to Continue] │ ← Orange button
│                             │
│ ┌─────────────────────┐     │
│ │ 💡 Need Help?       │     │
│ └─────────────────────┘     │
├─────────────────────────────┤
│   DARK NAVY FOOTER          │
│   Contact Information       │
└─────────────────────────────┘
```

### Colors:
- **Header/Footer:** `#0a1628` (Dark Navy Blue)
- **Button/Accents:** `#ff6b35` (Orange/Coral)
- **Text:** `#ffffff` (White on dark)

---

## 🗄️ Database Models

### Student:
```python
- name: CharField
- email: EmailField
- mobile: CharField (optional)
- course_name: CharField
- link: URLField
- email_sent: BooleanField
- template_sent: BooleanField
```

### EmailTemplate:
```python
- subject: CharField
- message: TextField
- created_at: DateTimeField
- sent_count: IntegerField
```

---

## 🛠️ Tech Stack

- **Backend:** Django 5.2.1, Django REST Framework
- **Database:** SQLite (dev), PostgreSQL (prod)
- **Email:** Gmail SMTP with TLS
- **Frontend:** HTML5, CSS3, JavaScript
- **Data:** pandas, openpyxl

---

## 📊 Workflow

```
Upload Excel → Data Saved (No Email)
     ↓
Create Template → Write Subject & Message
     ↓
Use Placeholders → {name}, {course_name}, {link}
     ↓
Submit Template → Emails Sent to ALL
     ↓
Real-Time Updates → Table Refreshes Every 1s
     ↓
Monitor Progress → See "✓ Sent" Status
```

---

## 🎯 Key Highlights

### Manual Email Control:
- ✅ Excel upload does NOT send emails
- ✅ Emails sent ONLY via custom template
- ✅ Full control over timing
- ✅ No automatic background sending

### Real-Time Updates:
- ✅ Table refreshes every 1 second
- ✅ See progressive "✓ Sent" status
- ✅ Auto-stops after 30 seconds
- ✅ Manual refresh available

### Mobile-Friendly Button:
- ✅ `{link}` becomes clickable button
- ✅ Works on all email clients
- ✅ Large tap target for mobile
- ✅ Orange color matches brand

---

## 🔧 Configuration

### Email Settings (settings.py):
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Required Packages (requirements.txt):
```
Django==5.2.1
djangorestframework==3.14.0
pandas==2.0.3
openpyxl==3.1.2
```

---

## 📚 Documentation

**Complete Documentation:** See `PROJECT_DOCUMENTATION.md` for:
- Detailed API documentation
- Email template system
- Database schema
- Technical architecture
- Troubleshooting guide
- Performance tips

---

## 🐛 Troubleshooting

### Emails Not Sending?
- Check Gmail credentials
- Verify App Password
- Check internet connection
- Look for errors in terminal

### Excel Upload Fails?
- Ensure required columns exist
- Check for empty rows
- Verify file format (.xlsx or .xls)

### Table Not Updating?
- Check browser console (F12)
- Try manual refresh button
- Clear browser cache

---

## 🔐 Security

- ✅ CSRF protection enabled
- ✅ TLS encryption for emails
- ✅ App Password authentication
- ✅ Input validation
- ✅ XSS protection

---

## 📈 Performance

- **Upload Speed:** 100 rows in < 5 seconds
- **Email Speed:** ~1 email per second
- **Database:** Handles 1000+ students
- **Response Time:** < 1 second

---

## 🚀 Deployment

### Production Checklist:
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use environment variables
- [ ] Setup PostgreSQL
- [ ] Configure static files
- [ ] Use Gunicorn + Nginx
- [ ] Setup SSL certificate

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

---

## 📧 Support

**Repository:** https://github.com/Raihanroo/Email_tamplate  
**Developer:** Raihan  
**Email:** raihanroo21@gmail.com

For issues or questions, open an issue on GitHub.

---

## 📝 License

MIT License - Free for personal and commercial use

---

## 🎯 Use Cases

- Course enrollment campaigns
- Event invitations
- Newsletter distribution
- Marketing campaigns
- Student notifications
- Bulk email management

---

## ⭐ Features Highlight

✅ Manual email control (no auto-send)  
✅ Custom email templates  
✅ {link} converts to clickable button  
✅ Real-time table updates  
✅ Mobile-responsive design  
✅ Brand-consistent colors  
✅ Excel file upload  
✅ Flexible column detection  
✅ Statistics dashboard  
✅ Production ready  

---

## 📸 Screenshots

### Main Dashboard
- Upload section with drag & drop
- Statistics cards (Total, Sent, Pending)
- Student table with status
- Action buttons

### Custom Template Modal
- Subject input
- Message textarea
- Placeholder buttons
- Send to All button

### Email Preview
- Dark navy header
- Custom message
- Orange clickable button
- Professional footer

---

**Version:** 2.0  
**Last Updated:** April 15, 2026  
**Status:** Production Ready ✅

---

**Happy Emailing! 📧**

*Built with ❤️ using Django and modern web technologies*

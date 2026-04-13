from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
import pandas as pd
import time
import requests
import threading

from .models import Student
from .serializers import StudentSerializer

# Rate limiting: 20 emails per hour
EMAILS_PER_HOUR = 20
EMAIL_DELAY_SECONDS = 3600 / EMAILS_PER_HOUR  # 180 seconds = 3 minutes between emails


def send_emails_in_background():
    """Background thread to send pending emails continuously"""
    while True:
        try:
            # Get pending students (limit 20)
            students = Student.objects.filter(email_sent=False)[:EMAILS_PER_HOUR]
            
            if not students.exists():
                # No pending emails, wait 5 minutes and check again
                time.sleep(300)
                continue
            
            # Send emails with delay
            for student in students:
                try:
                    send_course_email(student)
                    student.email_sent = True
                    student.save()
                    print(f"✅ Email sent to {student.email}")
                    
                    # Wait 3 minutes before next email
                    time.sleep(EMAIL_DELAY_SECONDS)
                except Exception as e:
                    print(f"❌ Failed to send to {student.email}: {str(e)}")
                    
        except Exception as e:
            print(f"Background task error: {str(e)}")
            time.sleep(60)  # Wait 1 minute on error


# Start background thread when module loads
background_thread = threading.Thread(target=send_emails_in_background, daemon=True)
background_thread.start()


def send_sms(mobile, name, course_name, link):
    """Helper function to send SMS (using SMS API)"""
    # Note: You need to configure SMS API credentials
    # Popular options: Twilio, Nexmo, BulkSMS, etc.
    
    message = f"Dear {name}, You are interested in {course_name}. Enroll now: {link}"
    
    # Example with a generic SMS API (replace with your actual API)
    try:
        # Uncomment and configure when you have SMS API
        # api_url = "https://api.sms-provider.com/send"
        # payload = {
        #     'api_key': 'YOUR_API_KEY',
        #     'to': mobile,
        #     'message': message
        # }
        # response = requests.post(api_url, json=payload)
        # return response.status_code == 200
        
        # For now, just log (remove this in production)
        print(f"SMS would be sent to {mobile}: {message}")
        return True
    except Exception as e:
        print(f"SMS Error: {str(e)}")
        return False


def send_admin_confirmation(student):
    """Send confirmation email to admin when student email is sent"""
    subject = f"✅ Email Sent Successfully - {student.name}"
    
    text_message = f"""Email Delivery Confirmation

Student email has been sent successfully!

Student Details:
- Name: {student.name}
- Email: {student.email}
- Mobile: {student.mobile or 'N/A'}
- Course: {student.course_name}

Email Status: ✅ Sent
SMS Status: {'✅ Sent' if student.sms_sent else '⏳ Pending' if student.mobile else 'N/A'}

This is an automated confirmation from Email Automation System.
"""

    html_message = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }}
        .container {{ background: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px; }}
        .content {{ color: #333; line-height: 1.6; }}
        .info-box {{ background: #f8f9fa; padding: 15px; border-left: 4px solid #11998e; margin: 20px 0; border-radius: 5px; }}
        .status {{ display: inline-block; padding: 5px 15px; border-radius: 20px; font-size: 14px; font-weight: bold; margin: 5px 0; }}
        .status-success {{ background: #d4edda; color: #155724; }}
        .status-pending {{ background: #fff3cd; color: #856404; }}
        .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #e9ecef; color: #999; font-size: 12px; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>✅ Email Sent Successfully</h2>
        </div>
        <div class="content">
            <p><strong>Student email has been delivered!</strong></p>
            <div class="info-box">
                <p><strong>Name:</strong> {student.name}</p>
                <p><strong>Email:</strong> {student.email}</p>
                <p><strong>Mobile:</strong> {student.mobile or 'N/A'}</p>
                <p><strong>Course:</strong> {student.course_name}</p>
            </div>
            <p><strong>Delivery Status:</strong></p>
            <p>
                <span class="status status-success">✅ Email Sent</span>
                {'<span class="status status-success">✅ SMS Sent</span>' if student.sms_sent else '<span class="status status-pending">⏳ SMS Pending</span>' if student.mobile else ''}
            </p>
            <div class="footer">
                <p>This is an automated confirmation from Email Automation System.</p>
                <p>Sent at: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_HOST_USER]  # Send to yourself
        )
        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=True)  # Don't fail if admin email fails
    except Exception as e:
        print(f"Admin notification error: {str(e)}")


def home(request):
    """Home page with UI"""
    return render(request, 'index.html')


def send_course_email(student):
    """Helper function to send course enrollment email"""
    subject = f"You're Interested in {student.course_name} – Enroll Now!"
    
    text_message = f"""Dear {student.name},

You are interested in {student.course_name}.

Please click the link below to enroll:
{student.link}

Best regards,
Innovative Skills BD"""

    html_message = render_to_string('emails/course_enrollment.html', {
        'name': student.name,
        'course_name': student.course_name,
        'link': student.link,
    })

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_message,
        from_email=settings.EMAIL_HOST_USER,
        to=[student.email]
    )
    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)


class UploadStudentsView(APIView):
    """Upload Excel file - emails will be sent automatically in background"""
    
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded'}, status=400)

        try:
            df = pd.read_excel(file)
        except Exception as e:
            return Response({'error': f'Failed to read Excel file: {str(e)}'}, status=400)

        # Flexible column mapping - case insensitive
        column_mapping = {}
        df_columns = df.columns.str.strip().str.lower()
        
        # Map columns flexibly
        for col in df.columns:
            col_lower = col.strip().lower()
            if 'name' in col_lower and 'course' not in col_lower:
                column_mapping['Name'] = col
            elif 'email' in col_lower or 'mail' in col_lower:
                column_mapping['Email'] = col
            elif 'mobile' in col_lower or 'phone' in col_lower or 'number' in col_lower:
                column_mapping['Mobile'] = col
            elif 'course' in col_lower:
                column_mapping['Course Name'] = col
            elif 'link' in col_lower or 'url' in col_lower:
                column_mapping['Link'] = col
        
        # Check required columns
        required_columns = ['Name', 'Email', 'Course Name', 'Link']
        missing_columns = [col for col in required_columns if col not in column_mapping]
        if missing_columns:
            available_cols = ', '.join(df.columns.tolist())
            return Response({
                'error': f'Missing columns: {", ".join(missing_columns)}',
                'available_columns': available_cols,
                'hint': 'Column names should contain: name, email, course, link'
            }, status=400)

        imported = 0
        skipped_rows = 0

        for index, row in df.iterrows():
            try:
                # Get values using mapped column names
                name = row[column_mapping['Name']] if 'Name' in column_mapping else None
                email = row[column_mapping['Email']] if 'Email' in column_mapping else None
                course_name = row[column_mapping['Course Name']] if 'Course Name' in column_mapping else None
                link = row[column_mapping['Link']] if 'Link' in column_mapping else None
                mobile = row[column_mapping.get('Mobile', '')] if 'Mobile' in column_mapping and not pd.isna(row.get(column_mapping.get('Mobile', ''))) else None
                
                # Check if all required fields are present and not empty
                if pd.isna(name) or pd.isna(email) or pd.isna(course_name) or pd.isna(link):
                    skipped_rows += 1
                    continue
                
                # Check if fields are not empty strings
                if not str(name).strip() or not str(email).strip() or not str(course_name).strip() or not str(link).strip():
                    skipped_rows += 1
                    continue
                
                student, created = Student.objects.get_or_create(
                    email=email,
                    defaults={
                        'name': name,
                        'course_name': course_name,
                        'link': link,
                        'mobile': str(mobile).strip() if mobile else None,
                    }
                )
                
                if created:
                    imported += 1
                        
            except Exception as e:
                return Response({'error': f'Error processing row: {str(e)}'}, status=400)

        pending_count = Student.objects.filter(email_sent=False).count()
        
        response_data = {
            'message': f'{imported} new students imported! Emails will be sent automatically in background.',
            'pending': pending_count,
            'info': f'Background system will send 20 emails per hour automatically. {pending_count} emails in queue.'
        }
        
        if skipped_rows > 0:
            response_data['warning'] = f'{skipped_rows} incomplete rows skipped'
            
        return Response(response_data)


class StudentListView(APIView):
    """Get all students"""
    
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


class SendEmailsView(APIView):
    """Send emails to pending students (20 per hour rate limit)"""
    
    def post(self, request):
        students = Student.objects.filter(email_sent=False)[:EMAILS_PER_HOUR]
        
        if not students.exists():
            return Response({'message': 'No pending emails to send'})
        
        sent = 0
        failed_emails = []

        for student in students:
            try:
                send_course_email(student)
                student.email_sent = True
                student.save()
                sent += 1
                
                # Add delay between emails (3 minutes)
                if sent < len(students):
                    time.sleep(EMAIL_DELAY_SECONDS)
            except Exception as e:
                failed_emails.append(f"{student.email}: {str(e)}")

        pending_count = Student.objects.filter(email_sent=False).count()
        
        response_data = {
            'message': f'{sent} emails sent successfully!',
            'pending': pending_count,
            'info': f'{pending_count} emails still pending. Will send 20 per hour.'
        }
        if failed_emails:
            response_data['failed_emails'] = failed_emails
            
        return Response(response_data)



class SendSingleEmailView(APIView):
    """Send email to a single student"""
    
    def post(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
            
            if student.email_sent:
                return Response({'error': 'Email already sent to this student'}, status=400)
            
            try:
                send_course_email(student)
                student.email_sent = True
                student.save()
                return Response({'message': f'Email sent successfully to {student.email}'})
            except Exception as e:
                return Response({'error': f'Failed to send email: {str(e)}'}, status=500)
                
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)



class NotifyAdminView(APIView):
    """Send notification to admin when someone clicks a course link"""
    
    def post(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
            
            # Send notification to admin
            subject = f"🔔 Course Link Clicked - {student.name}"
            
            text_message = f"""Admin Notification:

Student {student.name} ({student.email}) clicked on the course link.

Course: {student.course_name}
Link: {student.link}

This is an automated notification from Email Automation System.
"""

            html_message = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }}
        .container {{ background: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px; }}
        .content {{ color: #333; line-height: 1.6; }}
        .info-box {{ background: #f8f9fa; padding: 15px; border-left: 4px solid #667eea; margin: 20px 0; }}
        .link-btn {{ display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 30px; text-decoration: none; border-radius: 50px; margin-top: 15px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>🔔 Course Link Clicked</h2>
        </div>
        <div class="content">
            <p><strong>Student Details:</strong></p>
            <div class="info-box">
                <p><strong>Name:</strong> {student.name}</p>
                <p><strong>Email:</strong> {student.email}</p>
                <p><strong>Course:</strong> {student.course_name}</p>
            </div>
            <p>The student clicked on the course enrollment link.</p>
            <a href="{student.link}" class="link-btn">View Course Page</a>
            <p style="margin-top: 20px; color: #999; font-size: 12px;">
                This is an automated notification from Email Automation System.
            </p>
        </div>
    </div>
</body>
</html>
"""

            try:
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=text_message,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[settings.EMAIL_HOST_USER]  # Send to admin (yourself)
                )
                email.attach_alternative(html_message, "text/html")
                email.send(fail_silently=False)
                
                return Response({'message': 'Notification sent to admin', 'link': student.link})
            except Exception as e:
                return Response({'error': f'Failed to send notification: {str(e)}'}, status=500)
                
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)



class DeleteStudentView(APIView):
    """Delete a single student"""
    
    def delete(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
            student_name = student.name
            student.delete()
            return Response({'message': f'Student {student_name} deleted successfully'})
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)


class DeleteAllStudentsView(APIView):
    """Delete all students"""
    
    def delete(self, request):
        count = Student.objects.count()
        Student.objects.all().delete()
        return Response({'message': f'All {count} students deleted successfully'})

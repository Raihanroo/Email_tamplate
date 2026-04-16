from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.shortcuts import render
import pandas as pd
import time

from .models import Student, EmailTemplate
from .serializers import StudentSerializer


def home(request):
    """Render main UI page"""
    return render(request, 'index.html')


def send_course_email(student):
    """Send course enrollment email to student"""
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
    """Upload Excel file and import student data"""
    
    def post(self, request):
        file = request.FILES.get('file')
        replace_all = request.POST.get('replace_all', 'false').lower() == 'true'
        
        if not file:
            return Response({'error': 'No file uploaded'}, status=400)

        deleted_count = 0
        if replace_all:
            deleted_count = Student.objects.count()
            Student.objects.all().delete()

        try:
            df = pd.read_excel(file)
        except Exception as e:
            return Response({'error': f'Failed to read Excel file: {str(e)}'}, status=400)

        column_mapping = {}
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
        
        required_columns = ['Name', 'Email', 'Course Name', 'Link']
        missing_columns = [col for col in required_columns if col not in column_mapping]
        if missing_columns:
            return Response({
                'error': f'Missing columns: {", ".join(missing_columns)}',
                'available_columns': ', '.join(df.columns.tolist()),
                'hint': 'Column names should contain: name, email, course, link'
            }, status=400)

        imported = 0
        skipped_rows = 0

        for index, row in df.iterrows():
            try:
                name = row[column_mapping['Name']] if 'Name' in column_mapping else None
                email = row[column_mapping['Email']] if 'Email' in column_mapping else None
                course_name = row[column_mapping['Course Name']] if 'Course Name' in column_mapping else None
                link = row[column_mapping['Link']] if 'Link' in column_mapping else None
                mobile = row[column_mapping.get('Mobile', '')] if 'Mobile' in column_mapping and not pd.isna(row.get(column_mapping.get('Mobile', ''))) else None
                
                if pd.isna(name) or pd.isna(email) or pd.isna(course_name) or pd.isna(link):
                    skipped_rows += 1
                    continue
                
                if not str(name).strip() or not str(email).strip() or not str(course_name).strip() or not str(link).strip():
                    skipped_rows += 1
                    continue
                
                if replace_all:
                    Student.objects.create(
                        email=email,
                        name=name,
                        course_name=course_name,
                        link=link,
                        mobile=str(mobile).strip() if mobile else None,
                    )
                    imported += 1
                else:
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
            'message': f'{imported} new students imported successfully!',
            'pending': pending_count,
            'info': f'Use "Create Template" button to send custom emails to {pending_count} students.'
        }
        
        if deleted_count > 0:
            response_data['deleted_count'] = deleted_count
            response_data['message'] = f'Deleted {deleted_count} old records. {imported} new students imported!'
        
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
    """Disabled - Use custom template instead"""
    
    def post(self, request):
        return Response({
            'error': 'This feature is disabled. Please use "Create Template" button to send custom emails.',
            'info': 'Click "Create Template" button, write your subject and message, then submit.'
        }, status=400)


class SendCustomTemplateView(APIView):
    """Send custom email template to all students"""
    
    def post(self, request):
        subject = request.data.get('subject', '').strip()
        message = request.data.get('message', '').strip()
        
        if not subject or not message:
            return Response({'error': 'Subject and message are required'}, status=400)
        
        template = EmailTemplate.objects.create(
            subject=subject,
            message=message
        )
        
        students = Student.objects.all()
        
        if not students.exists():
            return Response({'message': 'No students available to send template'})
        
        sent_count = 0
        failed_emails = []
        
        for student in students:
            try:
                personalized_subject = subject.replace('{name}', student.name)
                personalized_subject = personalized_subject.replace('{course_name}', student.course_name)
                personalized_subject = personalized_subject.replace('{link}', student.link)
                
                personalized_message = message.replace('{name}', student.name)
                personalized_message = personalized_message.replace('{course_name}', student.course_name)
                
                link_button_html = ''
                if '{link}' in personalized_message:
                    personalized_message = personalized_message.replace('{link}', '')
                    actual_link = student.link
                    link_button_html = f'''
                            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin: 35px 0 25px 0;">
                                <tr>
                                    <td align="center" style="padding: 0;">
                                        <table role="presentation" cellpadding="0" cellspacing="0" border="0">
                                            <tr>
                                                <td align="center" style="border-radius: 50px; background: #ff6b35; box-shadow: 0 6px 20px rgba(255, 107, 53, 0.4);">
                                                    <a href="{actual_link}" target="_blank" rel="noopener noreferrer" style="display: block; padding: 18px 50px; color: #ffffff; text-decoration: none; font-size: 18px; font-weight: bold; font-family: Arial, sans-serif; border-radius: 50px; -webkit-text-size-adjust: none; text-align: center; mso-padding-alt: 0; background: transparent;">
                                                        <span style="color: #ffffff; text-decoration: none;">🚀 Click Here to Continue</span>
                                                    </a>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                    '''
                
                html_message = f"""
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="x-apple-disable-message-reformatting">
    <meta name="format-detection" content="telephone=no,address=no,email=no,date=no,url=no">
    <title>{personalized_subject}</title>
    <style type="text/css">
        body {{
            margin: 0 !important;
            padding: 0 !important;
            -webkit-text-size-adjust: 100% !important;
            -ms-text-size-adjust: 100% !important;
            -webkit-font-smoothing: antialiased !important;
        }}
        table {{
            border-collapse: collapse !important;
            mso-table-lspace: 0pt !important;
            mso-table-rspace: 0pt !important;
        }}
        @media only screen and (max-width: 600px) {{
            .email-container {{ width: 100% !important; margin: auto !important; }}
            .mobile-padding {{ padding: 25px 20px !important; }}
            .mobile-text {{ font-size: 15px !important; line-height: 1.7 !important; }}
            .mobile-header {{ padding: 35px 20px !important; }}
            .mobile-header h1 {{ font-size: 26px !important; }}
        }}
        a {{ color: #ff6b35 !important; text-decoration: none !important; }}
        a[x-apple-data-detectors] {{
            color: inherit !important;
            text-decoration: none !important;
            font-size: inherit !important;
            font-family: inherit !important;
            font-weight: inherit !important;
            line-height: inherit !important;
        }}
        .button-link {{ color: #ffffff !important; text-decoration: none !important; }}
        .button-link span {{ color: #ffffff !important; text-decoration: none !important; }}
    </style>
</head>
<body style="margin: 0; padding: 0; font-family: Arial, Helvetica, sans-serif; background-color: #f0f2f5; width: 100% !important;">
    <div style="display: none; max-height: 0px; overflow: hidden;">{personalized_subject}</div>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f0f2f5; padding: 20px 0;">
        <tr>
            <td align="center" style="padding: 0;">
                <table role="presentation" class="email-container" width="600" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.15); max-width: 600px; margin: 0 auto;">
                    <tr>
                        <td class="mobile-header" style="background: #0a1628; padding: 50px 35px; text-align: center;">
                            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>
                                    <td align="center">
                                        <h1 style="color: #ffffff; margin: 0 0 12px 0; font-size: 34px; font-weight: bold; letter-spacing: -0.5px; line-height: 1.2;">Innovative Skills BD</h1>
                                        <p style="color: rgba(255,255,255,0.85); margin: 0; font-size: 16px; font-weight: 400; letter-spacing: 0.3px;">Transform Your Career with Expert Training</p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td class="mobile-padding" style="padding: 45px 40px;">
                            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>
                                    <td>
                                        <div style="width: 60px; height: 4px; background: #ff6b35; border-radius: 2px; margin-bottom: 25px;"></div>
                                        <div class="mobile-text" style="color: #1a202c; line-height: 1.8; font-size: 17px; white-space: pre-wrap; margin-bottom: 15px; font-family: Arial, Helvetica, sans-serif; font-weight: 400;">
{personalized_message}
                                        </div>
                                        {link_button_html}
                                        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top: 30px; background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%); border-radius: 12px; border-left: 4px solid #ff6b35;">
                                            <tr>
                                                <td style="padding: 20px 25px;">
                                                    <p style="margin: 0; color: #4a5568; font-size: 14px; line-height: 1.6;">
                                                        <strong style="color: #2d3748; font-size: 15px;">💡 Need Help?</strong><br>
                                                        If you have any questions, feel free to reach out to us. We're here to help you succeed!
                                                    </p>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 0 40px;">
                            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>
                                    <td style="height: 2px; background: linear-gradient(90deg, transparent 0%, #e2e8f0 50%, transparent 100%);"></td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td style="background: #0a1628; padding: 40px 35px; text-align: center;">
                            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>
                                    <td align="center">
                                        <p style="color: rgba(255,255,255,0.7); margin: 0 0 18px 0; font-size: 16px; line-height: 1.6; font-weight: 400;">
                                            Best regards,<br>
                                            <strong style="color: #ff6b35; font-weight: 700; font-size: 17px;">Innovative Skills BD Team</strong>
                                        </p>
                                        <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin: 20px auto;">
                                            <tr>
                                                <td style="padding: 8px 0;">
                                                    <p style="margin: 0; color: rgba(255,255,255,0.6); font-size: 14px; line-height: 1.8;">
                                                        📧 <a href="mailto:info@innovativeskillsbd.com" class="button-link" style="color: #ff6b35 !important; text-decoration: none; font-weight: 500;">info@innovativeskillsbd.com</a>
                                                    </p>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="padding: 8px 0;">
                                                    <p style="margin: 0; color: rgba(255,255,255,0.6); font-size: 14px; line-height: 1.8;">
                                                        🌐 <a href="https://www.innovativeskillsbd.com" target="_blank" class="button-link" style="color: #ff6b35 !important; text-decoration: none; font-weight: 500;">www.innovativeskillsbd.com</a>
                                                    </p>
                                                </td>
                                            </tr>
                                        </table>
                                        <p style="color: rgba(255,255,255,0.4); margin: 20px 0 0 0; font-size: 12px; line-height: 1.5;">
                                            © 2026 Innovative Skills BD. All rights reserved.<br>
                                            <span style="color: rgba(255,255,255,0.3); font-size: 11px;">This email was sent to you because you expressed interest in our courses.</span>
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""
                
                email = EmailMultiAlternatives(
                    subject=personalized_subject,
                    body=personalized_message,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[student.email]
                )
                email.attach_alternative(html_message, "text/html")
                email.send(fail_silently=False)
                
                student.email_sent = True
                student.template_sent = True
                student.save()
                sent_count += 1
                
                time.sleep(0.5)
                
            except Exception as e:
                failed_emails.append(f"{student.email}: {str(e)}")
        
        template.sent_count = sent_count
        template.save()
        
        response_data = {
            'message': f'Custom template sent to {sent_count} students successfully!',
            'sent_count': sent_count,
            'template_id': template.id
        }
        
        if failed_emails:
            response_data['failed_emails'] = failed_emails
        
        return Response(response_data)


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

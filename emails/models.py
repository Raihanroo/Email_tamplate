from django.db import models

class Student(models.Model):
    name        = models.CharField(max_length=200)
    email       = models.EmailField()
    mobile      = models.CharField(max_length=20, blank=True, null=True)
    course_name = models.CharField(max_length=200)
    link        = models.URLField()
    email_sent  = models.BooleanField(default=False)
    sms_sent    = models.BooleanField(default=False)
    template_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.course_name}"


class EmailTemplate(models.Model):
    subject = models.CharField(max_length=500)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sent_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.subject} - {self.sent_count} sent"
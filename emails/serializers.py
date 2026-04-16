from rest_framework import serializers
from .models import Student, EmailTemplate

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Student
        fields = '__all__'


class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = '__all__'
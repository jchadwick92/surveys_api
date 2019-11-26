from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import StudyRecord, StudyResponse

class StudyRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyRecord
        fields = ['survey_name', 'available_places', 'user_id']

class StudyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyResponse
        fields = ['user_id', 'created_at', 'survey_id']
import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import StudyRecord, StudyResponse
from ..serializers import StudyRecordSerializer, StudyResponseSerializer

client = Client()

class GetAllSurveyRecords(TestCase):
    def setUp(self):
        User.objects.create_user('testuser', "test@test.com", "pass1234")
        user = User.objects.get(email="test@test.com")
        StudyRecord.objects.create(survey_name = 'Test Survey', available_places = 10, user_id = user)
        StudyRecord.objects.create(survey_name = 'Test Survey 2', available_places = 11, user_id = user)
        StudyRecord.objects.create(survey_name = 'Test Survey 3', available_places = 12, user_id = user)

    def test_get_all_survey_records(self):
        response = client.get(reverse('get_post_study_records'))
        study_records = StudyRecord.objects.all()
        serializer = StudyRecordSerializer(study_records, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CreateNewSurveyRecordTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.user.set_password('password')
        self.user.save()
        client.login(username='testuser', password='password')

    def test_post_study_record_unauthorized(self):
        client.logout()
        response = client.post(reverse('get_post_study_records'), data=json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_post_valid_study_record(self):
        payload = {'survey_name': 'Test Post Survey', 'available_places': 1}

        response = client.post(reverse('get_post_study_records'), data=json.dumps(payload), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'survey_name': 'Test Post Survey', 'available_places': 1, 'user_id': self.user.id})
        
    def test_post_invalid_study_record(self):
        payload = {}

        response = client.post(reverse('get_post_study_records'), data=json.dumps(payload), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class CreateNewSurveyResponseTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.user.set_password('password')
        self.user.save()
        client.login(username='testuser', password='password')
        StudyRecord.objects.create(survey_name = 'Test Survey', available_places = 10, user_id = self.user)
        self.studyRecord = StudyRecord.objects.get(survey_name = 'Test Survey')
    
    def test_post_valid_study_response(self):
        payload = {'survey_id': self.studyRecord.id}

        response = client.post(reverse('get_post_study_responses'), data=json.dumps(payload), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['survey_id'], self.studyRecord.id)
        self.assertEqual(response.data['user_id'], self.user.id)
        # test created_at

    def test_post_invalid_study_response(self):
        payload = {}

        response = client.post(reverse('get_post_study_responses'), data=json.dumps(payload), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_study_response_when_study_record_full(self):
        StudyRecord.objects.create(survey_name = 'Single available place', available_places = 1, user_id = self.user)
        studyRecord = StudyRecord.objects.get(survey_name = 'Single available place')
        StudyResponse.objects.create(survey_id=studyRecord, user_id=self.user)

        payload = {'survey_id': studyRecord.id}

        response = client.post(reverse('get_post_study_responses'), data=json.dumps(payload), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['errors'], "All places have been taken")


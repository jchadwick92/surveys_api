from django.test import TestCase
from django.contrib.auth.models import User
from ..models import StudyRecord

class StudyRecordTest(TestCase):
    """ Test module for StudyRecord model """

    def setUp(self):
        User.objects.create_user('testuser', "test@test.com", "pass1234")
        user = User.objects.get(email="test@test.com")
        StudyRecord.objects.create(survey_name = 'Test Survey', available_places = 10, user_id = user)

    def test_available_places(self):
        study_record = StudyRecord.objects.get(survey_name='Test Survey')
        self.assertEqual(study_record.get_available_places(), 10)
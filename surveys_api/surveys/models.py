from django.db import models
from django.utils import timezone
from django.conf import settings

class StudyRecord(models.Model):
    survey_name = models.CharField(max_length=100)
    available_places = models.IntegerField()
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {} - {}".format(self.survey_name, self.available_places, self.user_id)

    def get_available_places(self):
        return self.available_places

class StudyResponse(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    survey_id = models.ForeignKey(StudyRecord, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {} - {}".format(self.user_id, self.created_at, self.survey_id)
from django.urls import path
from surveys import views

urlpatterns = [
    path('surveys/', views.study_record_list, name='get_post_study_records'),
    path('survey-responses/', views.study_response_list, name='get_post_study_responses')
]
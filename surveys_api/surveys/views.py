from rest_framework.response import Response
from rest_framework.decorators import api_view
from surveys.models import StudyRecord, StudyResponse
from surveys.serializers import StudyRecordSerializer, StudyResponseSerializer

@api_view(['GET', 'POST'])
def study_record_list(request):
    if request.method == 'GET':
        study_records = StudyRecord.objects.all()
        serializer = StudyRecordSerializer(study_records, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({"errors": "Unauthorized"}, status=401)
        data = {
            'survey_name': request.data.get('survey_name'),
            'available_places': request.data.get('available_places'),
            'user_id': request.user.id
        }
        serializer = StudyRecordSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['POST'])
def study_response_list(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({"errors": "Unauthorized"}, status=401)
        data = {
            'survey_id': request.data.get('survey_id'),
            'user_id': request.user.id
        }
        if studyRecordFull(request.data.get('survey_id')):
            return Response({"errors": "All places have been taken"}, status=403)
        serializer = StudyResponseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

def studyRecordFull(survey_id):
    if not (survey_id):
        return False
    available_places = StudyRecord.objects.get(id=survey_id).get_available_places()
    places_taken = len(StudyResponse.objects.filter(survey_id=survey_id))
    return places_taken >= available_places
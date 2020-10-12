from . import models
from rest_framework import serializers
from django.conf import settings
from .services.login_service import UserSessionService
from .services.survey_service import SurveyService

class UserLoginSerializer(serializers.Serializer):
    """Custom Serializer to validate and create a Login Session."""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, max_length=60, required=True)

    def save(self, **kwargs):
        """Create a new login session object or return an old one."""
        session_input = {
            'email': self.validated_data['email'],
            'password' : self.validated_data['password']
        }
        return UserSessionService(session_input).session_success_data()

class CreateSurveySerializer(serializers.Serializer):
    """Serializer for creating a Survey"""
    title = serializers.CharField(required=True,max_length=256)
    description = serializers.CharField(required=True,max_length=1000)
    questions = serializers.ListField(
        child = serializers.CharField(max_length=1000),
        min_length=1
    )

    def save(self,**kwargs):
        """Create a new survey object and questions object"""
        SurveyService().createSurvey(self.validated_data)

class QuestionSerializer(serializers.Serializer):
    question_id = serializers.IntegerField(required=True)
    attempt = serializers.IntegerField(required=True,min_value=0,max_value=1)

class TakeSurveySerializer(serializers.Serializer):
    survey_id = serializers.IntegerField(required=True)
    answers = QuestionSerializer(many=True,required=True)

    def save(self,**kwargs):
        """Update the survey related questions yes no count"""
        SurveyService().updateResult(self.validated_data)
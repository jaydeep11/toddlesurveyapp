from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models
from common.authorization import Authorization
from common.decorators import session_authorize
from common.custom_renders import JPEGRenderer , PNGRenderer
from .services.survey_service import SurveyService
from .services.image_service import ImageService
from django.conf import settings
from . import serializers
import jwt

import logging
LOGGER = logging.getLogger(__name__)

#Just for testing deployment
class UserWelcome(APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            {
                "message": "Welcome to the Survey API Server, deployed via heroku --V.1.0"
            },
            status=status.HTTP_200_OK)

#Auth API
class UserLoginView(APIView):
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            session_data = serializer.save()
            return Response(session_data, status=status.HTTP_200_OK)
        return Response({},status=status.HTTP_400_BAD_REQUEST)

#API for creating a Survey
class CreateSurveyView(APIView):
    @session_authorize()
    def post(self,request):
        serializer = serializers.CreateSurveySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({}, status=status.HTTP_200_OK)
        return Response({},status=status.HTTP_400_BAD_REQUEST)

#API for taking a survey
class TakeSurveyView(APIView):
    @session_authorize()
    def get(self, request, **kwargs):
        survey_id = request.GET.get('survey_id')
        response = SurveyService.getSurvey(survey_id=survey_id)
        if not response:
            return Response({},status = status.HTTP_400_BAD_REQUEST)
        return Response(response, status=status.HTTP_200_OK)

    @session_authorize()
    def post(self,request):
        serializer = serializers.TakeSurveySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({}, status=status.HTTP_200_OK)
        return Response({},status=status.HTTP_400_BAD_REQUEST)

#API for viewing result of a survey
class SurveyResultView(APIView):
    @session_authorize()
    def get(self, request, **kwargs):
        survey_id = request.GET.get('survey_id')
        response = SurveyService.getSurveyResult(survey_id=survey_id)
        if not response:
            return Response({},status = status.HTTP_400_BAD_REQUEST)
        return Response(response, status=status.HTTP_200_OK)

#API for generating Thumbnail
class CreateThumbnailView(APIView):
    
    renderer_classes = [JPEGRenderer]

    def get(self, request, **kwargs):
        image_url = request.GET.get('image_url')
        # response = HttpResponse(mimetype="image/png")
        image = ImageService.generate_thumbnail(image_url)
        # image.save(response, "PNG")
        image_file = open("temp_image.jpg",'rb')
        if not image:
            return Response({},status = status.HTTP_400_BAD_REQUEST)
        return Response(image_file,content_type = 'image/jpeg')

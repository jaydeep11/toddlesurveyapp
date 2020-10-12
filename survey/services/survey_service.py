"""User Session Service."""
from ..models import Token, Survey, Question
from django.db.models import F

class SurveyService(object):
    """Survey Service to provide functions to create and display surveys"""
    @classmethod
    def createSurvey(cls,data):
        survey_obj = Survey.objects.create(
            title = data.get('title'),
            description = data.get('description')
        )

        for question_text in data.get('questions'):
            Question.objects.create(
                text = question_text,
                survey = survey_obj
            )

    @classmethod
    def getSurvey(cls,survey_id):
        survey = None
        try:
            survey = Survey.objects.get(id=survey_id)
        except Survey.DoesNotExist:
            return None
        response={}
        response['survey_id'] = survey.id
        response['title'] = survey.title
        response['description'] = survey.description

        survey_questions = Question.objects.filter(survey_id=survey_id).values('id','text')

        response['questions'] = survey_questions

        return response

    @classmethod
    def updateResult(cls,data):
        try:
            survey = Survey.objects.get(id=data['survey_id'])
        except Survey.DoesNotExist:
            return None
        
        for answer in data['answers']:
            if answer['attempt'] == 0 :
                Question.objects.filter(id=answer['question_id']).update(no_count=F("no_count") + 1)
            else:
                Question.objects.filter(id=answer['question_id']).update(yes_count=F("yes_count") + 1)

    @classmethod
    def getSurveyResult(cls,survey_id):
        survey = None
        try:
            survey = Survey.objects.get(id=survey_id)
        except Survey.DoesNotExist:
            return None
        response={}
        response['survey_id'] = survey.id
        response['title'] = survey.title
        response['description'] = survey.description

        survey_questions = Question.objects.filter(survey_id=survey_id).values('id','text','yes_count','no_count')

        response['questions'] = survey_questions

        return response

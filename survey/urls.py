from django.urls import path, re_path
from . import views

urlpatterns = [
    #check for deployment Endpoint
    path('', views.UserWelcome.as_view(), name='UserWelcome'),
    
    #Auth Endpoint
    path('auth/',views.UserLoginView.as_view(),name='User Auth'),
    #Create Survey Endpoint
    path('survey/create/',views.CreateSurveyView.as_view(),name='create survey'),
    #Take survey Endpoint
    path('survey/take/',views.TakeSurveyView.as_view(),name='take survey'),
    #Result Endpoint
    path('survey/result/',views.SurveyResultView.as_view(),name='result survey'),
    #Thumbnail Endpoint
    path('thumbnail/',views.CreateThumbnailView.as_view(),name='create thumbnail'),
]

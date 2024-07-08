from django.urls import path
from .views import *

urlpatterns = [
    path('users/', users, name='users'),
    path('polls/', polls, name='polls'),
    path('support_request/', support_request, name='support_request'),
    path('project_settings/', project_settings, name='project_settings'),
    path('study_group/', study_group, name='study_group'),
]

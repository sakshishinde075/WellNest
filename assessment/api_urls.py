from django.urls import path
from . import views

app_name = 'assessment_api'

urlpatterns = [
    path('assessments/', views.assessment_api_list, name='assessment_list'),
    path('results/<int:assessment_id>/', views.assessment_api_result, name='assessment_result'),
]

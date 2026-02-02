from django.urls import path
from . import views

app_name = 'assessment'

urlpatterns = [
    # Assessment views
    path('', views.AssessmentListView.as_view(), name='assessment_list'),
    path('start/', views.start_assessment, name='start_assessment'),
    path('quick/', views.quick_assessment, name='quick_assessment'),
    path('quick/result/<int:assessment_id>/', views.quick_result, name='quick_result'),
    path('<int:pk>/', views.AssessmentDetailView.as_view(), name='assessment_detail'),
    path('take/<int:questionnaire_id>/', views.take_assessment, name='take_assessment'),
    path('result/<int:assessment_id>/', views.assessment_result, name='assessment_result'),
    
    # User dashboard and history
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('history/', views.assessment_history, name='history'),
]

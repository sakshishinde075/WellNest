from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import timedelta
import json

from .models import Questionnaire, AssessmentResponse, QuestionResponse, AssessmentResult, UserProgress
from .forms import AssessmentForm, AssessmentStartForm, QuickAssessmentForm
from .utils import calculate_risk_level, generate_session_id


class AssessmentListView(ListView):
    """List all available assessments."""
    model = Questionnaire
    template_name = 'assessment/assessment_list.html'
    context_object_name = 'questionnaires'
    
    def get_queryset(self):
        return Questionnaire.objects.filter(is_active=True)


class AssessmentDetailView(DetailView):
    """Detail view for a specific assessment."""
    model = Questionnaire
    template_name = 'assessment/assessment_detail.html'
    context_object_name = 'questionnaire'


def start_assessment(request):
    """Start a new assessment."""
    if request.method == 'POST':
        form = AssessmentStartForm(request.POST)
        if form.is_valid():
            questionnaire = form.cleaned_data['questionnaire']
            return redirect('assessment:take_assessment', questionnaire_id=questionnaire.id)
    else:
        form = AssessmentStartForm()
    
    return render(request, 'assessment/start_assessment.html', {'form': form})


def take_assessment(request, questionnaire_id):
    """Take an assessment."""
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id, is_active=True)
    
    if request.method == 'POST':
        form = AssessmentForm(questionnaire, request.POST)
        if form.is_valid():
            # Calculate total score
            total_score = 0
            responses = []
            
            for question in questionnaire.questions.filter(is_required=True):
                field_name = f'question_{question.id}'
                if field_name in form.cleaned_data:
                    value = form.cleaned_data[field_name]
                    
                    if question.question_type in ['single_choice', 'multiple_choice']:
                        if isinstance(value, list):  # Multiple choice
                            for option_id in value:
                                option = question.options.get(id=option_id)
                                total_score += option.value
                                responses.append({
                                    'question': question,
                                    'option': option,
                                    'score': option.value
                                })
                        else:  # Single choice
                            option = question.options.get(id=value)
                            total_score += option.value
                            responses.append({
                                'question': question,
                                'option': option,
                                'score': option.value
                            })
                    
                    elif question.question_type in ['scale', 'scale_extended']:
                        total_score += value
                        responses.append({
                            'question': question,
                            'scale_value': value,
                            'score': value
                        })
            
            # Determine risk level
            risk_level = calculate_risk_level(total_score, questionnaire)
            
            # Create assessment response
            assessment = AssessmentResponse.objects.create(
                user=request.user if request.user.is_authenticated else None,
                questionnaire=questionnaire,
                session_id=generate_session_id(request) if not request.user.is_authenticated else None,
                total_score=total_score,
                risk_level=risk_level,
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            # Save individual responses
            for response_data in responses:
                QuestionResponse.objects.create(
                    assessment=assessment,
                    question=response_data['question'],
                    selected_option=response_data.get('option'),
                    scale_value=response_data.get('scale_value'),
                    score=response_data['score']
                )
            
            # Create user progress entry if user is logged in
            if request.user.is_authenticated:
                UserProgress.objects.create(
                    user=request.user,
                    assessment=assessment,
                    score_change=total_score,
                    risk_level_change=risk_level
                )
            
            return redirect('assessment:assessment_result', assessment_id=assessment.id)
    else:
        form = AssessmentForm(questionnaire)
    
    return render(request, 'assessment/take_assessment.html', {
        'form': form,
        'questionnaire': questionnaire
    })


def assessment_result(request, assessment_id):
    """Display assessment results."""
    assessment = get_object_or_404(AssessmentResponse, id=assessment_id)
    
    # Get the appropriate result template based on risk level
    try:
        result_template = AssessmentResult.objects.filter(
            risk_level=assessment.risk_level,
            min_score__lte=assessment.total_score,
            max_score__gte=assessment.total_score,
            is_active=True
        ).first()
    except AssessmentResult.DoesNotExist:
        result_template = None
    
    return render(request, 'assessment/assessment_result.html', {
        'assessment': assessment,
        'result_template': result_template
    })


def quick_assessment(request):
    """Quick assessment for immediate results."""
    if request.method == 'POST':
        form = QuickAssessmentForm(request.POST)
        if form.is_valid():
            # Calculate score (reverse scale for stress question)
            scores = []
            for field_name, value in form.cleaned_data.items():
                if field_name == 'stress_question':
                    # Reverse scale for stress (higher stress = lower score)
                    scores.append(6 - value)
                else:
                    scores.append(value)
            
            total_score = sum(scores)
            risk_level = calculate_risk_level(total_score, None)  # Quick assessment
            
            # Create a temporary assessment response
            assessment = AssessmentResponse.objects.create(
                user=request.user if request.user.is_authenticated else None,
                questionnaire=None,  # Quick assessment
                session_id=generate_session_id(request) if not request.user.is_authenticated else None,
                total_score=total_score,
                risk_level=risk_level,
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            return redirect('assessment:quick_result', assessment_id=assessment.id)
    else:
        form = QuickAssessmentForm()
    
    return render(request, 'assessment/quick_assessment.html', {'form': form})


def quick_result(request, assessment_id):
    """Display quick assessment results."""
    assessment = get_object_or_404(AssessmentResponse, id=assessment_id)
    
    return render(request, 'assessment/quick_result.html', {
        'assessment': assessment
    })


@login_required
def user_dashboard(request):
    """User dashboard with assessment history."""
    user = request.user
    
    # Get recent assessments
    recent_assessments = AssessmentResponse.objects.filter(user=user).order_by('-completed_at')[:5]
    
    # Get assessment history for charts
    all_assessments = AssessmentResponse.objects.filter(user=user).order_by('completed_at')
    
    # Calculate statistics
    total_assessments = all_assessments.count()
    avg_score = all_assessments.aggregate(avg_score=Avg('total_score'))['avg_score'] or 0
    
    # Risk level distribution
    risk_distribution = all_assessments.values('risk_level').annotate(count=Count('risk_level'))
    
    # Recent trend (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_trend = all_assessments.filter(completed_at__gte=thirty_days_ago)
    
    return render(request, 'assessment/dashboard.html', {
        'recent_assessments': recent_assessments,
        'all_assessments': all_assessments,
        'total_assessments': total_assessments,
        'avg_score': round(avg_score, 2),
        'risk_distribution': risk_distribution,
        'recent_trend': recent_trend
    })


@login_required
def assessment_history(request):
    """Detailed assessment history for logged-in users."""
    assessments = AssessmentResponse.objects.filter(user=request.user).order_by('-completed_at')
    
    return render(request, 'assessment/history.html', {
        'assessments': assessments
    })


# API Views for mobile/frontend integration
def assessment_api_list(request):
    """API endpoint for listing assessments."""
    questionnaires = Questionnaire.objects.filter(is_active=True)
    data = []
    
    for questionnaire in questionnaires:
        data.append({
            'id': questionnaire.id,
            'name': questionnaire.name,
            'description': questionnaire.description,
            'question_count': questionnaire.questions.count()
        })
    
    return JsonResponse({'assessments': data})


def assessment_api_result(request, assessment_id):
    """API endpoint for getting assessment results."""
    try:
        assessment = AssessmentResponse.objects.get(id=assessment_id)
        data = {
            'id': assessment.id,
            'total_score': assessment.total_score,
            'risk_level': assessment.risk_level,
            'completed_at': assessment.completed_at.isoformat(),
            'questionnaire_name': assessment.questionnaire.name if assessment.questionnaire else 'Quick Assessment'
        }
        return JsonResponse(data)
    except AssessmentResponse.DoesNotExist:
        return JsonResponse({'error': 'Assessment not found'}, status=404)

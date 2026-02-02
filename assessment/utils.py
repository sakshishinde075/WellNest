"""
Utility functions for the assessment app.
"""
import uuid
from django.contrib.sessions.models import Session


def calculate_risk_level(total_score, questionnaire):
    """
    Calculate risk level based on total score.
    
    Args:
        total_score (int): The total score from the assessment
        questionnaire (Questionnaire): The questionnaire object (can be None for quick assessments)
    
    Returns:
        str: Risk level ('low', 'moderate', 'high')
    """
    if questionnaire:
        # For full questionnaires, use more sophisticated scoring
        max_possible_score = questionnaire.questions.filter(is_required=True).count() * 5  # Assuming max 5 points per question
        percentage = (total_score / max_possible_score) * 100 if max_possible_score > 0 else 0
        
        if percentage >= 70:
            return 'high'
        elif percentage >= 40:
            return 'moderate'
        else:
            return 'low'
    else:
        # For quick assessments (5 questions, max 5 points each = 25 max)
        if total_score >= 18:
            return 'high'
        elif total_score >= 12:
            return 'moderate'
        else:
            return 'low'


def generate_session_id(request):
    """
    Generate a unique session ID for anonymous users.
    
    Args:
        request: Django request object
    
    Returns:
        str: Unique session ID
    """
    if not request.session.session_key:
        request.session.create()
    
    return f"anon_{request.session.session_key}_{uuid.uuid4().hex[:8]}"


def get_risk_level_display(risk_level):
    """
    Get display text for risk level.
    
    Args:
        risk_level (str): Risk level code
    
    Returns:
        str: Display text for risk level
    """
    risk_levels = {
        'low': 'Low Risk',
        'moderate': 'Moderate Risk',
        'high': 'High Risk'
    }
    return risk_levels.get(risk_level, 'Unknown')


def get_risk_level_color(risk_level):
    """
    Get Tailwind CSS color class for risk level.
    
    Args:
        risk_level (str): Risk level code
    
    Returns:
        str: Tailwind CSS color class
    """
    colors = {
        'low': 'text-green-600 bg-green-100',
        'moderate': 'text-yellow-600 bg-yellow-100',
        'high': 'text-red-600 bg-red-100'
    }
    return colors.get(risk_level, 'text-gray-600 bg-gray-100')


def get_recommendations(risk_level):
    """
    Get recommendations based on risk level.
    
    Args:
        risk_level (str): Risk level code
    
    Returns:
        dict: Recommendations and resources
    """
    recommendations = {
        'low': {
            'title': 'You\'re doing well!',
            'description': 'Your responses suggest you\'re managing your mental health well. Keep up the good work!',
            'actions': [
                'Continue your current self-care practices',
                'Maintain regular sleep and exercise routines',
                'Stay connected with friends and family',
                'Consider periodic check-ins with this assessment'
            ],
            'resources': [
                'Mindfulness and meditation apps',
                'Regular exercise routines',
                'Social connection activities'
            ]
        },
        'moderate': {
            'title': 'Some areas for improvement',
            'description': 'Your responses suggest there are some areas where you could benefit from additional support.',
            'actions': [
                'Consider speaking with a mental health professional',
                'Practice stress management techniques',
                'Maintain a regular sleep schedule',
                'Engage in activities you enjoy',
                'Consider joining a support group'
            ],
            'resources': [
                'Stress management techniques',
                'Sleep hygiene resources',
                'Mental health support groups',
                'Professional counseling services'
            ]
        },
        'high': {
            'title': 'Professional support recommended',
            'description': 'Your responses suggest you may benefit from professional mental health support. Please consider reaching out for help.',
            'actions': [
                'Contact a mental health professional immediately',
                'Reach out to a trusted friend or family member',
                'Consider crisis support resources',
                'Prioritize your safety and well-being',
                'Don\'t hesitate to seek emergency help if needed'
            ],
            'resources': [
                'Crisis helplines (988 Suicide & Crisis Lifeline)',
                'Emergency mental health services',
                'Professional counseling and therapy',
                'Support groups and peer support'
            ]
        }
    }
    
    return recommendations.get(risk_level, recommendations['low'])

from django import forms
from django.forms import formset_factory
from .models import Questionnaire, Question, QuestionResponse, AssessmentResponse


class AssessmentForm(forms.Form):
    """Dynamic form for assessment questions."""
    
    def __init__(self, questionnaire, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.questionnaire = questionnaire
        
        # Add fields for each question
        for question in questionnaire.questions.filter(is_required=True).order_by('order'):
            field_name = f'question_{question.id}'
            
            if question.question_type == 'single_choice':
                choices = [(option.id, option.text) for option in question.options.all()]
                self.fields[field_name] = forms.ChoiceField(
                    choices=choices,
                    widget=forms.RadioSelect(attrs={'class': 'form-radio text-teal-600'}),
                    required=question.is_required,
                    label=question.text
                )
            
            elif question.question_type == 'multiple_choice':
                choices = [(option.id, option.text) for option in question.options.all()]
                self.fields[field_name] = forms.MultipleChoiceField(
                    choices=choices,
                    widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-checkbox text-teal-600'}),
                    required=question.is_required,
                    label=question.text
                )
            
            elif question.question_type == 'scale':
                self.fields[field_name] = forms.IntegerField(
                    widget=forms.NumberInput(attrs={
                        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500',
                        'min': '1',
                        'max': '5'
                    }),
                    required=question.is_required,
                    label=question.text,
                    help_text="Rate from 1 (Not at all) to 5 (Very much)"
                )
            
            elif question.question_type == 'scale_extended':
                self.fields[field_name] = forms.IntegerField(
                    widget=forms.NumberInput(attrs={
                        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500',
                        'min': '1',
                        'max': '10'
                    }),
                    required=question.is_required,
                    label=question.text,
                    help_text="Rate from 1 (Not at all) to 10 (Extremely)"
                )
            
            elif question.question_type == 'text':
                self.fields[field_name] = forms.CharField(
                    widget=forms.Textarea(attrs={
                        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500',
                        'rows': 3
                    }),
                    required=question.is_required,
                    label=question.text
                )


class AssessmentStartForm(forms.Form):
    """Form for starting an assessment."""
    
    questionnaire = forms.ModelChoiceField(
        queryset=Questionnaire.objects.filter(is_active=True),
        empty_label="Select an assessment",
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500'
        })
    )
    
    consent = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 text-teal-600 focus:ring-teal-500 border-gray-300 rounded'
        }),
        label="I understand that this assessment is for informational purposes only and is not a substitute for professional medical advice."
    )


class QuickAssessmentForm(forms.Form):
    """Quick assessment form for immediate results."""
    
    mood_question = forms.ChoiceField(
        choices=[
            (1, 'Very poor'),
            (2, 'Poor'),
            (3, 'Fair'),
            (4, 'Good'),
            (5, 'Excellent')
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-radio text-teal-600'}),
        label="How would you rate your overall mood today?",
        required=True
    )
    
    sleep_question = forms.ChoiceField(
        choices=[
            (1, 'Very poor'),
            (2, 'Poor'),
            (3, 'Fair'),
            (4, 'Good'),
            (5, 'Excellent')
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-radio text-teal-600'}),
        label="How would you rate your sleep quality recently?",
        required=True
    )
    
    stress_question = forms.ChoiceField(
        choices=[
            (1, 'Very high'),
            (2, 'High'),
            (3, 'Moderate'),
            (4, 'Low'),
            (5, 'Very low')
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-radio text-teal-600'}),
        label="How would you rate your current stress level?",
        required=True
    )
    
    social_question = forms.ChoiceField(
        choices=[
            (1, 'Very isolated'),
            (2, 'Somewhat isolated'),
            (3, 'Neutral'),
            (4, 'Somewhat connected'),
            (5, 'Very connected')
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-radio text-teal-600'}),
        label="How connected do you feel to others?",
        required=True
    )
    
    energy_question = forms.ChoiceField(
        choices=[
            (1, 'Very low'),
            (2, 'Low'),
            (3, 'Moderate'),
            (4, 'High'),
            (5, 'Very high')
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-radio text-teal-600'}),
        label="How would you rate your energy level?",
        required=True
    )

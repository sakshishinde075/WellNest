from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Questionnaire(models.Model):
    """Model for storing questionnaire templates."""
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']


class Question(models.Model):
    """Model for individual questions in a questionnaire."""
    
    QUESTION_TYPES = [
        ('single_choice', 'Single Choice'),
        ('multiple_choice', 'Multiple Choice'),
        ('scale', 'Scale (1-5)'),
        ('scale_extended', 'Scale (1-10)'),
        ('text', 'Text Response'),
    ]
    
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    order = models.PositiveIntegerField(default=0)
    is_required = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.questionnaire.name} - {self.text[:50]}..."
    
    class Meta:
        ordering = ['order', 'id']


class QuestionOption(models.Model):
    """Model for question options (for multiple choice questions)."""
    
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=200)
    value = models.IntegerField(help_text="Numeric value for scoring")
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.question.text[:30]}... - {self.text}"
    
    class Meta:
        ordering = ['order', 'id']


class AssessmentResponse(models.Model):
    """Model for storing user responses to assessments."""
    
    RISK_LEVELS = [
        ('low', 'Low Risk'),
        ('moderate', 'Moderate Risk'),
        ('high', 'High Risk'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assessments', null=True, blank=True)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=100, null=True, blank=True)  # For anonymous users
    total_score = models.IntegerField(default=0)
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS)
    completed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    def __str__(self):
        user_info = self.user.username if self.user else f"Anonymous ({self.session_id})"
        return f"{user_info} - {self.questionnaire.name} - {self.risk_level}"
    
    class Meta:
        ordering = ['-completed_at']


class QuestionResponse(models.Model):
    """Model for storing individual question responses."""
    
    assessment = models.ForeignKey(AssessmentResponse, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(QuestionOption, on_delete=models.CASCADE, null=True, blank=True)
    scale_value = models.IntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="For scale questions (1-10)"
    )
    text_response = models.TextField(null=True, blank=True)
    score = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.assessment} - {self.question.text[:30]}..."
    
    class Meta:
        unique_together = ['assessment', 'question']


class AssessmentResult(models.Model):
    """Model for storing assessment results and recommendations."""
    
    risk_level = models.CharField(max_length=20, choices=AssessmentResponse.RISK_LEVELS)
    title = models.CharField(max_length=200)
    description = models.TextField()
    recommendations = models.TextField()
    resources = models.TextField(help_text="Additional resources and helplines")
    min_score = models.IntegerField()
    max_score = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.risk_level.title()} Risk - {self.title}"
    
    class Meta:
        ordering = ['min_score']


class UserProgress(models.Model):
    """Model for tracking user progress over time."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    assessment = models.ForeignKey(AssessmentResponse, on_delete=models.CASCADE)
    score_change = models.IntegerField(default=0)
    risk_level_change = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.assessment.questionnaire.name} - {self.created_at.date()}"
    
    class Meta:
        ordering = ['-created_at']

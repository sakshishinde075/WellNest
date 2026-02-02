from django.contrib import admin
from .models import (
    Questionnaire, Question, QuestionOption, AssessmentResponse, 
    QuestionResponse, AssessmentResult, UserProgress
)


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'questionnaire', 'question_type', 'order', 'is_required']
    list_filter = ['question_type', 'is_required', 'questionnaire']
    search_fields = ['text']
    ordering = ['questionnaire', 'order']
    inlines = [QuestionOptionInline]


@admin.register(AssessmentResponse)
class AssessmentResponseAdmin(admin.ModelAdmin):
    list_display = ['user', 'questionnaire', 'risk_level', 'total_score', 'completed_at']
    list_filter = ['risk_level', 'completed_at', 'questionnaire']
    search_fields = ['user__username', 'user__email', 'session_id']
    ordering = ['-completed_at']
    readonly_fields = ['completed_at', 'ip_address']


@admin.register(QuestionResponse)
class QuestionResponseAdmin(admin.ModelAdmin):
    list_display = ['assessment', 'question', 'score', 'scale_value']
    list_filter = ['assessment__risk_level', 'question__question_type']
    search_fields = ['assessment__user__username', 'question__text']


@admin.register(AssessmentResult)
class AssessmentResultAdmin(admin.ModelAdmin):
    list_display = ['risk_level', 'title', 'min_score', 'max_score', 'is_active']
    list_filter = ['risk_level', 'is_active']
    search_fields = ['title', 'description']


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'assessment', 'score_change', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username']
    ordering = ['-created_at']

from django.contrib import admin
from .models import Therapist, Availability, Appointment, Article, UserStory, Video


@admin.register(Therapist)
class TherapistAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'years_experience', 'rating', 'is_available']
    list_filter = ['specialization', 'is_available', 'created_at']
    search_fields = ['name', 'bio', 'contact_email']
    ordering = ['-rating', 'name']


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ['therapist', 'day_of_week', 'start_time', 'end_time', 'is_active']
    list_filter = ['day_of_week', 'is_active', 'therapist']
    ordering = ['therapist', 'day_of_week', 'start_time']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'therapist', 'appointment_date', 'status', 'created_at']
    list_filter = ['status', 'appointment_date', 'therapist']
    search_fields = ['user__username', 'therapist__name']
    ordering = ['-appointment_date']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_published', 'publish_date', 'views']
    list_filter = ['category', 'is_published', 'publish_date']
    search_fields = ['title', 'author', 'content']
    ordering = ['-publish_date']


@admin.register(UserStory)
class UserStoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'approval_status', 'is_anonymous', 'created_at']
    list_filter = ['approval_status', 'is_anonymous', 'created_at']
    search_fields = ['title', 'story_text', 'user__username']
    ordering = ['-created_at']


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'is_active', 'created_at']
    list_filter = ['category', 'is_featured', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['-is_featured', '-created_at']

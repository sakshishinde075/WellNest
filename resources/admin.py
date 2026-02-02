from django.contrib import admin
from .models import (
    ResourceCategory, Resource, GuidanceContent, 
    CrisisResource, FAQ, UserBookmark
)


@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'resource_type', 'category', 'is_free', 'is_verified', 'is_active']
    list_filter = ['resource_type', 'category', 'is_free', 'is_verified', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'url']
    ordering = ['-created_at']


@admin.register(GuidanceContent)
class GuidanceContentAdmin(admin.ModelAdmin):
    list_display = ['risk_level', 'title', 'is_active', 'created_at']
    list_filter = ['risk_level', 'is_active', 'created_at']
    search_fields = ['title', 'content']


@admin.register(CrisisResource)
class CrisisResourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'is_24_7', 'priority', 'is_active']
    list_filter = ['is_24_7', 'is_active', 'priority']
    search_fields = ['name', 'description', 'phone']
    ordering = ['-priority']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order', 'is_active']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['question', 'answer']
    ordering = ['order', 'question']


@admin.register(UserBookmark)
class UserBookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'resource', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'resource__title']
    ordering = ['-created_at']

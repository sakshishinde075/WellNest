from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ResourceCategory(models.Model):
    """Model for categorizing resources."""
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#3B82F6', help_text="Hex color code")
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class name")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Resource Categories'
        ordering = ['name']


class Resource(models.Model):
    """Model for storing mental health resources."""
    
    RESOURCE_TYPES = [
        ('article', 'Article'),
        ('video', 'Video'),
        ('podcast', 'Podcast'),
        ('app', 'Mobile App'),
        ('book', 'Book'),
        ('website', 'Website'),
        ('helpline', 'Helpline'),
        ('support_group', 'Support Group'),
        ('therapy', 'Therapy Service'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE, related_name='resources')
    url = models.URLField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    is_free = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']


class GuidanceContent(models.Model):
    """Model for storing guidance content based on assessment results."""
    
    RISK_LEVELS = [
        ('low', 'Low Risk'),
        ('moderate', 'Moderate Risk'),
        ('high', 'High Risk'),
    ]
    
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS)
    title = models.CharField(max_length=200)
    content = models.TextField()
    self_care_tips = models.TextField(blank=True)
    when_to_seek_help = models.TextField(blank=True)
    emergency_resources = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_risk_level_display()} - {self.title}"
    
    class Meta:
        ordering = ['risk_level', 'title']


class CrisisResource(models.Model):
    """Model for crisis and emergency resources."""
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    phone = models.CharField(max_length=20)
    text_line = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    is_24_7 = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    priority = models.PositiveIntegerField(default=0, help_text="Higher numbers = higher priority")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-priority', 'name']


class FAQ(models.Model):
    """Model for frequently asked questions."""
    
    question = models.CharField(max_length=500)
    answer = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.question
    
    class Meta:
        ordering = ['order', 'question']


class UserBookmark(models.Model):
    """Model for user bookmarks."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.resource.title}"
    
    class Meta:
        unique_together = ['user', 'resource']
        ordering = ['-created_at']

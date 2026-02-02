from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Therapist(models.Model):
    """Model for therapist profiles."""
    
    SPECIALIZATIONS = [
        ('depression', 'Depression'),
        ('anxiety', 'Anxiety'),
        ('stress', 'Stress Management'),
        ('trauma', 'Trauma'),
        ('relationships', 'Relationships'),
        ('addiction', 'Addiction'),
        ('grief', 'Grief Counseling'),
        ('eating_disorders', 'Eating Disorders'),
        ('bipolar', 'Bipolar Disorder'),
        ('ocd', 'OCD'),
        ('ptsd', 'PTSD'),
        ('general', 'General Counseling'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='therapist_profile')
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATIONS)
    years_experience = models.PositiveIntegerField()
    bio = models.TextField()
    profile_photo = models.ImageField(upload_to='therapists/', blank=True, null=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    meeting_link = models.URLField(blank=True, help_text="Google Meet or Zoom link")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_specialization_display()}"
    
    class Meta:
        ordering = ['-rating', 'name']


class Availability(models.Model):
    """Model for therapist availability slots."""
    
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE, related_name='availability')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.therapist.name} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"
    
    class Meta:
        ordering = ['day_of_week', 'start_time']


class Appointment(models.Model):
    """Model for therapy appointments."""
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    meeting_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.therapist.name} - {self.appointment_date}"
    
    class Meta:
        ordering = ['-appointment_date']


class Article(models.Model):
    """Model for mental health articles."""
    
    CATEGORIES = [
        ('depression', 'Depression'),
        ('anxiety', 'Anxiety'),
        ('stress', 'Stress Management'),
        ('self_care', 'Self-Care'),
        ('relationships', 'Relationships'),
        ('mindfulness', 'Mindfulness'),
        ('therapy', 'Therapy'),
        ('general', 'General'),
    ]
    
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    content = models.TextField()
    excerpt = models.TextField(max_length=500)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORIES)
    publish_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-publish_date']


class UserStory(models.Model):
    """Model for user motivational stories."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    title = models.CharField(max_length=200)
    story_text = models.TextField()
    approval_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    class Meta:
        ordering = ['-created_at']


class Video(models.Model):
    """Model for YouTube videos."""
    
    CATEGORIES = [
        ('meditation', 'Meditation'),
        ('relaxation', 'Relaxation'),
        ('education', 'Educational'),
        ('motivation', 'Motivation'),
        ('therapy', 'Therapy'),
        ('general', 'General'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    youtube_url = models.URLField()
    youtube_id = models.CharField(max_length=20, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORIES)
    thumbnail_url = models.URLField(blank=True)
    duration_minutes = models.PositiveIntegerField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-is_featured', '-created_at']

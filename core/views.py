from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Home page view with featured content and navigation."""
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any context data needed for the home page
        context['featured_articles'] = self.get_featured_articles()
        return context
    
    def get_featured_articles(self):
        """Get featured articles for the home page."""
        # This would typically come from a database
        return [
            {
                'title': 'Understanding Mental Health: A Comprehensive Guide',
                'category': 'MENTAL HEALTH BASICS',
                'author': 'Dr. Sarah Johnson, PhD',
                'excerpt': 'Learn about the fundamentals of mental health and how to recognize early signs.',
                'image': 'images/mental-health-guide.jpg'
            },
            {
                'title': '5 Simple Self-Care Practices for Daily Wellness',
                'category': 'SELF-CARE',
                'author': 'Dr. Michael Chen, LCSW',
                'excerpt': 'Discover easy-to-implement self-care strategies that can improve your mental well-being.',
                'image': 'images/self-care-practices.jpg'
            },
            {
                'title': 'Building Resilience: How to Bounce Back from Challenges',
                'category': 'RESILIENCE',
                'author': 'Dr. Emily Rodriguez, PhD',
                'excerpt': 'Learn practical techniques to build emotional resilience and cope with life\'s difficulties.',
                'image': 'images/resilience-building.jpg'
            }
        ]


class AboutView(TemplateView):
    """About page view."""
    template_name = 'core/about.html'


class HowItWorksView(TemplateView):
    """How it works page view."""
    template_name = 'core/how_it_works.html'


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    """User dashboard view for logged-in users."""
    template_name = 'core/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get user's recent assessments
        from assessment.models import AssessmentResponse
        recent_assessments = AssessmentResponse.objects.filter(user=user).order_by('-completed_at')[:5]
        context['recent_assessments'] = recent_assessments
        
        # Get user's assessment history for charts
        all_assessments = AssessmentResponse.objects.filter(user=user).order_by('completed_at')
        context['assessment_history'] = all_assessments
        
        # Get video resources (from Resource model)
        from resources.models import Resource
        import re
        
        video_resources = Resource.objects.filter(
            resource_type='video',
            is_active=True
        ).order_by('-created_at')[:2]
        
        # Extract YouTube video IDs if URLs are YouTube links
        videos_data = []
        for video in video_resources:
            video_data = {
                'title': video.title,
                'description': video.description,
                'url': video.url,
                'youtube_id': None
            }
            
            # Extract YouTube video ID from URL
            if video.url:
                youtube_regex = r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})'
                match = re.search(youtube_regex, video.url)
                if match:
                    video_data['youtube_id'] = match.group(1)
            
            videos_data.append(video_data)
        
        context['videos'] = videos_data if videos_data else None
        
        # Get article resources
        context['articles'] = Resource.objects.filter(
            resource_type='article',
            is_active=True
        ).order_by('-created_at')[:2]
        
        # Get therapists (with dummy data fallback)
        try:
            from therapists.models import Therapist, UserStory, Appointment
            db_therapists = Therapist.objects.filter(
                is_available=True
            ).order_by('-rating')[:6]
            
            # Convert to dict format with image support
            therapists_list = []
            for therapist in db_therapists:
                therapists_list.append({
                    'name': therapist.name,
                    'experience': f"{therapist.get_specialization_display} ({getattr(therapist, 'years_experience', 'N/A')} years)" if hasattr(therapist, 'years_experience') else therapist.get_specialization_display,
                    'image': None,
                    'profile_photo': therapist.profile_photo,
                    'rating': therapist.rating,
                    'specialization': therapist.get_specialization_display()
                })
            
            # Add dummy therapists if we don't have enough
            if len(therapists_list) < 6:
                dummy_therapists = [
                    {"name": "Dr. Ananya Sharma", "experience": "Clinical Psychologist (8 years)", "image": "https://randomuser.me/api/portraits/women/65.jpg", "rating": 4.9},
                    {"name": "Dr. Rahul Mehta", "experience": "Cognitive Behavioral Therapist (5 years)", "image": "https://randomuser.me/api/portraits/men/43.jpg", "rating": 4.7},
                    {"name": "Dr. Priya Menon", "experience": "Child Psychologist (6 years)", "image": "https://randomuser.me/api/portraits/women/48.jpg", "rating": 4.8},
                    {"name": "Dr. Sameer Verma", "experience": "Stress Management Expert (10 years)", "image": "https://randomuser.me/api/portraits/men/60.jpg", "rating": 4.9},
                    {"name": "Dr. Kavita Rao", "experience": "Mindfulness Coach (7 years)", "image": "https://randomuser.me/api/portraits/women/52.jpg", "rating": 4.6},
                    {"name": "Dr. Arjun Nair", "experience": "Relationship Counselor (9 years)", "image": "https://randomuser.me/api/portraits/men/49.jpg", "rating": 4.8},
                ]
                therapists_list.extend(dummy_therapists[:6 - len(therapists_list)])
            
            context['therapists'] = therapists_list[:6]
            
            # Get approved success stories
            context['success_stories'] = UserStory.objects.filter(
                approval_status='approved'
            ).order_by('-created_at')[:2]
            
            # Get user's upcoming appointments
            from django.utils import timezone
            context['upcoming_appointments'] = Appointment.objects.filter(
                user=user,
                status__in=['scheduled', 'confirmed'],
                appointment_date__gte=timezone.now()
            ).order_by('appointment_date')[:5]
        except ImportError:
            context['therapists'] = []
            context['success_stories'] = []
            context['upcoming_appointments'] = []
        
        # Add MEDIA_URL to context
        from django.conf import settings
        context['MEDIA_URL'] = settings.MEDIA_URL
        
        return context

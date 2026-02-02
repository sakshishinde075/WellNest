from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Resource, ResourceCategory, GuidanceContent, CrisisResource, FAQ, UserBookmark


class ResourceListView(ListView):
    """List all resources with filtering and search."""
    model = Resource
    template_name = 'resources/resource_list.html'
    context_object_name = 'resources'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Resource.objects.filter(is_active=True)
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__name__icontains=category)
        
        # Filter by resource type
        resource_type = self.request.GET.get('type')
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(category__name__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ResourceCategory.objects.filter(is_active=True)
        context['resource_types'] = Resource.RESOURCE_TYPES
        return context


class ResourceDetailView(DetailView):
    """Detail view for a specific resource."""
    model = Resource
    template_name = 'resources/resource_detail.html'
    context_object_name = 'resource'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resource = self.get_object()
        
        # Check if user has bookmarked this resource
        if self.request.user.is_authenticated:
            context['is_bookmarked'] = UserBookmark.objects.filter(
                user=self.request.user,
                resource=resource
            ).exists()
        
        # Get related resources
        context['related_resources'] = Resource.objects.filter(
            category=resource.category,
            is_active=True
        ).exclude(id=resource.id)[:4]
        
        return context


def guidance_view(request, risk_level):
    """Display guidance content based on risk level."""
    guidance = get_object_or_404(GuidanceContent, risk_level=risk_level, is_active=True)
    
    # Get relevant resources for this risk level
    resources = Resource.objects.filter(
        is_active=True,
        is_verified=True
    ).order_by('-created_at')[:6]
    
    return render(request, 'resources/guidance.html', {
        'guidance': guidance,
        'resources': resources,
        'risk_level': risk_level
    })


def crisis_resources_view(request):
    """Display crisis and emergency resources."""
    crisis_resources = CrisisResource.objects.filter(is_active=True).order_by('-priority')
    
    return render(request, 'resources/crisis.html', {
        'crisis_resources': crisis_resources
    })


def faq_view(request):
    """Display frequently asked questions."""
    faqs = FAQ.objects.filter(is_active=True).order_by('order', 'question')
    
    # Group FAQs by category
    categories = {}
    for faq in faqs:
        category = faq.category or 'General'
        if category not in categories:
            categories[category] = []
        categories[category].append(faq)
    
    return render(request, 'resources/faq.html', {
        'categories': categories
    })


@login_required
def bookmark_resource(request, resource_id):
    """Bookmark or unbookmark a resource."""
    if request.method == 'POST':
        resource = get_object_or_404(Resource, id=resource_id)
        bookmark, created = UserBookmark.objects.get_or_create(
            user=request.user,
            resource=resource
        )
        
        if created:
            messages.success(request, f'"{resource.title}" has been bookmarked.')
            return JsonResponse({'status': 'bookmarked'})
        else:
            bookmark.delete()
            messages.info(request, f'"{resource.title}" has been removed from bookmarks.')
            return JsonResponse({'status': 'unbookmarked'})
    
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def user_bookmarks(request):
    """Display user's bookmarked resources."""
    bookmarks = UserBookmark.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'resources/bookmarks.html', {
        'bookmarks': bookmarks
    })


def resource_search(request):
    """AJAX search for resources."""
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'resources': []})
    
    resources = Resource.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query),
        is_active=True
    )[:10]
    
    data = []
    for resource in resources:
        data.append({
            'id': resource.id,
            'title': resource.title,
            'description': resource.description[:100] + '...' if len(resource.description) > 100 else resource.description,
            'url': resource.get_absolute_url(),
            'type': resource.get_resource_type_display(),
            'category': resource.category.name
        })
    
    return JsonResponse({'resources': data})


def reference_links_view(request):
    """Display reference links and research."""
    return render(request, 'resources/reference_links.html')

from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [
    # Resource views
    path('', views.ResourceListView.as_view(), name='resource_list'),
    path('<int:pk>/', views.ResourceDetailView.as_view(), name='resource_detail'),
    path('search/', views.resource_search, name='resource_search'),
    
    # Guidance and crisis resources
    path('guidance/<str:risk_level>/', views.guidance_view, name='guidance'),
    path('crisis/', views.crisis_resources_view, name='crisis'),
    path('faq/', views.faq_view, name='faq'),
    path('reference-links/', views.reference_links_view, name='reference_links'),
    
    # User bookmarks
    path('bookmark/<int:resource_id>/', views.bookmark_resource, name='bookmark_resource'),
    path('bookmarks/', views.user_bookmarks, name='bookmarks'),
]

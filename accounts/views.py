from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.decorators import method_decorator
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from .models import User


class SignUpView(CreateView):
    """User registration view."""
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('core:dashboard')
    
    def form_valid(self, form):
        """Log the user in after successful registration."""
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Account created successfully! Welcome to MindCheck.')
        return response


class CustomLoginView(LoginView):
    """Custom login view with styling."""
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        """Redirect to dashboard after successful login."""
        return reverse_lazy('core:dashboard')


class CustomLogoutView(LogoutView):
    """Custom logout view."""
    next_page = reverse_lazy('core:home')
    
    def dispatch(self, request, *args, **kwargs):
        """Add success message before logout."""
        messages.success(request, 'You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    """User profile update view."""
    model = User
    form_class = UserProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        """Return the current user."""
        return self.request.user
    
    def form_valid(self, form):
        """Add success message after profile update."""
        messages.success(self.request, 'Your profile has been updated successfully.')
        return super().form_valid(form)


@login_required
def profile_view(request):
    """Profile view for displaying user information."""
    return render(request, 'accounts/profile.html', {'user': request.user})

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form with additional fields."""
    
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500',
        'placeholder': 'Enter your email address'
    }))
    
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500',
        'placeholder': 'First name'
    }))
    
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500',
        'placeholder': 'Last name'
    }))
    
    privacy_consent = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={
        'class': 'h-4 w-4 text-teal-600 focus:ring-teal-500 border-gray-300 rounded'
    }))
    
    data_processing_consent = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={
        'class': 'h-4 w-4 text-teal-600 focus:ring-teal-500 border-gray-300 rounded'
    }))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Style the form fields
        for field_name, field in self.fields.items():
            if field_name not in ['privacy_consent', 'data_processing_consent']:
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500'
                })
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.privacy_consent = self.cleaned_data['privacy_consent']
        user.data_processing_consent = self.cleaned_data['data_processing_consent']
        
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """Custom login form with styling."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500',
            'placeholder': 'Username or email'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500',
            'placeholder': 'Password'
        })


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile information."""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'emergency_contact', 'emergency_phone']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500'
            }),
            'emergency_contact': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500'
            }),
            'emergency_phone': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500'
            }),
        }

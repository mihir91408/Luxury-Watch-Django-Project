from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CreativeSignupForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, label="Full Name")
    email = forms.EmailField(max_length=254, label="Email Address")

    class Meta:
        model = User
        fields = ('full_name', 'email')

    # --- ADD THIS NEW FUNCTION ---
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if a user with this email already exists
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered. Please login instead.")
        return email
    # -----------------------------

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['full_name']
        user.username = self.cleaned_data['email']  # Sync username with email
        
        if commit:
            user.save()
        return user

# (Keep CreativeLoginForm unchanged)
class CreativeLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'you@domain.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
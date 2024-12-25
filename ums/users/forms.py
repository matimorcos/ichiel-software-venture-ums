from django import forms
from .models import User, Provider, Team

class LoginForm(forms.ModelForm):
    """Custom authentication form for username login."""
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
class RegisterForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['address', 'birthdate', 'city', 'country', 'email', 'first_name', 'last_name', 'password', 'phone_number', 'postal_code', 'username']
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['address', 'birthdate', 'city', 'country', 'email', 'first_name', 'last_name', 'phone_number', 'postal_code']   

class ProviderForm(forms.ModelForm):
    class Meta:
        model=Provider
        fields=['is_approved']
        
class TeamForm(forms.ModelForm):
    team_id = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Team
        fields = ['name', 'player_count', 'sport',]
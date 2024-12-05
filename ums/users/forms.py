from django import forms
from .models import User

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
        fields=['email', 'username', 'password', 'first_name', 'last_name', 'birthdate', 'country', 'city', 'postal_code', 'address', 'phone_number']
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['email', 'username', 'country', 'city', 'postal_code', 'address', 'phone_number']   

    
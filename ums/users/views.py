from rest_framework import generics, status
from .models import User, UserManager, Profile
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.views import APIView, View
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q

"""HTTP RESPONSES ARE REPLACED WITH JSON RESPONSES"""

class UsernameLoginForm(AuthenticationForm):
    """Custom authentication form for username login."""
    username = forms.CharField(
        label="Username",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
    )

class RegisterView(generics.CreateAPIView):
    """Register a new user view."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

def register_view(request):
    """ Register a new user. """
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        birthdate = request.POST['birthdate']
        country = request.POST['country']
        city = request.POST['city']
        postal_code = request.POST['postal_code']
        address = request.POST['address']
        phone_number = request.POST['phone_number']
        
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
            user.save()
            messages.success(request, "Usuario registrado exitosamente. ¡Inicia sesión!")
            return redirect('login') 
        except Exception as e:
            messages.error(request, f"Error al registrar usuario: {str(e)}")
            return render(request, 'register.html')

    return render(request, 'register.html')
        
class LoginView(APIView):
    """ Login a user view."""
    def post(self, request):
        """ Login a user."""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.id,
                "email": user.email,
                "username": user.username,
                "role": user.role,
            },
            status=status.HTTP_200_OK,
        )

class CustomLoginView(View):
    """ Custom login view. """
    template_name = 'index.html'  

    def get(self, request):
        """ Render the login page. """
        if request.user.is_authenticated:
            return redirect('/dashboard/')
        return render(request, self.template_name)

    def post(self, request):
        """ Handle the login form submission. """
        username = request.POST.get('username')
        password = request.POST.get('password')

        
        user = authenticate(request, username=username, password=password)
        """ If the user is authenticated, log him in and redirect to the dashboard ('/dashboard/'). """
        if user is not None:
            login(request, user)  
            return redirect('/dashboard/')  
        else:
            
            return render(request, self.template_name, {'error': 'Credenciales inválidas'})

@login_required
def dashboard_view(request):
    """ Dashboard view. """
    return render(request, 'login.html', {'user': request.user})

@login_required
def home_view(request):
    """ Home view. """
    return render(request, 'home.html', {'user': request.user})

@login_required
def profile(request):
    """ Profile view. TRY DRY CODE"""
    return render(request, 'profile.html', {'profile': request.user.profile})

@login_required
def profile(request):
    """ Profile view. Check if the user has a profile, if not, create one. TRY DRY CODE"""
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

@login_required
def update_profile(request):
    """ Update profile view. """
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        email = request.POST.get('email', user.email)
        username = request.POST.get('username', user.username)
        first_name = request.POST.get('first_name', user.first_name)
        last_name = request.POST.get('last_name', user.last_name)
        birthdate = request.POST.get('birthdate', profile.birthdate)
        country = request.POST.get('country', profile.country)
        city = request.POST.get('city', profile.city)
        address = request.POST.get('address', profile.address)
        phone_number = request.POST.get('phone_number', profile.phone_number)

        """Update user (account data) and profile"""
        user.email = email
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        """Update profile data and save"""
        profile.birthdate = birthdate
        profile.country = country
        profile.city = city
        profile.address = address
        profile.phone_number = phone_number
        profile.save()

        messages.success(request, 'Perfil actualizado exitosamente.')
        return redirect('profile')

    return render(request, 'update_profile.html', {'user': user})

def search_users(request):
    """ Search for users by username, first name, or last name. """
    query = request.GET.get('query', '').strip()
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).values('username', 'first_name', 'last_name')
        return JsonResponse(list(users), safe=False)
    return JsonResponse([], safe=False)

def logout_view(request):
    """ Logout the user. """
    logout(request)  
    return redirect('/')  
from rest_framework import generics, status
from .models import User, UserManager
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.views import APIView, View
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

class UsernameLoginForm(AuthenticationForm):
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
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

def register_view(request):
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
    def post(self, request):
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
    template_name = 'index.html'  

    def get(self, request):
        
        if request.user.is_authenticated:
            return redirect('/dashboard/')
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  
            return redirect('/dashboard/')  
        else:
            
            return render(request, self.template_name, {'error': 'Credenciales inválidas'})

@login_required
def dashboard_view(request):
    
    return render(request, 'login.html', {'user': request.user})
    
def logout_view(request):
    logout(request)  
    return redirect('/')  
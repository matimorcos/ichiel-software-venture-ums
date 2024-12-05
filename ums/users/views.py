from .forms import LoginForm, RegisterForm, ProfileForm
from .models import User, UserManager, Profile
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import generics, status
from rest_framework.views import APIView, View
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q

class LoginTemplateView(View):
    """ Custom login view. """
    template_name = 'index.html'  

    def get(self, request):
        """ Render the login page. """
        if request.user.is_authenticated:
            return redirect('/login/')
        form=LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """ Handle the login form submission. """
        username = request.POST.get('username')
        password = request.POST.get('password')

        
        user = authenticate(request, username=username, password=password)
        """ If the user is authenticated, log him in and redirect to the dashboard ('/dashboard/'). """
        if user is not None:
            login(request, user)  
            return redirect('/home/')  
        else:
            
            return render(request, self.template_name, {'error': 'Credenciales inválidas'})

class LoginAPIView(APIView):    
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

class RegisterSerializerTemplateView(View):
    template_name = 'register.html'
    
    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
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
    
class RegisterTemplateView(View):
    template_name = 'register.html'

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, 'Registro exitoso, ahora puedes iniciar sesión.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Error al registrar: {e}')
        return render(request, self.template_name, {'form': form})

@method_decorator(login_required, name='dispatch')
class HomeTemplateView(View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name, {'user': request.user})
    
    def post(self, request):
        return render(request, self.template_name, {'user': request.user})

class SearchUsersView(View):
    def get(self, request):
        query = request.GET.get('query', '').strip()
        if query:
            users = User.objects.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            ).values('username', 'first_name', 'last_name')
            return JsonResponse(list(users), safe=False)
        return JsonResponse([], safe=False)

@method_decorator(login_required, name='dispatch')
class ProfileTemplateView(View):
    template_name = 'update_profile.html'

    def get(self, request):
        form = ProfileForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user = request.user
        profile = user.profile
        # Actualización de datos DE USUARIO
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()

        # Actualización de datos DE PERFIL
        profile.birthdate = request.POST.get('birthdate', profile.birthdate)
        profile.country = request.POST.get('country', profile.country)
        profile.city = request.POST.get('city', profile.city)
        profile.address = request.POST.get('address', profile.address)
        profile.phone_number = request.POST.get('phone_number', profile.phone_number)
        profile.save()

        messages.success(request, 'Perfil actualizado exitosamente.')
        return redirect('update_profile')

class UpdateProfileTemplateView(View):
    template_name = 'update_profile.html'

    def get(self, request):
        form = ProfileForm()
        return render(request, self.template_name, {'form': form})
    
class LogoutTemplateView(View):
    template_name = 'index.html'
    
    def post(self, request):
        logout(request)
        return redirect('/') 
from .forms import LoginForm, RegisterForm, ProfileForm, ProviderForm, TeamForm
from .models import User, UserManager, Profile, Provider, Team
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import generics, status
from rest_framework.views import APIView, View
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.messages import get_messages
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
            messages.success(request, "Inicio de sesión exitoso.")
            return redirect('/home/')  
        else:
            messages.error(request, "Credenciales incorrectas. Inténtalo nuevamente.")
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
                storage = get_messages(request)
                list(storage)
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Error al registrar: {e}')
                storage = get_messages(request)
                list(storage)
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
    template_name = 'profile.html'

    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            profile = user.profile
            profile.birthdate = request.POST.get('birthdate', profile.birthdate)
            profile.country = request.POST.get('country', profile.country)
            profile.city = request.POST.get('city', profile.city)
            profile.address = request.POST.get('address', profile.address)
            profile.phone_number = request.POST.get('phone_number', profile.phone_number)
            profile.save()

            messages.success(request, 'Perfil editado exitosamente.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
                    
        return render(request, self.template_name, {'form': form})

class TeamTemplateView(View):
    template_name = 'teams.html'

    def get(self, request):
        teams = Team.objects.filter(user=request.user)
        form = TeamForm()
        return render(request, self.template_name, {'teams': teams, 'form': form})

    def post(self, request):
        form = TeamForm(request.POST)
        if 'create_team' in request.POST:
            if form.is_valid():
                team = form.save(commit=False)
                team.user = request.user
                team.save()
                return redirect('teams')
        elif 'edit_team' in request.POST:
            team = get_object_or_404(Team, id=request.POST.get('team_id'), user=request.user)
            form = TeamForm(request.POST, instance=team)
            if form.is_valid():
                form.save()
                return redirect('teams')
        elif 'delete_team' in request.POST:
            team = get_object_or_404(Team, id=request.POST.get('team_id'), user=request.user)
            team.delete()
            return redirect('teams')
        
        teams = Team.objects.filter(user=request.user)
        return render(request, self.template_name, {'teams': teams, 'form': form})

class NotificationsTemplateView(View):
    template_name = 'notifications.html'
    
    def get(self, request):
        return render(request, self.template_name, {'user': request.user})
    
    def post(self, request):
        return render(request, self.template_name, {'user': request.user}) 
    
class MyBookingsTemplateView(View):
    template_name = 'mybookings.html'
    
    def get(self, request):
        return render(request, self.template_name, {'user': request.user})

    def post(self, request):
        return render(request, self.template_name, {'user': request.user})

@method_decorator(login_required, name='dispatch')
class PartnershipTemplateView(View):
    template_name = 'partnership.html'

    def get(self, request):
        try:
            provider = Provider.objects.get(user=request.user)
            is_provider = True
        except Provider.DoesNotExist:
            provider = None
            is_provider = False
        return render(request, self.template_name, {'is_provider': is_provider, 'provider': provider})

    def post(self, request):
        if 'cancel_partnership' in request.POST:
            try:
                provider = Provider.objects.get(user=request.user)
                provider.delete()
                request.user.is_staff = False
                request.user.save()
                messages.success(request, 'Has cancelado tu asociación.')
            except Provider.DoesNotExist:
                messages.error(request, 'No tienes una asociación activa.')
        elif 'accept_terms' in request.POST:
            provider, created = Provider.objects.get_or_create(user=request.user)
            provider.is_approved = True
            provider.save()
            request.user.is_staff = True
            request.user.save()
            messages.success(request, 'Has sido aprobado como socio.')
        else:
            messages.error(request, 'Debes aceptar los términos y condiciones.')
        return redirect('partnership')

@method_decorator(login_required, name='dispatch')    
class AboutTemplateView(View):
    template_name = 'about.html'
    
    def get(self, request):
        return render(request, self.template_name, {'user': request.user})
    
    def post(self, request):
        return render(request, self.template_name, {'user': request.user})
    
class LogoutTemplateView(View):
    template_name = 'index.html'
    
    def post(self, request):
        logout(request)
        return redirect('/') 
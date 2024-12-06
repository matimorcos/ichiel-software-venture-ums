"""
URL configuration for ums project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users.views import LoginTemplateView, LoginAPIView, RegisterTemplateView, RegisterSerializerTemplateView, HomeTemplateView, SearchUsersView, ProfileTemplateView, LogoutTemplateView 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginTemplateView.as_view(), name='login'),
    #path('login/', LoginAPIView.as_view(), name='login'),
    #path('register/', RegisterTemplateView.as_view(), name='register'),
    path('register/', RegisterSerializerTemplateView.as_view(), name='register'),
    path('home/', HomeTemplateView.as_view(), name='home'),
    path('search-users/', SearchUsersView.as_view(), name='search-users'),
    path('profile/', ProfileTemplateView.as_view(), name='profile'),
    path('logout/', LogoutTemplateView.as_view(), name='logout'),
]


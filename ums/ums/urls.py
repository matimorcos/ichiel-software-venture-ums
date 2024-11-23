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
from users.views import CustomLoginView, register_view, logout_view, dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CustomLoginView.as_view(), name='login'),
    path("dashboard/", dashboard_view, name="dashboard"),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
]

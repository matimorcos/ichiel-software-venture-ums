from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """ Admin shared class for User model. """
    list_display = ('email', 'username', 'first_name', 'last_name', 'role', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    

from django.apps import AppConfig

class UsersConfig(AppConfig):
    """Users application config."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Users Management'
    
    def ready(self):
        """Import users models."""
        import users.models 

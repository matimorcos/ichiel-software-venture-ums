from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserManager(BaseUserManager):
    """User manager for creating users and superusers for specific validations accurate as
    the obligatory email and username."""
    
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required.")
        if not username:
            raise ValueError("The Username field is required.")
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """ Create and return a new superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')
        
        return self.create_user(email, username, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    """User Django default model extended for manage additional fields, like role, adress, etc.
    This inherits from PermissionsMixin, allowing you to use Django's default permissions system,
    and overrides methods like has_perm and has_module_perms. Custom logic can be implemented
    if necessary."""
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    
    """Avoid multiple users models creations for each role, simplyfing code mantenance differentiating
    users behavior and autorization."""
    ROLES = (
        ("Customer", "Customer"),
        ("Provider", "Provider"),
    )
    
    email = models.EmailField(unique=True, max_length=255, verbose_name="email")
    username = models.CharField(unique=True, max_length=150, verbose_name="username")
    password = models.CharField(max_length=128, verbose_name="password")
    first_name = models.CharField(max_length=50, verbose_name="first name")
    last_name = models.CharField(max_length=50, verbose_name="last name")
    birthdate = models.DateField(blank=True, null=True, verbose_name="birthdate")
    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, verbose_name="city")
    postal_code = models.CharField(max_length=20, blank=True, null=True, verbose_name="postal code")
    address = models.TextField(blank=True, null=True, verbose_name="address")
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="phone number")
    role = models.CharField(max_length=10, choices=ROLES, default="Customer")
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]
    
    def __str__(self):
        """Return user username."""
        return f"{self.username} ({self.role})"

    def has_perm(self, perm, obj=None):
        """Return True if the user has the specified permission."""
        return True

    def has_module_perms(self, app_label):
        """Return True if the user has permissions to view the specified app."""
        return True

    def delete_user(self):
        """Soft delete a user marking them as inactive to comply with privacy regulations 
        and preserve referential integrity in the database."""
        self.is_active = False
        self.deleted_at = now()
        self.save()

    def update_user(self, **fields):
        """Update user fields."""
        for key, value in fields.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = now()
        self.save()

class Profile(models.Model):
    """Profile model. This avoids overloading the User model with too much information."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        """Return user username."""
        return self.user.username
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        """ Post save signal to automatically create and update a profile when a user is saved.
        This separates responsibilities (account data in User and personal data in Profile),
        which follows the Single Responsibility Principle design principle."""
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        """ Save user profile when a user is saved """
        instance.profile.save()

class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
"""class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    image = models.ImageField(upload_to='notifications/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title"""
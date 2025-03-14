from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class UserRole(models.TextChoices):
    SUPER_ADMIN = "Super Admin", "Super Admin"
    ADMIN = "Admin", "Admin"
    HR = "HR", "HR"
    EMPLOYEE = "Employee", "Employee"
    MANAGER = "Manager", "Manager"

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    role = models.CharField(max_length=100, choices=UserRole.choices, default=UserRole.EMPLOYEE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    REQUIRED_FIELDS = ["first_name", "last_name", "role"]

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

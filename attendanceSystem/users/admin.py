from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ['email', 'first_name', 'role', 'is_active', 'created_at']
    search_fields = ('email', 'first_name', 'role', 'is_active', 'created_at')
    list_filter = ('email', 'first_name', 'role', 'is_active',  'created_at')    
    fieldsets = (
        ('Personal info', {'fields': ('first_name', 'last_name', 'role', 'phone_number','email','is_active')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

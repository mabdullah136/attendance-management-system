from django.contrib import admin
from .models import Holiday

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ['title', 'from_date', 'to_date', 'description', 'created_by', 'created_at']
    search_fields = ['title', 'from_date', 'to_date', 'description', 'created_by', 'created_at']
    list_filter = ['title', 'from_date', 'to_date', 'description', 'created_by', 'created_at']


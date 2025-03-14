from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "check_in", "check_out", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__email", "user__first_name", "user__last_name")
    ordering = ("-created_at",)

from django.contrib import admin
from .models import LeaveRequest

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "leave_type", "start_date", "end_date", "status", "approved_by")
    list_filter = ("leave_type", "status")
    search_fields = ("user__email", "user__first_name", "user__last_name")
    ordering = ("-start_date",)

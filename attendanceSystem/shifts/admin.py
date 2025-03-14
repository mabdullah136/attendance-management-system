from django.contrib import admin
from .models import Shift, EmployeeShift

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ("name", "start_time", "end_time", "created_at")
    search_fields = ("name",)
    ordering = ("name",)

@admin.register(EmployeeShift)
class EmployeeShiftAdmin(admin.ModelAdmin):
    list_display = ("user", "shift", "start_date", "end_date")
    list_filter = ("shift", "start_date")
    search_fields = ("user__email", "user__first_name", "user__last_name", "shift__name")
    ordering = ("-start_date",)

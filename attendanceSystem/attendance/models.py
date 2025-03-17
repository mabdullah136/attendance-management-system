from django.db import models
from users.models import CustomUser

class AttendanceStatus(models.TextChoices):
    CHECK_IN = 'CHECK_IN', 'Check In'
    CHECK_OUT = 'CHECK_OUT', 'Check Out'
    MISSING_PUNCH = 'MISSING_PUNCH', 'Missing Punch'

class Attendance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=AttendanceStatus.choices, default=AttendanceStatus.CHECK_IN)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.status} ({self.created_at.date()})"

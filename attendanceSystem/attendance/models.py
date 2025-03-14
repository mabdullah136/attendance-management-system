from django.db import models
from users.models import CustomUser

class AttendanceStatus(models.TextChoices):
    PRESENT = "Present", "Present"
    ABSENT = "Absent", "Absent"
    LATE = "Late", "Late"
    HALF_DAY = "Half-Day", "Half-Day"
    LEAVE = "Leave", "Leave"

class Attendance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=AttendanceStatus.choices, default=AttendanceStatus.PRESENT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.status} ({self.created_at.date()})"

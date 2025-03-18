from django.db import models
from users.models import CustomUser

class LeaveType(models.TextChoices):
    SICK = "Sick Leave", "Sick Leave"
    CASUAL = "Casual Leave", "Casual Leave"
    ANNUAL = "Annual Leave", "Annual Leave"
    UNPAID = "Unpaid Leave", "Unpaid Leave"

class LeaveRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=50, choices=LeaveType.choices)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")], default="Pending")
    approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_leaves")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.leave_type} ({self.status})"

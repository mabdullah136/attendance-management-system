from django.db import models
from users.models import CustomUser

class Shift(models.Model):
    name = models.CharField(max_length=100, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class EmployeeShift(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.shift.name}"
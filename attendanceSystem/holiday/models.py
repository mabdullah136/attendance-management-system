from django.db import models
from users.models import CustomUser

class Holiday(models.Model):
    title = models.CharField(max_length=255) 
    from_date = models.DateField()
    to_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True) 
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) 

    class Meta:
        ordering = ["from_date"] 

    def __str__(self):
        return f"{self.title} on {self.from_date}"

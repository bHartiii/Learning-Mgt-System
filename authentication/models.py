from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    roles = (
        ("Admin", "Admin"),
        ("Mentor", "Mentor"),
        ("Student", "Student"),
    )
    mobile_number = models.CharField(max_length=10, default=None, null=True)
    role = models.CharField(null=False, blank=False, choices=roles, default="Admin", max_length=10)

    def __str__(self):
        return self.email 




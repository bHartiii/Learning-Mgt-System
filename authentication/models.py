from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    roles = (
        ("Admin", "Admin"),
        ("Mentor", "Mentor"),
        ("Student", "Student"),
    )
    mobile_number = models.CharField(max_length=10, default=None, null=True)
    email = models.EmailField(max_length=255, unique=True,  db_index=True)
    role = models.CharField(null=False, blank=False, choices=roles, default="Admin", max_length=10)
    first_login = models.BooleanField(default=False)
    created_by = models.ForeignKey('self',blank=True, null=True, on_delete=models.SET_NULL, related_name='created_by_user')
    upated_by = models.ForeignKey('self',blank=True, null=True, on_delete=models.SET_NULL, related_name='updated_by_user')

    def __str__(self):
        return self.email 

    def get_full_name(self):
        return self.first_name+" "+self.last_name


from django.contrib import admin
from django.urls import path
from learning_mgt.views import UpdateStudentDetails

urlpatterns = [
    path('update-details/', UpdateStudentDetails.as_view(), name='update-details'),
]

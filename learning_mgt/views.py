from django.shortcuts import render, redirect
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from learning_mgt.serializers import UpdateStudentDetailsSerializer
from learning_mgt.models import Student, EducationDetails

class UpdateStudentDetails(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateStudentDetailsSerializer

    def get_object(self):
        """
            Returns current logged in student profile instance
        """        
        return self.request.user.student
        
    def performe_update(self):
        """
            Save the updated user student instance
        """
        profile = serializer.save(student=self.request.user)
        return Response({'response': profile}, status=status.HTTP_200_OK)
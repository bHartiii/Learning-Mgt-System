from django.shortcuts import render, redirect
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from learning_mgt.serializers import UpdateStudentDetailsSerializer, UpdateEducationDetailsSerializer
from learning_mgt.models import Student, EducationDetails

class UpdateStudentDetails(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateStudentDetailsSerializer

    def get_object(self):
        """
            Returns current logged in student profile instance
        """        
        return self.request.user.student

    def get_education_details(self):
        return EducationDetails.object.get(student=self.get_object())
        
    def performe_update(self, serializer):
        """
            Save the updated user student instance
        """
        student = serializer.save(student=self.request.user)
        education_details_data = serializer.data['education_details']
        student_education = self.get_education_details()
        student_education.course = education_details_data['course'],
        student_education.percentage = education_details_data['percentage'],
        student_education.institution = education_details_data['institution']
        student_education.save(student=student)
        
        return Response({'response': student}, status=status.HTTP_200_OK)

class UpdateEducationDetails(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateEducationDetailsSerializer

    def get_object(self):
        return EducationDetails.objects.get(student=self.request.user.student)
        
    def performe_update(self, serializer):
        """
            Save the updated user student instance
        """
        student = serializer.save(student=self.request.user)
        return Response({'response': student}, status=status.HTTP_200_OK)
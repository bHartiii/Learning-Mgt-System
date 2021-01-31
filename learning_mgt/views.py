from django.shortcuts import render, redirect
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from learning_mgt.serializers import UpdateStudentDetailsSerializer, UpdateEducationDetailsSerializer, AddCourseSerializer, MentorSerializer, ListMentorsSerializer
from learning_mgt.models import Student, EducationDetails, Course, Mentor
from authentication.permissions import IsAdmin

class Courses(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = AddCourseSerializer


    def get_queryset(self):
        """
            Returns a list of all create courses
        """        
        return Course.objects.all()
        
    def perform_create(self, serializer):
        """
            create a new course instance
        """
        course = serializer.save()
        return Response({'response': course}, status=status.HTTP_201_CREATED)

class CourseDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = AddCourseSerializer
    queryset = Course.objects.all()
    lookup_field = "id"

    def perform_update(self,serializer):
        course = serializer.save()
        return Response({'response':course}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()
        return Response({'response': 'Course is deleted permanently.'}, status=status.HTTP_204_NO_CONTENT)
        

class Mentors(generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = MentorSerializer

    def put(self, request, mentor_id):
        try:
            mentor = Mentor.objects.get(id = mentor_id)
        except Mentor.DoesNotExist:
            return Response({'response':'Mentor does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        courses = serializer.validated_data['course']
        for course_data in courses:
            print(course_data)
            course = Course.objects.get(course_name=course_data)
            mentor.course.add(course.id)
            mentor.save()
        return Response({'response':'Course added successfully.'}, status=status.HTTP_200_OK)

    def get(self,request, mentor_id):

        mentor = Mentor.objects.filter(id=mentor_id)
        if mentor:
            serializer = ListMentorsSerializer(mentor, many=True)
            return Response({'response':serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'response':'Not Found'}, status=status.HTTP_404_NOT_FOUND)


class UpdateStudentDetails(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateStudentDetailsSerializer

    def get_object(self):
        """
            Returns current logged in student profile instance
        """        
        return self.request.user.student
        
    def perform_update(self, serializer):
        """
            Save the updated user student instance
        """
        student = serializer.save(student=self.request.user)
        return Response({'response': student}, status=status.HTTP_200_OK)
        

class UpdateEducationDetails(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateEducationDetailsSerializer

    def get_object(self):
        return EducationDetails.objects.get(student=self.request.user.student)
        
    def perform_update(self, serializer):
        """
            Save the updated user student instance
        """
        student = serializer.save(student=self.request.user)
        return Response({'response': student}, status=status.HTTP_200_OK)
from django.shortcuts import render, redirect
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from learning_mgt.serializers import UpdateStudentDetailsSerializer, UpdateEducationDetailsSerializer, AddCourseSerializer, MentorCourseMappingSerializer, MentorsSerializer
from learning_mgt.models import Student, EducationDetails, Course, Mentor
from authentication.permissions import IsAdmin, IsMentor, IsStudent

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
        
class Mentors(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = MentorsSerializer
    queryset = Mentor.objects.all()

    def get_queryset(self):
        return self.queryset.all()

class Mentordetails(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsMentor)
    serializer_class = MentorsSerializer
    lookup_field = "id"
    queryset = Mentor.objects.all()
    def get_queryset(self):
        user = self.request.user
        if user.role=='Mentor':
            return self.queryset.filter(mentor=user)
        elif user.role == 'Admin':
            return self.queryset.all()

class MentorCourseMapping(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = MentorCourseMappingSerializer

    def put(self, request, mentor_id):
        try:
            mentor = Mentor.objects.get(id = mentor_id)
        except Mentor.DoesNotExist:
            return Response({'response':'Mentor does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        courses = serializer.validated_data['course']
        for course_data in courses:
            course = Course.objects.get(course_name=course_data)
            mentor.course.add(course.id)
            mentor.save()
        return Response({'response':'Course added successfully.'}, status=status.HTTP_200_OK)

    def get(self,request, mentor_id):

        mentor = Mentor.objects.filter(id=mentor_id)
        if mentor:
            serializer = MentorsSerializer(mentor, many=True)
            return Response({'response':serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'response':'Not Found'}, status=status.HTTP_404_NOT_FOUND)


class UpdateStudentDetails(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = UpdateStudentDetailsSerializer
    queryset = Student.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        """
            Returns current logged in student profile instance
        """        
        if self.request.user.role == 'Student':
            return self.queryset.filter(student=self.request.user)
        else :
            return self.queryset.all()

    def perform_update(self, serializer):
        """
            Save the updated user student instance
        """
        student = serializer.save(student=self.request.user)
        return Response({'response': student}, status=status.HTTP_200_OK)
        

class UpdateEducationDetails(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = UpdateEducationDetailsSerializer
    queryset = EducationDetails.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        """
            Returns current logged in student profile instance
        """        
        if self.request.user.role == 'Student':
            return self.queryset.filter(student=self.request.user.student)
        else :
            return self.queryset.all()
        
    def perform_update(self, serializer):
        """
            Save the updated user student instance
        """
        student = serializer.save(student=self.request.user.student)
        return Response({'response': student}, status=status.HTTP_200_OK)
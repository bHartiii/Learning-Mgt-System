from django.shortcuts import render, redirect
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from learning_mgt.serializers import UpdateStudentDetailsSerializer, UpdateEducationDetailsSerializer, AddCourseSerializer, MentorCourseMappingSerializer, MentorsSerializer, MentorStudentMappingSerializer, MentorStudentUpdateMappingSerializer, MentorStudentListSerializer, PerformanceSerializer
from learning_mgt.models import Student, EducationDetails, Course, Mentor, MentorStudent, Performance
from authentication.permissions import IsAdmin, IsMentor, IsStudent, OnlyAdmin, IsMentorOrAdmin
from authentication.models import User


class UpdateStudentDetails(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = UpdateStudentDetailsSerializer
    queryset = Student.objects.all()
    lookup_field = "student_id"

    def get_queryset(self):
        """
            Returns current logged in student profile instance
        """        
        role = self.request.user.role
        if role == 'Student':
            return self.queryset.filter(student=self.request.user)
        elif role == "Mentor" :
            return self.queryset.filter(mentorstudent=Mentor.objects.get(mentor= self.request.user.id).id)
        else:
            return self.queryset.all()

    def perform_update(self, serializer):
        """
            Save the updated user student instance
        """
        user = self.request.user
        student = serializer.save(student=user, updated_by=user)
        return Response({'response': student}, status=status.HTTP_200_OK)


class EducationDetailsList(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = UpdateEducationDetailsSerializer
    queryset = EducationDetails.objects.all()
    lookup_field = "student_id"

    def get_queryset(self):
        """
            Returns current logged in student profile instance
        """        
        role = self.request.user.role
        if role == 'Student':
            return EducationDetails.objects.filter(student=self.request.user.student)
        elif role == "Mentor" :
            return self.queryset.filter(mentorstudent=self.request.user.id)
        else:
            return self.queryset.all()


class UpdateEducationDetailsByCourse(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = UpdateEducationDetailsSerializer
    queryset = EducationDetails.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        """
            Returns current logged in student profile instance
        """        
        role = self.request.user.role
        if role == 'Student':
            return EducationDetails.objects.filter(student=self.request.user.student)
        elif role == "Mentor" :
            return self.queryset.filter(mentorstudent=self.request.user.id)
        else:
            return self.queryset.all()
        
    def perform_update(self, serializer):
        """
            Save the updated user student instance
        """
        user = self.request.user
        student = serializer.save(student=user.student, updated_by=user)
        return Response({'response': student}, status=status.HTTP_200_OK)


class Courses(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, OnlyAdmin)
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
        course = serializer.save(created_by=self.request.user)
        return Response({'response': course}, status=status.HTTP_201_CREATED)

class CourseDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, OnlyAdmin)
    serializer_class = AddCourseSerializer
    queryset = Course.objects.all()
    lookup_field = "id"

    def perform_update(self,serializer):
        course = serializer.save(upated_by=self.request.user)
        return Response({'response':course}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()
        return Response({'response': 'Course is deleted permanently.'}, status=status.HTTP_204_NO_CONTENT)
        

class Mentors(generics.ListAPIView):
    permission_classes = (IsAuthenticated, OnlyAdmin)
    serializer_class = MentorsSerializer
    queryset = Mentor.objects.all()

    def get_queryset(self):
        return self.queryset.all()


class MentorCourseMapping(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, IsMentor)
    serializer_class = MentorCourseMappingSerializer
    queryset = Mentor.objects.all()
    
    def get_queryset(self, mentor_id):
        user = self.request.user
        if user.role=='Mentor':
            return self.queryset.filter(mentor=user.id)
        elif user.role == 'Admin':
            return self.queryset.filter(id=mentor_id)

    def put(self, request, mentor_id):
        try:
            mentor = Mentor.objects.get(id = mentor_id)
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            courses = serializer.validated_data['course']
            for course_data in courses:
                course = Course.objects.get(course_name=course_data)
                mentor.course.add(course.id)
                mentor.save(updated_by=self.request.user)
            return Response({'response':'Course added successfully.'}, status=status.HTTP_200_OK)
        except Mentor.DoesNotExist:
            return Response({'response':'Mentor does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def get(self,request, mentor_id):
        try:
            mentor = self.get_queryset(mentor_id)
            if mentor:
                serializer = MentorsSerializer(mentor, many=True)
                return Response({'response':serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'response':'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        except Mentor.DoesNotExist:
            return Response({'response':'This mentor does not exist'}, status=status.HTTP_404_NOT_FOUND)


class MentorStudentMapping(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, IsMentor)
    serializer_class = MentorStudentMappingSerializer
    queryset = MentorStudent.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        mentor_data = serializer.validated_data['mentor']
        course_data = serializer.validated_data['course']
        mentor = Mentor.objects.get(mentor=User.objects.get(email=mentor_data))
        if course_data in mentor.course.all():
            serializer.save(created_by=self.request.user)
            return Response({'response':'Mentor added successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'response':'This mentor is not assigned for this course!!!'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        if request.user.role == 'Admin':
            students = self.queryset.all()
        else:
            students = self.queryset.filter(mentor=Mentor.objects.get(mentor=request.user))
        serializer = MentorStudentListSerializer(students, many=True)
        return Response({'response':serializer.data}, status=status.HTTP_200_OK)

class MentorStudentDetails(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, IsMentor)
    serializer_class = MentorStudentUpdateMappingSerializer
    
    def get_queryset(self, search_id):
        user = self.request.user
        try:
            if self.request.user.role == 'Admin':
                students = MentorStudent.objects.get(id=search_id)
            else:
                students = MentorStudent.objects.get(id=search_id, mentor=Mentor.objects.get(mentor=user))
            return students
        except MentorStudent.DoesNotExist:
            return Response({'response': 'This record does not exist'}, status=status.HTTP_404_NOT_FOUND)
        

    def put(self, request, search_id):
        students = self.get_queryset(search_id)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        mentor_data = serializer.validated_data['mentor']
        course_data = serializer.validated_data['course']
        mentor = Mentor.objects.get(mentor=User.objects.get(email=mentor_data))
        if course_data in mentor.course.all():
            students.course = course_data
            students.mentor = mentor
            students.save(updated_by=user)
            return Response({'response':'Mentor added successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'response':'This mentor is not assigned for this course!!!'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,search_id ):
        students = self.get_queryset(search_id)
        serializer = MentorStudentListSerializer(students)
        return Response({'response':serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, search_id):   
        students = self.get_queryset(search_id)
        students.delete()
        return Response({'response': 'Record is deleted successfully!!'}, status=status.HTTP_204_NO_CONTENT)

class PerformanceAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsMentorOrAdmin)
    serializer_class = PerformanceSerializer
    queryset = Performance.objects.all()
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return self.queryset.all()
        else:
            return self.queryset.filter(mentor=user.id)

class PerformanceDetailsAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsMentorOrAdmin)
    serializer_class = PerformanceSerializer
    queryset = Performance.objects.all()
    lookup_field = "id"
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return self.queryset.all()
        else:
            return self.queryset.filter(mentor=user.id)

    def perform_update(self, serializer):
        user = self.request.user
        student = serializer.save(updated_by=user)
        return Response({'response': student}, status=status.HTTP_200_OK)        

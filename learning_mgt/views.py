from django.shortcuts import render, redirect
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from learning_mgt.serializers import UpdateStudentDetailsSerializer, UpdateEducationDetailsSerializer, AddCourseSerializer, MentorCourseMappingSerializer, MentorsSerializer, MentorStudentMappingSerializer, MentorStudentUpdateMappingSerializer, MentorStudentListSerializer, PerformanceSerializer
from learning_mgt.models import Student, EducationDetails, Course, Mentor, MentorStudent, Performance
from authentication.permissions import IsAdmin, IsMentor, IsStudent, OnlyAdmin, IsMentorOrAdmin
from authentication.models import User


class UpdateStudentDetails(generics.RetrieveUpdateAPIView):
    """
        Summary:
        --------
            This class will let authorized user to get and update .
        --------
        Methods:
            get_queryset : It will let authorized user to get student-details.
            perform_update : Student will able to update the details.
    """
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = UpdateStudentDetailsSerializer
    queryset = Student.objects.all()
    lookup_field = "student_id"

    def get_queryset(self):
        """
            Returns current logged in student profile instance
        """        
        role = self.request.user.role
        try:
            if role == 'Student':
                return self.queryset.filter(student=self.request.user)
            elif role == "Mentor" :
                return self.queryset.filter(mentorstudent=Mentor.objects.get(mentor= self.request.user.id).id)
            else:
                return self.queryset.all()
        except Exception:
            return []

    def perform_update(self, serializer):
        """
            Save the updated user student instance
        """
        user = self.request.user
        student = serializer.save(student=user, updated_by=user)
        return Response({'response': student}, status=status.HTTP_200_OK)


class EducationDetailsList(generics.ListAPIView):
    """
        Summary:
        --------
            This class will let authorized user to get education-details.
        --------
        Methods:
            get_queryset : It will let authorized user to get education-details based on the user-role.
    """
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = UpdateEducationDetailsSerializer
    queryset = EducationDetails.objects.all()

    def get_queryset(self):
        """
            Returns current logged in student profile instance
        """        
        role = self.request.user.role
        try:
            if role == 'Student':
                return self.queryset.filter(student=Student.objects.get(student=self.request.user))
            elif role == "Mentor" :
                return self.queryset.filter(student=Student.objects.get(mentorstudent=Mentor.objects.get(mentor= self.request.user.id).id))
            else:
                return self.queryset.all()
        except Exception:
            return []


class UpdateEducationDetailsByCourse(generics.RetrieveUpdateAPIView):
    """
        Summary:
        --------
            This class will let authorized user to get education-details by course.
        --------
        Methods:
            get_queryset : It will return single record of education details.
            perform_update : Student will able to update the details.
    """
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = UpdateEducationDetailsSerializer
    queryset = EducationDetails.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        """
            Returns current logged in student profile instance
        """        
        role = self.request.user.role
        try:
            if role == 'Student':
                return self.queryset.filter(student=self.request.user.student)
            elif role == "Mentor" :
                return self.queryset.filter(student=Student.objects.get(mentorstudent=Mentor.objects.get(mentor= self.request.user.id).id))
            else:
                return self.queryset.all()
        except Exception:
            return []
        
    def perform_update(self, serializer):
        """
            Save the updated user student instance
        """
        user = self.request.user
        student = serializer.save(student=user.student, updated_by=user)
        return Response({'response': student}, status=status.HTTP_200_OK)


class Courses(generics.ListCreateAPIView):
    """
        Summary:
        --------
            This class will let admin to create and list courses.
        --------
        Methods:
            get_queryset : Admin will get all the courses.
            perform_create : Admin will able to create new course.
    """
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
    """
        Summary:
        --------
            This class will let admin user to get, update, delete course.
        --------
        Methods:
            perform_update : Admin will be update the course.
            perform_destroy : Admin will be able to delete the course.
    """
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
    """
        Summary:
        --------
            This class will let admin to get all mentors.
        --------
        Methods:
            get_queryset : It will return mentor list.
    """
    permission_classes = (IsAuthenticated, OnlyAdmin)
    serializer_class = MentorsSerializer
    queryset = Mentor.objects.all()

    def get_queryset(self):
        return self.queryset.all()


class MentorCourseMapping(generics.GenericAPIView):
    """
        Summary:
        --------
            This class will let admin to map mentor and courses.
        --------
        Methods:
            get_queryset : It return queryset according to user role.
            get : It will return mentor-courses details by mentor_id.
            put : The courses will be added to fetched mentor.
    """
    permission_classes = (IsAuthenticated, IsMentor)
    serializer_class = MentorCourseMappingSerializer
    queryset = Mentor.objects.all()
    
    def get_queryset(self, mentor_id):
        user = self.request.user
        if user.role=='Mentor':
            return self.queryset.filter(mentor=user.id)
        elif user.role == 'Admin':
            return self.queryset.filter(mentor=mentor_id)

    def put(self, request, mentor_id):
        try:
            mentor = Mentor.objects.get(mentor = mentor_id)
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            courses = serializer.validated_data['course']
            for course_data in courses:
                course = Course.objects.get(course_name=course_data)
                mentor.course.add(course.id)
                mentor.updated_by=self.request.user
                mentor.save()
            return Response({'response':'Course added successfully.'}, status=status.HTTP_200_OK)
        except Mentor.DoesNotExist:
            return Response({'response':'Mentor does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def get(self,request, mentor_id):
        try:
            mentor = self.get_queryset(mentor_id)
            if mentor:
                serializer = MentorsSerializer(mentor, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'response':'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        except Mentor.DoesNotExist:
            return Response({'response':'This mentor does not exist'}, status=status.HTTP_404_NOT_FOUND)


class MentorStudentMapping(generics.GenericAPIView):
     """
        Summary:
        --------
            This class will let admin to map mentor-course and students.
        --------
        Methods:
            get : It will return mentor-courses details according to user role.
            post : It will create a new record to map student and mentor-course.
    """
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
        try:
            if request.user.role == 'Admin':
                students = self.queryset.all()
            else:
                students = self.queryset.filter(mentor=Mentor.objects.get(mentor=request.user))
            serializer = MentorStudentListSerializer(students, many=True)
            return Response({'response':serializer.data}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'response':'No mentor-student mapping is done for you!!!'}, status=status.HTTP_404_NOT_FOUND)

class MentorStudentDetails(generics.GenericAPIView):
     """
        Summary:
        --------
            This class will let admin to get and update the details of mapped mentor-course and students.
        --------
        Methods:
            get_queryset : It return queryset according to user role and student_id.
            get : It will return mentor-courses details by student_id.
            put : The courses or mentor can be updated to fetched student.
    """
    permission_classes = (IsAuthenticated, IsMentor)
    serializer_class = MentorStudentUpdateMappingSerializer
    
    def get_queryset(self, student_id):
        user = self.request.user
        try:
            if self.request.user.role == 'Admin':
                students = MentorStudent.objects.get(student=student_id)
            else:
                students = MentorStudent.objects.get(student=student_id, mentor=Mentor.objects.get(mentor=user))
            return students
        except MentorStudent.DoesNotExist:
            return Response({'response': 'This record does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({'response': 'Something went wrong!!!!'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, student_id):
        students = self.get_queryset(student_id)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        mentor_data = serializer.validated_data['mentor']
        course_data = serializer.validated_data['course']
        try:
            mentor = Mentor.objects.get(mentor=User.objects.get(email=mentor_data))
            if course_data in mentor.course.all():
                students.course = course_data
                students.mentor = mentor
                students.updated_by = request.user
                students.save()
                return Response({'response':'Mentor added successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'response':'This mentor is not assigned for this course!!!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'response':'Something went wrong!!!'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,student_id ):
        students = self.get_queryset(student_id)
        serializer = MentorStudentListSerializer(students)
        return Response({'response':serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, student_id):   
        students = self.get_queryset(student_id)
        students.delete()
        return Response({'response': 'Record is deleted successfully!!'}, status=status.HTTP_204_NO_CONTENT)

class PerformanceAPI(generics.ListAPIView):
     """
        Summary:
        --------
            This class will let authorized user to get list of performances of all students.
        --------
        Methods:
            get_queryset : It will return all performances objects.
    """
    permission_classes = (IsAuthenticated, IsMentorOrAdmin)
    serializer_class = PerformanceSerializer
    queryset = Performance.objects.all()
    
    def get_queryset(self):
        user = self.request.user
        try:
            if user.role == 'Admin':
                performance = self.queryset.all()
            elif user.role == 'Student':
                performance = self.queryset.filter(student=Student.objects.get(student=user))
            else:
                performance = self.queryset.filter(mentor=Mentor.objects.get(mentor=user))
            return performance
        except Exception:
            return []

class PerformanceDetailsAPI(generics.RetrieveUpdateDestroyAPIView):
     """
        Summary:
        --------
            This class will let authorized user to create and get performance object by id.
        --------
        Methods:
            get_queryset : It returns performances view according to user role.
            perform_update : Admin or mentor will be able to update performance.
    """
    permission_classes = (IsAuthenticated, IsMentorOrAdmin)
    serializer_class = PerformanceSerializer
    queryset = Performance.objects.all()
    lookup_field = "id"
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            performance = self.queryset.all()
        elif user.role == 'Student':
            performance = self.queryset.filter(student=Student.objects.get(student=user))
        else:
            performance = self.queryset.filter(mentor=Mentor.objects.get(mentor=user))
        return performance

    def perform_update(self, serializer):
        user = self.request.user
        student = serializer.save(updated_by=user)
        return Response({'response': student}, status=status.HTTP_200_OK)        

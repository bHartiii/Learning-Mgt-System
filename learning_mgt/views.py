from django.shortcuts import render, redirect
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from learning_mgt.serializers import UpdateStudentDetailsSerializer, UpdateEducationDetailsSerializer, AddCourseSerializer, MentorCourseMappingSerializer, MentorsSerializer, MentorStudentMappingSerializer, MentorStudentUpdateMappingSerializer, MentorStudentListSerializer, PerformanceSerializer
from learning_mgt.models import Student, EducationDetails, Course, Mentor, MentorStudent, Performance
from authentication.permissions import IsAdmin, IsMentor, IsStudent, OnlyAdmin, IsMentorOrAdmin
from authentication.models import User
import logging
logger = logging.getLogger('django')

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
        try:
            student = []
            user = self.request.user
            if user.role == 'Student':
                logger.info(f"student details view of {user} for student.")
                return self.queryset.filter(student=user)
            elif user.role == "Mentor" :
                logger.info(f"student details view of {user} for mentor.")
                return self.queryset.filter(mentorstudent=Mentor.objects.get(mentor=user.id).id)
            else:
                logger.info(f"student details view for admin.")
                return self.queryset.all()
        except Student.DoesNotExist:
            logger.error("This student does not exist.")
            return student
        except Exception as e:
            logger.error(e)
            return student

    def perform_update(self, serializer):
        """
            Save the updated user student instance
        """
        try:
            user = self.request.user
            student = serializer.save(student=user, updated_by=user)
            logger.info(f"Student details are updated for {user}.")
            return Response({'response': student}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e)
            return Response({"response":"Something went wrong !!!"}, status=status.HTTP_400_BAD_REQUEST)


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
        try:
            user = self.request.user
            student = []
            if user.role == 'Student':
                logger.info(f"Education details of {user} are fetched for student")
                return self.queryset.filter(student=Student.objects.get(student=user))
            elif user.role == "Mentor" :
                logger.info(f"Education details of {user} are fetched for mentor")
                return self.queryset.filter(student=Student.objects.get(mentorstudent=Mentor.objects.get(mentor=user.id).id))
            else:
                logger.info(f"Education details are fetched for admin")
                return self.queryset.all()
        except Student.DoesNotExist:
            logger.error("The student does not exist.")
            return student            
        except EducationDetails.DoesNotExist:
            logger.error("The student does not exist.")
            return student
        except Exception as e:
            logger.error(e)
            return student


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
        try:
            education_details = []
            user = self.request.user
            if role == 'Student':
                logger.info(f"Education details view of {user} for student.")
                return self.queryset.filter(student=user.student)
            elif role == "Mentor" :
                logger.info(f"Education details view of {user} for mentor.")
                return self.queryset.filter(student=Student.objects.get(mentorstudent=Mentor.objects.get(mentor=user.id).id))
            else:
                logger.info(f"Education details view for admin.")
                return self.queryset.all()
        except Student.DoesNotExist:
            logger.error("The student does not exist.")
            return education_details            
        except EducationDetails.DoesNotExist:
            logger.error("The student does not exist.")
            return education_details
        except Exception as e:
            logger.error(e)
            return education_details
        
    def perform_update(self, serializer):
        """
            Save the updated user student instance
        """
        try:
            user = self.request.user
            student = serializer.save(student=user.student, updated_by=user)
            logger.info(f"Education detail is updated for {user}.")
            return Response({'response': student}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e)
            return Response({"response":"Something went wrong!!!"}, status=status.HTTP_400_BAD_REQUEST)


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
    queryset = Course.objects.all()

    def get_queryset(self):
        """
            Returns a list of all create courses
        """        
        try:
            courses = []
            logger.info("Course list is fetched.")
            return self.queryset.all()
        except Exception as e : 
            logger.error(e)
            return courses

    def perform_create(self, serializer):
        """
            create a new course instance
        """
        try:
            course = serializer.save(created_by=self.request.user)
            logger.info("New course is created.")
            return Response({'response': course}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(e)
            return Response({"response":"Somethin went wrong!!!"}, status=status.HTTP_400_BAD_REQUEST)

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
        try:
            course = serializer.save(upated_by=self.request.user)
            logger.info(f"Course detail {course} is updated!!!")
            return Response({'response':course}, status=status.HTTP_200_OK)
        except Exception as e :
            logger.error(e)
            return Response({"response":"Something went wrong!!!"}, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        try:
            instance.delete()
            logger.info(f"Course {instance} is deleted.")
            return Response({'response': 'Course is deleted permanently.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(e)
            return Response({"response":"Something went wrong!!!"}, status=status.HTTP_400_BAD_REQUEST)

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
        try:
            mentors = []
            logger.info("Mentor list is fetched!!!")
            return self.queryset.all()
        except Exception as e :
            logger.error(e)
            return mentors


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
            logger.info(f"Course list is updated for mentor {mentor}")
            return Response({'response':'Course added successfully.'}, status=status.HTTP_200_OK)
        except Mentor.DoesNotExist:
            logger.error("Mentor does not exist.")
            return Response({'response':'Mentor does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(e)
            return Response({"reposne":"Something went wrong!!!"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request, mentor_id):
        try:
            mentor = self.get_queryset(mentor_id)
            if mentor:
                serializer = MentorsSerializer(mentor, many=True)
                logger.info("Mentor details is fetched.")
                return Response({"response":serializer.data}, status=status.HTTP_200_OK)
            else:
                logger.info("Mentor details not found.")
                return Response({'response':'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        except Mentor.DoesNotExist:
            logger.error("Mentor does not exist.")
            return Response({'response':'This mentor does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(e)
            return Response({'response':'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        


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
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            mentor_data = serializer.validated_data['mentor']
            course_data = serializer.validated_data['course']
            mentor = Mentor.objects.get(mentor=User.objects.get(email=mentor_data))
            if course_data in mentor.course.all():
                serializer.save(created_by=self.request.user)
                logger.info("New Mentor-Studnet mapping is done.")
                return Response({'response':'Mentor is added for student successfully.'}, status=status.HTTP_200_OK)
            else:
                logger.info("This mentor is not assigned for this course!!!")
                return Response({'response':'This mentor is not assigned for this course!!!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({"response": "Something went wrong!!!"})

    def get(self,request):
        try:
            if request.user.role == 'Admin':
                students = self.queryset.all()
            else:
                students = self.queryset.filter(mentor=Mentor.objects.get(mentor=request.user))
            serializer = MentorStudentListSerializer(students, many=True)
            logger.info("Mentor-student data is fetched.")
            return Response({'response':serializer.data}, status=status.HTTP_200_OK)
        except MentorStudent.DoesNotExist:
            logger.error("No mentor-student mapping is done!!!")
            return Response({'response':'No mentor-student mapping is done for you!!!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(e)
            return Response({"response":"Something went wrong!!!"}, status=status.HTTP_400_BAD_REQUEST)

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
        try:
            user = self.request.user
            if self.request.user.role == 'Admin':
                students = MentorStudent.objects.get(student=student_id)
            else:
                students = MentorStudent.objects.get(student=student_id, mentor=Mentor.objects.get(mentor=user))
            logger.info("Mentor-student details is fetched.")
            return students
        except MentorStudent.DoesNotExist:
            logger.error("This mentor-student does not exist")
            return Response({'response': 'This mentor-student record does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(e)
            return Response({'response': 'Something went wrong!!!!'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, student_id):
        try:
            students = self.get_queryset(student_id)
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            mentor_data = serializer.validated_data['mentor']
            course_data = serializer.validated_data['course']
            mentor = Mentor.objects.get(mentor=User.objects.get(email=mentor_data))
            if course_data in mentor.course.all():
                students.course = course_data
                students.mentor = mentor
                students.updated_by = request.user
                students.save()
                logger.info("Mentor is updated successfully.")
                return Response({'response':'Mentor is updated successfully.'}, status=status.HTTP_200_OK)
            else:
                logger.info("This mentor is not assigned for this course!!!")
                return Response({'response':'This mentor is not assigned for this course!!!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'response':'Something went wrong!!!'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,student_id ):
        try:
            students = self.get_queryset(student_id)
            serializer = MentorStudentListSerializer(students)
            return Response({'response':serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"response":"Something went wrong!!!"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, student_id):  
        try: 
            students = self.get_queryset(student_id)
            students.delete()
            logger.info("Mentor-studnet record is deleted successfully!!")
            return Response({'response': 'Mentor-studnet record is deleted successfully!!'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(e)
            return Response({"response":"Something went wrong."}, status=status.HTTP_400_BAD_REQUEST)

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
                logger.info("Performance list for admin is fetched!!!")
            elif user.role == 'Student':
                logger.info("Performance list for student is fetched!!!")
                performance = self.queryset.filter(student=Student.objects.get(student=user))
            else:
                logger.info("Performance list for mentor is fetched!!!")
                performance = self.queryset.filter(mentor=Mentor.objects.get(mentor=user))
            return performance
        except Exception as e:
            logger.error(e)
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
        try:
            user = self.request.user
            if user.role == 'Admin':
                performance = self.queryset.all()
                logger.info(f"Performance view of {user} for admin.")
            elif user.role == 'Student':
                logger.info(f"Performance view of {user} for student.")
                performance = self.queryset.filter(student=Student.objects.get(student=user))
            else:
                logger.info(f"Performance view of {user} for mentor.")
                performance = self.queryset.filter(mentor=Mentor.objects.get(mentor=user))
            return performance
        except Performance.DoesNotExist:
            logger.error(f"This performance record for {user} does not exist.")
            return []
        except Exception as e:
            logger.error(e)
            return []

    def perform_update(self, serializer):
        try:
            user = self.request.user
            student = serializer.save(updated_by=user)
            logger.info(f"Performance is updateed for {user}")
            return Response({'response': student}, status=status.HTTP_200_OK)        
        except Exception as e:
            logger.error(e)
            return Response({"response":"Something went wrong!!!"}, status=status.HTTP_400_BAD_REQUEST)
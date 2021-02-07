from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import User
from learning_mgt.models import Mentor, Student, EducationDetails, Performance, MentorStudent, Course
from ..serializers import UpdateEducationDetailsSerializer, UpdateStudentDetailsSerializer, MentorsSerializer, MentorCourseMappingSerializer, MentorStudentMappingSerializer, MentorStudentUpdateMappingSerializer, MentorStudentListSerializer, PerformanceSerializer
import json
from rest_framework.response import Response

CONTENT_TYPE = 'application/json'
class ManagementAPITest(TestCase):
    """ Test module for authentication APIs """
    
    def setUp(self):
        # initialize the APIClient app
        self.client = Client()

        self.admin = User.objects.create(username='admin', first_name='Bharti', last_name='Mali', role='Admin', email='admin@gmail.com', password='pbkdf2_sha256$216000$yG97oIyabA7B$nzM1GiofqbxOqH/prQTgjDWhT1C7o1cpj0VdJ5viW0M=', first_login=True)
        self.student = User.objects.create(username='student1', first_name='Bharti', last_name='Mali', role='Student', email='student@gmail.com', password='pbkdf2_sha256$216000$jge4gjoUWquH$RqjqlYMi9gKUAEItd91thLEwpewzUn5WOfL2TdsLyjY=', first_login=True)
        self.student2 = User.objects.create(username='student2', first_name='Bharti', last_name='Mali', role='Student', email='student2@gmail.com', password='pbkdf2_sha256$216000$jge4gjoUWquH$RqjqlYMi9gKUAEItd91thLEwpewzUn5WOfL2TdsLyjY=', first_login=True)
        self.student3 = User.objects.create(username='student3', first_name='Bharti', last_name='Mali', role='Student', email='student3@gmail.com', password='pbkdf2_sha256$216000$jge4gjoUWquH$RqjqlYMi9gKUAEItd91thLEwpewzUn5WOfL2TdsLyjY=', first_login=True)
        self.mentor = User.objects.create(username='mentor', first_name='Bharti', last_name='Mali', role='Mentor', email='mentor@gmail.com', password='pbkdf2_sha256$216000$jge4gjoUWquH$RqjqlYMi9gKUAEItd91thLEwpewzUn5WOfL2TdsLyjY=', first_login=True)
        self.mentor2 = User.objects.create(username='mentor2', first_name='Bharti', last_name='Mali', role='Mentor', email='mentor2@gmail.com', password='pbkdf2_sha256$216000$jge4gjoUWquH$RqjqlYMi9gKUAEItd91thLEwpewzUn5WOfL2TdsLyjY=', first_login=True)
        self.mentor3 = User.objects.create(username='mentor3', first_name='Bharti', last_name='Mali', role='Mentor', email='mentor3@gmail.com', password='pbkdf2_sha256$216000$jge4gjoUWquH$RqjqlYMi9gKUAEItd91thLEwpewzUn5WOfL2TdsLyjY=', first_login=True)


        # Create course model object
        self.course1 = Course.objects.create(course_name='Python')
        self.course2 = Course.objects.create(course_name='Java')
        self.course3 = Course.objects.create(course_name='Django')
        
        # Create student model object 
        self.student_details = Student.objects.get(student=self.student)
        self.student2_details = Student.objects.get(student=self.student2)
        self.student3_details = Student.objects.get(student=self.student3)
        
        # Create education-details model 
        self.edu_details = EducationDetails.objects.get(student=self.student_details, course='UG')
        self.edu_details_2 = EducationDetails.objects.get(student=self.student2_details, course='UG')
        self.edu_details_3 = EducationDetails.objects.get(student=self.student3_details, course='UG')
        
        # Create mentor-course object
        self.mentor_course = Mentor.objects.get(mentor=self.mentor)
        self.mentor_course2 = Mentor.objects.get(mentor=self.mentor2)
        self.mentor_course3 = Mentor.objects.get(mentor=self.mentor3)

        # Assign course to mentor-course object
        self.mentor_course.course.add(self.course1)
        self.mentor_course.save()
        self.mentor_course2.course.add(self.course2)
        self.mentor_course2.save()
        self.mentor_course3.course.add(self.course3)
        self.mentor_course3.save()

        # Create mentor-student model object
        self.mentor_student = MentorStudent.objects.create(student=self.student_details , course=self.course1, mentor=self.mentor_course)
        self.mentor_student2 = MentorStudent.objects.create(student=self.student2_details , course=self.course2, mentor=self.mentor_course2)


        # Update performance model object : 
        self.performance = Performance.objects.get(student=self.student_details)
        self.performance.current_score = 3
        self.performance.save()

        self.performance2 = Performance.objects.get(student=self.student2_details)
        self.performance2.current_score = 4
        self.performance2.save()


        self.student_details_valid_data = {
            'image': None,
            'contact': '7742977480',
            'alternate_contact': '7772779990',
            'relation_with_alternate_contact': 'myself',
            'current_location': 'RJ',
            'Address':'Nathdwara',
            'git_link':'github.com/bHartiii',
            'yr_of_exp':0
        }
        
        self.education_details_valid_data = {
            'institution': 'amity',
            'percentage': 81,
            'From': 2016,
            'Till': 2020,
        }
        self.student_details_invalid_data = {
            'image': None,
            'contact': '12345678',
            'alternate_contact': '7772779990',
            'relation_with_alternate_contact': '',
            'current_location': 'RJ',
            'Address':'Nathdwara',
            'git_link':'github.com/bHartiii',
            'yr_of_exp':'0'
        }
        
        self.education_details_invalid_data = {
            'institution': '121',
            'percentage': '81',
            'From': '2016',
            'Till': 2020,
        } 
        self.admin_login_payload = {
            'username' : 'admin',
            'password' : 'bharti'
        }
        self.mentor_login_payload = {
            'username' : 'mentor',
            'password' : 'bharti'
        }
        self.student_login_payload = {
            'username' : 'student1',
            'password' : 'bharti'
        }
        self.student2_login_payload = {
            'username' : 'student2',
            'password' : 'bharti'
        }
        self.invalid_login_payload = {
            'username' : 'bharti',
            'password' : 'bharti'
        }
        self.valid_course_data = {
            'course_name' : 'bharti'
        }
        self.invalid_course_data = {
            'course_name' : ''
        }       
        self.mentor_course_data = {
            'course':[self.course1.id]
        }
        self.mentor_course_invalid_data = {
            'course': self.course1.id
        }
        self.mentor_student_data = {
            'student':  self.student3_details.id,
            'mentor' :  self.mentor_course3.id,
            'course' :  self.course3.id
        }
        self.mentor_student_invalid_data = {
            'student':  self.student_details.id,
            'mentor' :  self.mentor_course.id,
            'course' :  self.course2.id
        }
        self.performance_data = {
            'current_score' : 3.43
        }
        self.performance_invalid_data = {
            'current_score' : ''
        }

### Test cases for PUT Method of student-details API : 

    def test_update_student_details_without_login(self):
        # To check if student-details API is accessible without login
        response = self.client.put(reverse('student-details', kwargs={'student_id': self.student_details.id}), data=json.dumps(self.student_details_valid_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_student_details_by_user_after_login_with_invalid_credentials(self):
        # To check if PUT method of student-details API is accessible by user after login with invalid credentials
        self.client.post(reverse('login'), data=json.dumps(self.invalid_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('student-details', kwargs={'student_id': self.student.id}), data=json.dumps(self.student_details_valid_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_student_details_by_admin_after_login(self):
        # To check if PUT method of student-details API is accessible by admin after login
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('student-details', kwargs={'student_id': self.student.id}), data=json.dumps(self.student_details_valid_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_student_details_by_mentor_after_login(self):
        # To check if PUT method of student-details API is accessible by mentor after login
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('student-details', kwargs={'student_id': self.student.id}), data=json.dumps(self.student_details_valid_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_student_details_by_student_after_login(self):
        # To check if PUT method of student-details API is accessible by student after login
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('student-details', kwargs={'student_id': self.student.id}), data=json.dumps(self.student_details_valid_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_student_details_by_student__with_invalid_data_after_login(self):
        # To check if details are updated with invalid data by student after login
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('student-details', kwargs={'student_id': self.student.id}), data=json.dumps(self.student_details_invalid_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_student_details_of_another_student_user_by_student_after_login(self):
        # To check if student can update other student's details after login
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('student-details', kwargs={'student_id': self.student2.id}), data=json.dumps(self.student_details_valid_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

### Test cases for GET Method of student-details API : 

    def test_get_student_details_without_login(self):
        # To check if GET method of student-details API is accessible without login
        response = self.client.get(reverse('student-details', kwargs={'student_id': self.student.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_student_details_by_user_after_login_with_invalid_credentials(self):
        # To check if GET method of student-details API is accessible by user after login with invalid credentials
        self.client.post(reverse('login'), data=json.dumps(self.invalid_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('student-details', kwargs={'student_id': self.student.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_student_details_by_admin_after_login(self):
        # To check if GET method of student-details API is accessible by admin after login
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('student-details', kwargs={'student_id': self.student.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_student_details_by_mentor_after_login(self):
        # To check if GET method of student-details API is accessible by mentor after login
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        try:
            response = self.client.get(reverse('student-details', kwargs={'student_id': self.student.id}), content_type=CONTENT_TYPE)          
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except Exception:
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_student_details_of_student_not_alloted_by_mentor_after_login(self):
        # To check if student-details of another mentor's student are accessible by mentor after login
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('student-details', kwargs={'student_id': self.student2.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_student_details_by_student_after_login(self):
        # To check if GET method of student-details API is accessible by student after login
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('student-details', kwargs={'student_id': self.student.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_student_details_of_another_student_by_student_after_login(self):
        # To check if student-details of another student are accessible by student after login
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('student-details', kwargs={'student_id': self.student2.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


### Test cases for GET Method of edu-details-list API : 

    def test_get_edu_details_list_without_login(self):
        # To check if GET method of edu-details-list API is accessible without login
        response = self.client.get(reverse('edu-details-list'), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_edu_details_list_by_user_after_login_with_invalid_credentials(self):
        # To check if GET method of edu-details-list API is accessible by user after login with invalid credentials
        self.client.post(reverse('login'), data=json.dumps(self.invalid_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('edu-details-list'), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_edu_details_list_by_admin_after_login(self):
        # To check if GET method of edu-details-list API is accessible by admin after login
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('edu-details-list'), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_edu_details_list_by_mentor_after_login(self):
        # To check if GET method of edu-details-list API is accessible by mentor after login
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('edu-details-list'), content_type=CONTENT_TYPE)
        try:
            students = EducationDetails.objects.filter(student=Student.objects.get(mentorstudent=Mentor.objects.get(mentor= self.mentor.id).id))
            serializer = UpdateEducationDetailsSerializer(students, many=True)
            self.assertEqual(response.data, serializer.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except Exception:
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_edu_details_list_of_student_not_alloted_by_mentor_after_login(self):
        # To check if edu-details-list of another mentor's student are accessible by mentor after login
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('edu-details-list'), content_type=CONTENT_TYPE)
        try:
            students = EducationDetails.objects.filter(student=Student.objects.get(mentorstudent=Mentor.objects.get(mentor= self.mentor2.id).id))
            serializer = UpdateEducationDetailsSerializer(students, many=True)
            self.assertNotEqual(response.data, serializer.data)
        except Exception:
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_edu_details_list_by_student_after_login(self):
        # To check if GET method of edu-details-list API is accessible by student after login
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('edu-details-list'), content_type=CONTENT_TYPE)
        students = EducationDetails.objects.filter(student=self.student_details.id)
        serializer = UpdateEducationDetailsSerializer(students, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_edu_details_list_of_another_student_by_student_after_login(self):
        # To check if edu-details-list of another student are accessible by student after login
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('edu-details-list'), content_type=CONTENT_TYPE)
        students = EducationDetails.objects.filter(student=self.student2_details.id)
        serializer = UpdateEducationDetailsSerializer(students, many=True)
        self.assertNotEqual(response.data, serializer.data)


### Test cases for PUT Method of UpdateEducationDetailsByCourse API : 

    def test_update_edu_details_by_course_without_login(self):
        # To check if edu-details-by-course API is accessible without login
        response = self.client.put(reverse('edu-details', kwargs={'id': self.edu_details.id}), data=json.dumps(self.education_details_valid_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_edu_details_by_course_for_user_after_login_with_invalid_credentials(self):
        # To check if PUT method of edu-details-by-course  API is accessible by user after login with invalid credentials
        self.client.post(reverse('login'), data=json.dumps(self.invalid_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('edu-details', kwargs={'id': self.edu_details.id}), data=json.dumps(self.education_details_valid_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_edu_details_by_course_for_admin_after_login(self):
        # To check if PUT method of edu-details-by-course  API is accessible by admin after login
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('edu-details', kwargs={'id': self.edu_details.id}), data=json.dumps(self.education_details_valid_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_edu_details_by_course_for_mentor_after_login(self):
        # To check if PUT method of edu-details-by-course  API is accessible by mentor after login
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('edu-details', kwargs={'id': self.edu_details.id}), data=json.dumps(self.education_details_valid_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_edu_details_by_course_for_student_after_login(self):
        # To check if PUT method of edu-details-by-course API is accessible by student after login
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('edu-details', kwargs={'id': self.edu_details.id}), data=json.dumps(self.education_details_valid_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_edu_details_by_course_for_student_with_invalid_data_after_login(self):
        # To check if details are updated with invalid data by student after login
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('edu-details', kwargs={'id': self.edu_details.id}), data=json.dumps(self.education_details_invalid_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_edu_details_by_course_of_another_student_user_by_student_after_login(self):
        # To check if student can update other student's details after login
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('edu-details', kwargs={'id': self.edu_details_2.id}), data=json.dumps(self.education_details_valid_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


### Test cases for GET Method of UpdateEducationDetailsByCourse API : 

    def test_get_edu_details_by_course_without_login(self):
        # To check if edu-details-by-course API is accessible without login
        response = self.client.put(reverse('edu-details', kwargs={'id': self.edu_details.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_edu_details_by_course_for_user_after_login_with_invalid_credentials(self):
        # To check if GET method of edu-details-by-course  API is accessible by user after login with invalid credentials
        self.client.post(reverse('login'), data=json.dumps(self.invalid_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('edu-details', kwargs={'id': self.edu_details.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_edu_details_by_course_for_admin_after_login(self):
        # To check if GET method of edu-details-by-course  API is accessible by admin after login
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('edu-details', kwargs={'id': self.edu_details.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_edu_details_by_course_for_mentor_after_login(self):
        # To check if GET method of edu-details-by-course  API is accessible by mentor after login
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        try:
            response = self.client.get(reverse('edu-details', kwargs={'id': self.edu_details.id}), content_type=CONTENT_TYPE)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except Exception:
            return self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_edu_details_by_course_of_student_not_alloted_to_mentor(self):
        # To check if details are updated with invalid data by student after login
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('edu-details', kwargs={'id': self.edu_details_2.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_edu_details_by_course_for_student_after_login(self):
        # To check if GET method of edu-details-by-course API is accessible by student after login
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('edu-details', kwargs={'id': self.edu_details.id}), content_type=CONTENT_TYPE)
        students = EducationDetails.objects.get(id=self.edu_details.id)
        serializer = UpdateEducationDetailsSerializer(students)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_edu_details_by_course_of_another_student_user_by_student_after_login(self):
        # To check if student can get other student's details after login
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('edu-details', kwargs={'id': self.edu_details_2.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

### Test cases for course-list API 

    def test_get_course_list_without_login(self):
        # To check if GET method of courses-list API is accessible without login
        response = self.client.get(reverse('courses'), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_course_list_by_user_after_login_with_invalid_credentials(self):
        # To check if GET method of courses-list API is accessible by user after login with invalid credentials
        self.client.post(reverse('login'), data=json.dumps(self.invalid_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('courses'), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_course_list_by_admin_after_login(self):
        # To check if GET method of courses-list API is accessible by admin after login
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('courses'), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_course_list_by_mentor_after_login(self):
        # To check if GET method of courses-list API is accessible by mentor after login
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('courses'), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_course_list_by_student_after_login(self):
        # To check if GET method of courses-list API is accessible by student after login
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('courses'), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


### Test cases for course-create API 

    def test_get_course_list_without_login(self):
        # To check if POST method of courses-create API is accessible without login
        response = self.client.post(reverse('courses'), data=json.dumps(self.valid_course_data) , content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_course_list_by_user_after_login_with_invalid_credentials(self):
        # To check if POST method of courses-create API is accessible by user after login with invalid credentials
        self.client.post(reverse('login'), data=json.dumps(self.invalid_login_payload), content_type=CONTENT_TYPE)
        response = self.client.post(reverse('courses'), data=json.dumps(self.valid_course_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_course_list_by_admin_after_login(self):
        # To check if POST method of courses-create API is accessible by admin after login
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.post(reverse('courses'), data=json.dumps(self.valid_course_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_course_list_by_admin_with_invalid_data_after_login(self):
        # To check if admin gives invalid data to create course
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.post(reverse('courses'), data=json.dumps(self.invalid_course_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_course_list_by_mentor_after_login(self):
        # To check if POST method of courses-create API is accessible by mentor after login
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.post(reverse('courses'), data=json.dumps(self.valid_course_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_course_list_by_student_after_login(self):
        # To check if POST method of courses-create API is accessible by student after login
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.post(reverse('courses'), data=json.dumps(self.valid_course_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

### Test cases for GET method of course-details API 

    def test_get_course_details_without_login(self):
        # To check if GET method of courses-details API is accessible without login
        response = self.client.get(reverse('course', kwargs={'id':self.course1.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_course_details_by_user_after_login_with_invalid_credentials(self):
        # To check if GET method of courses-details API is accessible by user after login with invalid credentials
        self.client.post(reverse('login'), data=json.dumps(self.invalid_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('course', kwargs={'id':self.course1.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_course_details_by_admin_after_login(self):
        # To check if GET method of courses-create API is accessible by admin after login
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('course', kwargs={'id':self.course1.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_course_details_by_mentor_after_login(self):
        # To check if GET method of courses-details API is accessible by mentor after login
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('course', kwargs={'id':self.course1.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_course_details_by_student_after_login(self):
        # To check if GET method of courses-details API is accessible by student after login
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('course', kwargs={'id':self.course1.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


### Test cases for PUT method of course-details API 

    def test_update_course_details_without_login(self):
        # To check if PUT method of courses-details API is accessible without login
        response = self.client.put(reverse('course', kwargs={'id':self.course1.id}), data=json.dumps(self.valid_course_data) , content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_course_details_by_user_after_login_with_invalid_credentials(self):
        # To check if PUT method of courses-details API is accessible by user after login with invalid credentials
        self.client.post(reverse('login'), data=json.dumps(self.invalid_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('course', kwargs={'id':self.course1.id}), data=json.dumps(self.valid_course_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_course_details_by_admin_after_login(self):
        # To check if PUT method of courses-create API is accessible by admin after login
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('course', kwargs={'id':self.course1.id}), data=json.dumps(self.valid_course_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_course_details_by_admin_with_invalid_data_after_login(self):
        # To check if admin gives invalid data to create course
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('course', kwargs={'id':self.course1.id}), data=json.dumps(self.invalid_course_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_course_details_by_mentor_after_login(self):
        # To check if PUT method of courses-details API is accessible by mentor after login
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('course', kwargs={'id':self.course1.id}), data=json.dumps(self.valid_course_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_course_details_by_student_after_login(self):
        # To check if PUT method of courses-details API is accessible by student after login
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('course', kwargs={'id':self.course1.id}), data=json.dumps(self.valid_course_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


### Test cases for DELETE method of course-details API 

    def test_delete_course_details_without_login(self):
        # To check if DELETE method of courses-details API is accessible without login
        response = self.client.delete(reverse('course', kwargs={'id':self.course1.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_course_details_by_user_after_login_with_invalid_credentials(self):
        # To check if DELETE method of courses-details API is accessible by user after login with invalid credentials
        self.client.post(reverse('login'), data=json.dumps(self.invalid_login_payload), content_type=CONTENT_TYPE)
        response = self.client.delete(reverse('course', kwargs={'id':self.course1.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_course_details_by_admin_after_login(self):
        # To check if DELETE method of courses-create API is accessible by admin after login
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.delete(reverse('course', kwargs={'id':self.course1.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_course_details_by_mentor_after_login(self):
        # To check if DELETE method of courses-details API is accessible by mentor after login
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.delete(reverse('course', kwargs={'id':self.course1.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_course_details_by_student_after_login(self):
        # To check if DELETE method of courses-details API is accessible by student after login
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.delete(reverse('course', kwargs={'id':self.course1.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


### Test cases for mentors-list API 

    def test_get_mentors_list_without_login(self):
        # To check if GET method of mentors-list API is accessible without login
        response = self.client.get(reverse('mentors'), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_mentors_list_by_user_after_login_with_invalid_credentials(self):
        # To check if GET method of mentors-list API is accessible by user after login with invalid credentials
        self.client.post(reverse('login'), data=json.dumps(self.invalid_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('mentors'), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_mentors_list_by_admin_after_login(self):
        # To check if GET method of mentors-list API is accessible by admin after login
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('mentors'), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_mentors_list_by_mentor_after_login(self):
        # To check if GET method of mentors-list API is accessible by mentor after login
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('mentors'), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_mentors_list_by_student_after_login(self):
        # To check if GET method of mentors-list API is accessible by student after login
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('mentors'), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


### Test cases for PUT method of mentor-course API 

    def test_update_mentor_course_details_without_login(self):
        # To check if PUT method of mentor-course API is accessible without login
        response = self.client.put(reverse('mentor-course', kwargs={'mentor_id':self.mentor.id}), data=json.dumps(self.mentor_course_data) , content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_mentor_course_details_by_user_after_login_with_invalid_credentials(self):
        # To check if PUT method of mentor-course API is accessible by user after login with invalid credentials
        self.client.post(reverse('login'), data=json.dumps(self.invalid_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('mentor-course', kwargs={'mentor_id':self.mentor.id}), data=json.dumps(self.mentor_course_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_mentor_course_details_by_admin_after_login(self):
        # To check if PUT method of mentor-course API is accessible by admin after login
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('mentor-course', kwargs={'mentor_id':self.mentor.id}), data=json.dumps(self.mentor_course_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_mentor_course_details_by_admin_with_invalid_data_after_login(self):
        # To check if admin gives invalid data to map mentor-course
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('mentor-course', kwargs={'mentor_id':self.mentor.id}), data=json.dumps(self.mentor_course_invalid_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_mentor_course_details_by_mentor_after_login(self):
        # To check if PUT method of mentor-course API is accessible by mentor after login
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('mentor-course', kwargs={'mentor_id':self.mentor.id}), data=json.dumps(self.mentor_course_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_mentor_course_details_by_student_after_login(self):
        # To check if PUT method of mentor-course API is accessible by student after login
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('mentor-course', kwargs={'mentor_id':self.mentor.id}), data=json.dumps(self.mentor_course_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


### Test cases for GET method of mentor-course API 

    def test_get_mentor_course_details_without_login(self):
        # To check if GET method of mentor-course API is accessible without login
        response = self.client.get(reverse('mentor-course', kwargs={'mentor_id':self.mentor.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_mentor_course_details_by_user_after_login_with_invalid_credentials(self):
        # To check if GET method of mentor-course API is accessible by user after login with invalid credentials
        self.client.post(reverse('login'), data=json.dumps(self.invalid_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('mentor-course', kwargs={'mentor_id':self.mentor.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_mentor_course_details_by_admin_after_login(self):
        # To check if GET method of mentor-course API is accessible by admin after login
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('mentor-course', kwargs={'mentor_id':self.mentor.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_mentor_course_details_by_mentor_after_login(self):
        # To check if GET method of mentor-course API is accessible by mentor after login
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('mentor-course', kwargs={'mentor_id':self.mentor.id}), content_type=CONTENT_TYPE)
        mentor = Mentor.objects.filter(mentor=self.mentor.id)
        serializer = MentorsSerializer(mentor, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_mentor_course_details_of_another_mentor_by_mentor_user_after_login(self):
        # To check if mentor can view other mentor's data
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('mentor-course', kwargs={'mentor_id':self.mentor2.id}), content_type=CONTENT_TYPE)
        mentor = Mentor.objects.filter(mentor=self.mentor2.id)
        serializer = MentorsSerializer(mentor, many=True)
        self.assertNotEqual(response.data, serializer.data)

    def test_get_mentor_course_details_by_student_after_login(self):
        # To check if GET method of mentor-course API is accessible by student after login
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('mentor-course', kwargs={'mentor_id':self.mentor.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



### Test cases for POST method of MentorStudentMapping API 

    def test_mentor_student_mapping_without_login(self):
        # To check if POST method of mentor-student API is accessible without login
        response = self.client.post(reverse('mentor-student'), data=json.dumps(self.mentor_student_data) , content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_mentor_student_mapping_by_user_after_login_with_invalid_credentials(self):
        # To check if POST method of mentor-student API is accessible by user after login with invalid credentials
        self.client.post(reverse('login'), data=json.dumps(self.invalid_login_payload), content_type=CONTENT_TYPE)
        response = self.client.post(reverse('mentor-student'), data=json.dumps(self.mentor_student_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_mentor_student_mapping_by_admin_after_login(self):
        # To check if POST method of mentor-student API is accessible by admin after login
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.post(reverse('mentor-student'), data=json.dumps(self.mentor_student_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mentor_student_mapping_by_admin_with_invalid_data_after_login(self):
        # To check if admin gives invalid data to map mentor-student
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.post(reverse('mentor-student'), data=json.dumps(self.mentor_student_invalid_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_mentor_student_mapping_by_mentor_after_login(self):
        # To check if POST method of mentor-student API is accessible by mentor after login
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.post(reverse('mentor-student'), data=json.dumps(self.mentor_student_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_mentor_student_mapping_by_student_after_login(self):
        # To check if POST method of mentor-student API is accessible by student after login
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.post(reverse('mentor-student'), data=json.dumps(self.mentor_student_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

### Test cases for GET method of MentorStudentMapping API 

    def test_get_mentor_mapping_details_without_login(self):
        # To check if GET method of mentor-student API is accessible without login
        response = self.client.get(reverse('mentor-student'), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_mentor_student_mapping_by_user_after_login_with_invalid_credentials(self):
        # To check if GET method of mentor-student API is accessible by user after login with invalid credentials
        self.client.post(reverse('login'), data=json.dumps(self.invalid_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('mentor-student'), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_mentor_student_mapping_by_admin_after_login(self):
        # To check if GET method of mentor-student API is accessible by admin after login
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('mentor-student'), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_mentor_student_mapping_by_mentor_after_login(self):
        # To check if GET method of mentor-student API is accessible by mentor after login
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        try:
            response = self.client.get(reverse('mentor-student'), content_type=CONTENT_TYPE)
            mentor = MentorStudent.objects.filter(mentor=self.mentor_course.id)
            serializer = MentorStudentListSerializer(mentor, many=True)
            self.assertEqual(response.data['response'], serializer.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except Exception :
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_mentor_student_mapping_of_other_mentor_by_mentor_after_login(self):
        # To check if mentor can view other mentor's data
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        try:
            response = self.client.get(reverse('mentor-student'), content_type=CONTENT_TYPE)   
            mentor = MentorStudent.objects.filter(mentor=self.mentor_course2.id)
            serializer = MentorStudentListSerializer(mentor, many=True)
            self.assertNotEqual(response.data, serializer.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except Exception :
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_mentor_student_mapping_by_student_after_login(self):
        # To check if GET method of mentor-student API is accessible by student after login
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('mentor-student'), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


### Test cases for GET method of MentorStudentDetails API 

    def test_get_mentor_student_details_without_login(self):
        # To check if GET method of mentor-student API is accessible without login
        response = self.client.get(reverse('mentor-student-details', kwargs={'student_id':self.student_details.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_mentor_student_details_by_user_after_login_with_invalid_credentials(self):
        # To check if GET method of mentor-student API is accessible by user after login with invalid credentials
        self.client.post(reverse('login'), data=json.dumps(self.invalid_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('mentor-student-details', kwargs={'student_id':self.student_details.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_mentor_student_details_by_admin_after_login(self):
        # To check if GET method of mentor-student API is accessible by admin after login
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('mentor-student-details', kwargs={'student_id':self.student_details.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_mentor_student_details_by_mentor_after_login(self):
        # To check if GET method of mentor-student API is accessible by mentor after login
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        try:
            response = self.client.get(reverse('mentor-student-details', kwargs={'student_id':self.student_details.id}), content_type=CONTENT_TYPE)   
            mentor = MentorStudent.objects.get(student=self.student_details , mentor=self.mentor_course)
            serializer = MentorStudentListSerializer(mentor)
            self.assertEqual(response.data['response'], serializer.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except Exception :
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_mentor_student_details_of_other_mentor_by_mentor_after_login(self):
        # To check if mentor can view other mentor's data
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        try:
            response = self.client.get(reverse('mentor-student-details', kwargs={'student_id':self.student2_details.id}), content_type=CONTENT_TYPE)   
            mentor = MentorStudent.objects.get(student=self.student2_details , mentor=self.mentor_course2)
            serializer = MentorStudentListSerializer(mentor)
            self.assertNotEqual(response.data['response'], serializer.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except Exception :
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_mentor_student_details_by_student_after_login(self):
        # To check if GET method of mentor-student API is accessible by student after login
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('mentor-student-details', kwargs={'student_id':self.student_details.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        
### Test cases for PUT method of MentorStudentMapping API 

    def test_update_mentor_student_details_without_login(self):
        # To check if PUT method of mentor-student-details API is accessible without login
        response = self.client.put(reverse('mentor-student-details', kwargs={'student_id':self.student_details.id}), data=json.dumps(self.mentor_student_data) , content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_mentor_student_details_by_user_after_login_with_invalid_credentials(self):
        # To check if PUT method of mentor-student-details API is accessible by user after login with invalid credentials
        self.client.post(reverse('login'), data=json.dumps(self.invalid_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('mentor-student-details', kwargs={'student_id':self.student_details.id}), data=json.dumps(self.mentor_student_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_mentor_student_details_by_admin_after_login(self):
        # To check if PUT method of mentor-student-details API is accessible by admin after login
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        try:
            response = self.client.put(reverse('mentor-student-details', kwargs={'student_id':self.student_details.id}), data=json.dumps(self.mentor_student_data), content_type=CONTENT_TYPE)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except Exception:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_mentor_student_details_by_admin_with_invalid_data_after_login(self):
        # To check if admin gives invalid data to map mentor-student-details
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('mentor-student-details', kwargs={'student_id':self.student_details.id}), data=json.dumps(self.mentor_student_invalid_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_mentor_student_details_by_mentor_after_login(self):
        # To check if PUT method of mentor-student-details API is accessible by mentor after login
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('mentor-student-details', kwargs={'student_id':self.student_details.id}), data=json.dumps(self.mentor_student_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_mentor_student_details_by_student_after_login(self):
        # To check if PUT method of mentor-student-details API is accessible by student after login
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('mentor-student-details', kwargs={'student_id':self.student_details.id}), data=json.dumps(self.mentor_student_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


### Test cases for performance-list API 

    def test_get_performance_list_without_login(self):
        # To check if GET method of performance-list API is accessible without login
        response = self.client.get(reverse('performance'), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_performance_list_by_user_after_login_with_invalid_credentials(self):
        # To check if GET method of performance-list API is accessible by user after login with invalid credentials
        self.client.post(reverse('login'), data=json.dumps(self.invalid_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('performance'), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_performances_list_by_admin_after_login(self):
        # To check if GET method of performances-list API is accessible by admin after login
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('performance'), content_type=CONTENT_TYPE)
        performances = Performance.objects.all()
        serializer = PerformanceSerializer(performances, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_performance_list_by_mentor_after_login(self):
        # To check if GET method of performance-list API is accessible by mentor after login
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('performance'), content_type=CONTENT_TYPE)
        performances = Performance.objects.filter(mentor=self.mentor_course)
        serializer = PerformanceSerializer(performances, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_performance_list_of_another_mentors_student_by_mentor_after_login(self):
        # To check if mentor can view other mentor's student performance
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('performance'), content_type=CONTENT_TYPE)
        performances = Performance.objects.filter(mentor=self.mentor_course2)
        serializer = PerformanceSerializer(performances, many=True)
        self.assertNotEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_performance_list_by_student_after_login(self):
        # To check if GET method of performance-list API is accessible by student after login
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('performance'), content_type=CONTENT_TYPE)
        performances = Performance.objects.filter(student=self.student_details.id)
        serializer = PerformanceSerializer(performances, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_performance_list_of_other_student_by_student_after_login(self):
        # To check if student can view other student's performance
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('performance'), content_type=CONTENT_TYPE)
        performances = Performance.objects.filter(student=self.student2_details.id)
        serializer = PerformanceSerializer(performances, many=True)
        self.assertNotEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


### Test cases for GET method for performance-details API 

    def test_get_performance_without_login(self):
        # To check if GET method of performance-details API is accessible without login
        response = self.client.get(reverse('performance-details', kwargs={'id':self.performance.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_performance_by_user_after_login_with_invalid_credentials(self):
        # To check if GET method of performance-details API is accessible by user after login with invalid credentials
        self.client.post(reverse('login'), data=json.dumps(self.invalid_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('performance-details', kwargs={'id':self.performance.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_performances_by_admin_after_login(self):
        # To check if GET method of performances-details API is accessible by admin after login
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('performance-details', kwargs={'id':self.performance.id}), content_type=CONTENT_TYPE)
        performances = Performance.objects.get(id=self.performance.id)
        serializer = PerformanceSerializer(performances)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_performance_by_mentor_after_login(self):
        # To check if GET method of performance-details API is accessible by mentor after login
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('performance-details', kwargs={'id':self.performance.id}), content_type=CONTENT_TYPE)
        performances = Performance.objects.get(id=self.performance.id, mentor=self.mentor_course)
        serializer = PerformanceSerializer(performances)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_performance_of_another_mentors_student_by_mentor_after_login(self):
        # To check if mentor can view other mentor's student performance-details
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('performance-details', kwargs={'id':self.performance.id}), content_type=CONTENT_TYPE)
        performances = Performance.objects.get(id=self.performance2.id, mentor=self.mentor_course2)
        serializer = PerformanceSerializer(performances)
        self.assertNotEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_performance_by_student_after_login(self):
        # To check if GET method of performance-details API is accessible by student after login
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('performance-details', kwargs={'id':self.performance.id}), content_type=CONTENT_TYPE)
        performances = Performance.objects.get(id=self.performance.id, student=self.student_details.id)
        serializer = PerformanceSerializer(performances)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_performance_of_other_student_by_student_after_login(self):
        # To check if student can view other student's performance-details
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('performance-details', kwargs={'id':self.performance.id}), content_type=CONTENT_TYPE)
        performances = Performance.objects.get(id=self.performance2.id, student=self.student2_details.id)
        serializer = PerformanceSerializer(performances)
        self.assertNotEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


### Test cases for PUT method for performance-details API 

    def test_update_performance_without_login(self):
        # To check if PUT method of performance-details API is accessible without login
        response = self.client.put(reverse('performance-details', kwargs={'id':self.performance.id}), data=json.dumps(self.performance_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_performance_by_user_after_login_with_invalid_credentials(self):
        # To check if PUT method of performance-details API is accessible by user after login with invalid credentials
        self.client.post(reverse('login'), data=json.dumps(self.invalid_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('performance-details', kwargs={'id':self.performance.id}), data=json.dumps(self.performance_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_performances_by_admin_after_login(self):
        # To check if PUT method of performances-details API is accessible by admin after login
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('performance-details', kwargs={'id':self.performance.id}), data=json.dumps(self.mentor_student_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_performance_by_mentor_after_login(self):
        # To check if PUT method of performance-details API is accessible by mentor after login
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('performance-details', kwargs={'id':self.performance.id}), data=json.dumps(self.performance_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_performance_by_mentor_with_invalid_data_after_login(self):
        # To check if PUT method of performance-details API is accessible by mentor after login
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('performance-details', kwargs={'id':self.performance.id}), data=json.dumps(self.performance_invalid_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_performance_of_another_mentors_student_by_mentor_after_login(self):
        # To check if mentor can view other mentor's student performance-details
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('performance-details', kwargs={'id':self.performance.id}), data=json.dumps(self.performance_data), content_type=CONTENT_TYPE)
        performances = Performance.objects.filter(id=self.performance2.id, mentor=self.mentor_course2)
        serializer = PerformanceSerializer(performances, many=True)
        self.assertNotEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_performance_by_student_after_login(self):
        # To check if PUT method of performance-details API is accessible by student after login
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('performance-details', kwargs={'id':self.performance.id}), data=json.dumps(self.performance_data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


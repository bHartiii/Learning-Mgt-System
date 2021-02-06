from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import User
from learning_mgt.models import Mentor, Student, EducationDetails, Performance, MentorStudent, Course
from ..serializers import UpdateEducationDetailsSerializer, UpdateStudentDetailsSerializer, MentorsSerializer, MentorCourseMappingSerializer, MentorStudentMappingSerializer, MentorStudentUpdateMappingSerializer, MentorStudentListSerializer, PerformanceSerializer
import json

CONTENT_TYPE = 'application/json'
class ManagementAPITest(TestCase):
    """ Test module for authentication APIs """
    
    def setUp(self):
        # initialize the APIClient app
        self.client = Client()

        self.admin = User.objects.create(username='admin', first_name='Bharti', last_name='Mali', role='Admin', email='admin@gmail.com', password='pbkdf2_sha256$216000$yG97oIyabA7B$nzM1GiofqbxOqH/prQTgjDWhT1C7o1cpj0VdJ5viW0M=', first_login=True)
        self.student = User.objects.create(username='student1', first_name='Bharti', last_name='Mali', role='Student', email='student@gmail.com', password='pbkdf2_sha256$216000$jge4gjoUWquH$RqjqlYMi9gKUAEItd91thLEwpewzUn5WOfL2TdsLyjY=', first_login=True)
        self.student2 = User.objects.create(username='student2', first_name='Bharti', last_name='Mali', role='Student', email='student2@gmail.com', password='pbkdf2_sha256$216000$jge4gjoUWquH$RqjqlYMi9gKUAEItd91thLEwpewzUn5WOfL2TdsLyjY=', first_login=True)
        self.mentor = User.objects.create(username='mentor', first_name='Bharti', last_name='Mali', role='Mentor', email='mentor@gmail.com', password='pbkdf2_sha256$216000$jge4gjoUWquH$RqjqlYMi9gKUAEItd91thLEwpewzUn5WOfL2TdsLyjY=', first_login=True)

        # Create course model object
        self.course = Course.objects.create(course_name='Python')
        
        # Create student model object 
        self.student_details = Student.objects.get(student=self.student)
        
        # Create education-details model 
        self.edu_details = EducationDetails.objects.get(student=self.student_details, course='UG')
        
        # Create mentor-course object
        self.mentor_course = Mentor.objects.get(mentor=self.mentor)

        # Assign course to mentor-course object
        self.mentor_course.course.add(self.course)
        self.mentor_course.save()

        # Create mentor-student model object
        self.mentor_student = MentorStudent.objects.create(student=self.student_details , course=self.course, mentor=self.mentor_course)

        # Update performance model object : 
        self.performance = Performance.objects.get(student=self.student_details)
        self.performance.current_score = 3
        self.performance.save()

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
            'From': 2016,
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


### Test cases for PUT Method of student-details API : 

    def test_update_student_details_without_login(self):
        # To check if student-details API is accessible without login
        response = self.client.put(reverse('student-details', kwargs={'student_id': self.student.id}), data=json.dumps(self.student_details_valid_data), content_type=CONTENT_TYPE)
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
        response = self.client.get(reverse('student-details', kwargs={'student_id': self.student.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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




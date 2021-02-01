from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import User
from ..serializers import UserCreationSerializer
import json

CONTENT_TYPE = 'application/json'
class AuthenticationAPITest(TestCase):
    """ Test module for authentication APIs """
    
    def setUp(self):
        # initialize the APIClient app
        self.client = Client()

        self.admin = User.objects.create(username='admin', first_name='Bharti', last_name='Mali', role='Admin', email='admin@gmail.com', password='pbkdf2_sha256$216000$yG97oIyabA7B$nzM1GiofqbxOqH/prQTgjDWhT1C7o1cpj0VdJ5viW0M=', is_superuser=True)
        self.student = User.objects.create(username='student', first_name='Bharti', last_name='Mali', role='Student', email='student@gmail.com', password='pbkdf2_sha256$216000$jge4gjoUWquH$RqjqlYMi9gKUAEItd91thLEwpewzUn5WOfL2TdsLyjY=')
        self.mentor = User.objects.create(username='mentor', first_name='Bharti', last_name='Mali', role='Mentor', email='mentor@gmail.com', password='pbkdf2_sha256$216000$jge4gjoUWquH$RqjqlYMi9gKUAEItd91thLEwpewzUn5WOfL2TdsLyjY=')

        self.valid_user_payload = {
            'username' : 'test',
            'first_name' : 'Bharti',
            'last_name' : 'Mali',
            'email' : 'malibharti5@gmail.com',
            'mobile_number':'1234567890',
            'password' : 'bharti',
            'role' : 'Admin'
        }
        
        self.invalid_user_payload = {
            'username' : '',
            'first_name' : 'Bharti',
            'last_name' : '',
            'email' : '',
            'password' : 'bharti',
            'mobile_number':'1234567890',
            'role' : 'Admin'
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
            'username' : 'student',
            'password' : 'bharti'
        }
        self.invalid_login_payload = {
            'username' : 'bharti',
            'password' : 'bharti'
        }

### Test cases for create-user API : 

    def test_create_user_with_valid_payload_without_login(self):
        response = self.client.post(reverse('create-user'), data=json.dumps(self.valid_user_payload), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_with_valid_payload_after_login_by_invalid_credentials(self):
        self.client.post(reverse('login'), data=json.dumps(self.invalid_login_payload), content_type=CONTENT_TYPE)
        response = self.client.post(reverse('create-user'), data=json.dumps(self.valid_user_payload), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_with_valid_payload_after_login_by_admin_credentials(self):
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.post(reverse('create-user'), data=json.dumps(self.valid_user_payload), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_with_invalid_payload(self):
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.post(reverse('create-user'), data=json.dumps(self.invalid_user_payload), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_valid_payload_after_login_by_mentor_credentials(self):
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.post(reverse('create-user'), data=json.dumps(self.valid_user_payload), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_user_with_valid_payload_after_login_by_studnet_credentials(self):
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.post(reverse('create-user'), data=json.dumps(self.valid_user_payload), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


### Test cases to retrieve user-details API : 

    def test_retrieve_user_details_with_valid_payload_without_login(self):
        response = self.client.get(reverse('user', kwargs={'id': self.admin.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user_details_with_valid_payload_after_login_by_invalid_credentials(self):
        self.client.post(reverse('login'), data=json.dumps(self.invalid_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('user', kwargs={'id': self.admin.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user_details_with_valid_payload_after_login_by_admin_credentials(self):
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('user', kwargs={'id': self.admin.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user_details_with_valid_payload_after_login_by_mentor_credentials(self):
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('user', kwargs={'id': self.admin.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user_details_with_valid_payload_after_login_by_mentor_credentials(self):
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('user', kwargs={'id': self.admin.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

### Test cases to update user-details API : 

    def test_user_details_with_valid_payload_without_login(self):
        response = self.client.put(reverse('user', kwargs={'id': self.admin.id}), data=json.dumps(self.valid_user_payload), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_details_with_valid_payload_after_login_by_invalid_credentials(self):
        self.client.post(reverse('login'), data=json.dumps(self.invalid_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('user', kwargs={'id': self.admin.id}), data=json.dumps(self.valid_user_payload), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_details_with_valid_payload_after_login_by_admin_credentials(self):
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('user', kwargs={'id': self.admin.id}), data=json.dumps(self.valid_user_payload), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_details_with_invalid_payload_after_login_by_admin_credentials(self):
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('user', kwargs={'id': self.admin.id}), data=json.dumps(self.invalid_user_payload), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_details_with_valid_payload_after_login_by_mentor_credentials(self):
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('user', kwargs={'id': self.admin.id}), data=json.dumps(self.valid_user_payload), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_details_with_valid_payload_after_login_by_mentor_credentials(self):
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('user', kwargs={'id': self.admin.id}), data=json.dumps(self.valid_user_payload), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

### Test cases to delete user-details API : 

    def test_delete_user_with_valid_payload_without_login(self):
        response = self.client.delete(reverse('user', kwargs={'id': self.admin.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_with_valid_payload_after_login_by_invalid_credentials(self):
        self.client.post(reverse('login'), data=json.dumps(self.invalid_login_payload), content_type=CONTENT_TYPE)
        response = self.client.delete(reverse('user', kwargs={'id': self.admin.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_with_valid_payload_after_login_by_admin_credentials(self):
        self.client.post(reverse('login'), data=json.dumps(self.admin_login_payload), content_type=CONTENT_TYPE)
        response = self.client.delete(reverse('user', kwargs={'id': self.admin.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_with_valid_payload_after_login_by_mentor_credentials(self):
        self.client.post(reverse('login'), data=json.dumps(self.mentor_login_payload), content_type=CONTENT_TYPE)
        response = self.client.delete(reverse('user', kwargs={'id': self.admin.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user_details_with_valid_payload_after_login_by_mentor_credentials(self):
        self.client.post(reverse('login'), data=json.dumps(self.student_login_payload), content_type=CONTENT_TYPE)
        response = self.client.delete(reverse('user', kwargs={'id': self.admin.id}), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
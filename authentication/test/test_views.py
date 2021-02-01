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
        self.admin = User.objects.create(username='admin', first_name='Bharti', last_name='Mali', role='Admin', email='admin@gmail.com', password='pbkdf2_sha256$216000$jge4gjoUWquH$RqjqlYMi9gKUAEItd91thLEwpewzUn5WOfL2TdsLyjY=')
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

    def test_create_user_with_valid_payload(self):
        response = self.client.post(reverse('create-user'),data=json.dumps(self.valid_user_payload) ,content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_with_invalid_payload(self):
        response = self.client.post(reverse('create-user'),data=json.dumps(self.invalid_user_payload) ,content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
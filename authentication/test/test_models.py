from django.test import TestCase
from authentication.models import User
from learning_mgt.models import Student, EducationDetails, Mentor

class UserTest(TestCase):

    def setUp(self):
        self.student = User.objects.create(username='student', first_name='Bharti', last_name='Mali', email='student@gmail.com', password='bharti', role='Student')
        self.admin = User.objects.create(username='admin', first_name='Bharti', last_name='Mali', email='admin@gmail.com', password='bharti', role='Admin')
        self.mentor = User.objects.create(username='mentor', first_name='Bharti', last_name='Mali', email='mentor@gmail.com', password='bharti', role='Mentor')


    def test_create_user_student(self):
        user = User.objects.get(username='student')
        self.assertEqual(user.get_full_name(), 'Bharti Mali')
        self.assertEqual(user.role, 'Student')
        

    def test_create_user_admin(self):
        user = User.objects.get(username='admin')
        self.assertEqual(user.get_full_name(), 'Bharti Mali')
        self.assertEqual(user.role, 'Admin')


    def test_create_user_mentor(self):
        user = User.objects.get(username='mentor')
        self.assertEqual(user.get_full_name(), 'Bharti Mali')
        self.assertEqual(user.role, 'Mentor')

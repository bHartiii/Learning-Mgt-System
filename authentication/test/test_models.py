from django.test import TestCase
from authentication.models import User
from learning_mgt.models import Student, EducationDetails, Mentor
from learning_mgt.serializers import MentorsSerializer

class UserTest(TestCase):

    def setUp(self):
        self.student = User.objects.create(username='student', first_name='Bharti', last_name='Mali', email='student@gmail.com', password='bharti', role='Student')
        self.admin = User.objects.create(username='admin', first_name='Bharti', last_name='Mali', email='admin@gmail.com', password='bharti', role='Admin')
        self.mentor = User.objects.create(username='mentor', first_name='Bharti', last_name='Mali', email='mentor@gmail.com', password='bharti', role='Mentor')


    def test_create_user(self):
        user = User.objects.get(username='student')
        self.assertEqual(user.get_full_name(), 'Bharti Mali')

    def test_create_student_details(self):
        student_details = Student.objects.get(student=self.student)
        self.assertEqual(student_details.contact, "")

    def test_create_mentor(self):
        mentor = Mentor.objects.get(mentor=self.mentor)
        serializer = MentorsSerializer(mentor.course.all(), many=True)
        self.assertEqual(serializer.data, [])

    def test_create_education_details(self):
        student_details = Student.objects.get(student=self.student)
        education_details_10th = EducationDetails.objects.get(student=student_details, course="10th")
        self.assertEqual(education_details_10th.institution, "")
        education_details_12th = EducationDetails.objects.get(student=student_details, course="12th")
        self.assertEqual(education_details_12th.institution, "")
        education_details_UG = EducationDetails.objects.get(student=student_details, course="UG")
        self.assertEqual(education_details_UG.institution, "")
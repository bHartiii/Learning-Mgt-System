from django.test import TestCase
from authentication.models import User
from learning_mgt.models import Course, Student, EducationDetails, Mentor, MentorStudent, Performance
from learning_mgt.serializers import MentorsSerializer, MentorStudentListSerializer

class ManagementModelsTest(TestCase):

    def setUp(self):
        self.course = Course.objects.create(course_name='Python')
        self.student = User.objects.create(username='student', first_name='Bharti', last_name='Mali', email='student@gmail.com', password='bharti', role='Student')
        self.admin = User.objects.create(username='admin', first_name='Bharti', last_name='Mali', email='admin@gmail.com', password='bharti', role='Admin')
        self.mentor = User.objects.create(username='mentor', first_name='Bharti', last_name='Mali', email='mentor@gmail.com', password='bharti', role='Mentor')
        self.student_details = Student.objects.get(student=self.student)
        self.mentor_course = Mentor.objects.get(mentor=self.mentor)
        self.mentor_course.course.set = self.course
        self.mentor_student = MentorStudent.objects.create(student=self.student_details , course=self.course, mentor=self.mentor_course)
        
### Test cases for course model :

    def test_create_course(self):
        course = Course.objects.get(id=self.course.id)
        self.assertEqual(course.course_name, "Python")

    def test_create_course_methods(self):
        course = Course.objects.get(id=self.course.id)
        self.assertEqual(course.__str__(), "Python")

    def test_course_details(self):
        course = Course.objects.get(id=self.course.id)
        self.assertEqual(course.created_by, None)

### Test cases for student model :

    def test_create_student_methods(self):
        self.assertEqual(self.student_details.get_full_name(), 'Bharti Mali')
        self.assertEqual(self.student_details.__str__(), "student@gmail.com")

    def test_create_student_details(self):
        self.assertEqual(self.student_details.contact, "")
        self.assertEqual(self.student_details.created_by, None)

### Test cases for mentor model :

    def test_create_mentor_details(self):
        mentor = Mentor.objects.get(mentor_id=self.mentor.id)
        self.assertEqual(mentor.__str__(), "mentor@gmail.com")

    def test_create_mentor(self):
        mentor = Mentor.objects.get(mentor=self.mentor)
        serializer = MentorsSerializer(mentor.course.all(), many=True)
        self.assertEqual(serializer.data, [])

### Test cases for education-details model :

    def test_create_education_details(self):
        student_details = Student.objects.get(student=self.student)
        education_details_10th = EducationDetails.objects.get(student=student_details, course="10th")
        self.assertEqual(education_details_10th.institution, "")
        education_details_12th = EducationDetails.objects.get(student=student_details, course="12th")
        self.assertEqual(education_details_12th.institution, "")
        education_details_UG = EducationDetails.objects.get(student=student_details, course="UG")
        self.assertEqual(education_details_UG.institution, "")

### Test cases for mentor-student model :

    def test_create_mentor_student(self):
        serializer = MentorStudentListSerializer(self.mentor_student)
        self.assertEqual(serializer.data['course'], 'Python')
        self.assertEqual(serializer.data['student'], 'student@gmail.com')
        self.assertEqual(serializer.data['mentor'], 'mentor@gmail.com')

### Test cases for performance :
    
    def test_create_performance(self):
        performance = Performance.objects.get(student=self.student_details)
        self.assertEqual(performance.current_score, None)
        self.assertEqual(performance.mentor, self.mentor_course)
        self.assertEqual(performance.course, self.course)







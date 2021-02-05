from django.test import TestCase
from authentication.models import User
from learning_mgt.models import Student, EducationDetails, Course, MentorStudent, Mentor, Performance
from learning_mgt.serializers import UpdateStudentDetailsSerializer, UpdateEducationDetailsSerializer, AddCourseSerializer, MentorCourseMappingSerializer, MentorsSerializer, MentorStudentMappingSerializer, MentorStudentUpdateMappingSerializer, MentorStudentListSerializer, PerformanceSerializer


class ManagementSerializersTest(TestCase):

    def setUp(self):

        # Create course model object
        self.course = Course.objects.create(course_name='Python')

        # Create user inctance with studennt, admin, mentor role
        self.student = User.objects.create(username='student', first_name='Bharti', last_name='Mali', email='student@gmail.com', password='bharti', role='Student')
        self.admin = User.objects.create(username='admin', first_name='Bharti', last_name='Mali', email='admin@gmail.com', password='bharti', role='Admin')
        self.mentor = User.objects.create(username='mentor', first_name='Bharti', last_name='Mali', email='mentor@gmail.com', password='bharti', role='Mentor')
        
        # Payload to update model objects
        self.student_details_data = {
            'image': None,
            'contact': '7742977480',
            'alternate_contact': '7772779990',
            'relation_with_alternate_contact': 'myself',
            'current_location': 'RJ',
            'Address':'Nathdwara',
            'git_link':'github.com/bHartiii',
            'yr_of_exp':0
        }
        
        self.education_details_data = {
            'institution': 'amity',
            'percentage': 81,
            'From': 2016,
            'Till': 2020,
        }
        
        # payloads to pass data in serializers
        self.UpdateStudentDetailsSerializer_data = {
            'image': None,
            'contact': '7742977480',
            'alternate_contact': '7772779990',
            'relation_with_alternate_contact': 'myself',
            'current_location': 'RJ',
            'Address':'Nathdwara',
            'git_link':'github.com/bHartiii',
            'yr_of_exp':0
        }
      
        self.UpdateEducationDetailsSerializer_data = {
            'institution': 'amity',
            'percentage': 81,
            'From': 2006,
            'Till': 2020,
        }

        ### Update student model object with dictionary data
        self.student_details = Student.objects.get(student=self.student)
        self.student_details.image = self.student_details_data['image']
        self.student_details.contact = self.student_details_data['contact']
        self.student_details.alternate_contact = self.student_details_data['alternate_contact']
        self.student_details.relation_with_alternate_contact = self.student_details_data['relation_with_alternate_contact']
        self.student_details.current_location = self.student_details_data['current_location']
        self.student_details.Address = self.student_details_data['Address']
        self.student_details.git_link = self.student_details_data['git_link']
        self.student_details.yr_of_exp = self.student_details_data['yr_of_exp']
        self.student_details.save()

        ### Update education-details model object with dictioanry data
        self.edu_details = EducationDetails.objects.get(student=self.student_details, course='UG')
        self.edu_details.institution = self.education_details_data['institution']
        self.edu_details.percentage = self.education_details_data['percentage']
        self.edu_details.From = self.education_details_data['From']
        self.edu_details.Till = self.education_details_data['Till']
        self.edu_details.save()

        ### Create mentor-course object
        self.mentor_course = Mentor.objects.get(mentor=self.mentor)

        ### Assign course to mentor-course object
        self.mentor_course.course.set = self.course

        ### Create mentor-student model object
        self.mentor_student = MentorStudent.objects.create(student=self.student_details , course=self.course, mentor=self.mentor_course)

        ### Create serializer with each model instance
        self.student_detail_serializer = UpdateStudentDetailsSerializer(instance=self.student_details)
        self.education_detail_serializer = UpdateEducationDetailsSerializer(instance=self.edu_details)


### Test cases for UpdateStudentDetails :

    def test_update_student_details_serializer_contains_expected_fields(self):
        """
            To check fields of UpdateStudentDetailsSerializer serializer 
        """
        data = self.student_detail_serializer.data
        self.assertCountEqual(data.keys(), ['id', 'student', 'image', 'contact', 'alternate_contact', 'relation_with_alternate_contact','current_location','Address','git_link','yr_of_exp'])


    def test_update_student_details_serializer_fields_content(self):
        """ 
            To check if the serialized data is same as payload given in model object for each field 
        """
        data = self.student_detail_serializer.data
        self.assertEqual(data['image'], self.student_details_data['image'])
        self.assertEqual(data['contact'], self.student_details_data['contact'])
        self.assertEqual(data['alternate_contact'], self.student_details_data['alternate_contact'])
        self.assertEqual(data['relation_with_alternate_contact'], self.student_details_data['relation_with_alternate_contact'])
        self.assertEqual(data['current_location'], self.student_details_data['current_location'])
        self.assertEqual(data['Address'], self.student_details_data['Address'])
        self.assertEqual(data['git_link'], self.student_details_data['git_link'])
        self.assertEqual(data['yr_of_exp'], self.student_details_data['yr_of_exp'])


    def test_update_student_details_serializer_empty_fields_content(self):
        """
            To check if serializer is giving validation error if any field is empty
        """
        self.UpdateStudentDetailsSerializer_data['image'] = ''
        self.UpdateStudentDetailsSerializer_data['contact'] = ''
        self.UpdateStudentDetailsSerializer_data['alternate_contact'] = ''
        self.UpdateStudentDetailsSerializer_data['relation_with_alternate_contact'] = ''
        self.UpdateStudentDetailsSerializer_data['current_location'] = ''
        self.UpdateStudentDetailsSerializer_data['Address'] = ''
        self.UpdateStudentDetailsSerializer_data['git_link'] = ''
        self.UpdateStudentDetailsSerializer_data['yr_of_exp'] = ''
        serializer = UpdateStudentDetailsSerializer(data=self.UpdateStudentDetailsSerializer_data)
        self.assertFalse(serializer.is_valid())        
        self.assertEqual(set(serializer.errors), set(['image', 'contact', 'alternate_contact', 'relation_with_alternate_contact','current_location','Address','git_link','yr_of_exp']))


    def test_update_student_details_serializer_contact_field__string_content(self):
        """
            To check if serializer is giving validation error if contact field contains string
        """
        self.UpdateStudentDetailsSerializer_data['contact'] = 'bharti'
        serializer = UpdateStudentDetailsSerializer(data=self.UpdateStudentDetailsSerializer_data)
        self.assertFalse(serializer.is_valid())        
        self.assertEqual(set(serializer.errors), set(['contact']))


    def test_update_student_details_serializer_contact_field_content_min_length(self):
        """
            To check if serializer is giving validation error if contact field contains less than 10 digits
        """
        self.UpdateStudentDetailsSerializer_data['contact'] = '1234'
        serializer = UpdateStudentDetailsSerializer(data=self.UpdateStudentDetailsSerializer_data)
        self.assertFalse(serializer.is_valid())        
        self.assertEqual(set(serializer.errors), set(['contact']))


    def test_update_student_details_serializer_contact_field_content_max_length(self):
        """
            To check if serializer is giving validation error if contact field contains is more than 10 digits
        """
        self.UpdateStudentDetailsSerializer_data['contact'] = '12345678900'
        serializer = UpdateStudentDetailsSerializer(data=self.UpdateStudentDetailsSerializer_data)
        self.assertFalse(serializer.is_valid())        
        self.assertEqual(set(serializer.errors), set(['contact']))


    def test_update_student_details_serializer_alternate_contact_field__string_content(self):
        """
            To check if serializer is giving validation error if alternate contact field contains string
        """
        self.UpdateStudentDetailsSerializer_data['alternate_contact'] = 'bharti'
        serializer = UpdateStudentDetailsSerializer(data=self.UpdateStudentDetailsSerializer_data)
        self.assertFalse(serializer.is_valid())        
        self.assertEqual(set(serializer.errors), set(['alternate_contact']))


    def test_update_student_details_serializer_alternate_contact_field_content_min_length(self):
        """
            To check if serializer is giving validation error if alternate contact field contains less than 10 digits
        """
        self.UpdateStudentDetailsSerializer_data['alternate_contact'] = '1234'
        serializer = UpdateStudentDetailsSerializer(data=self.UpdateStudentDetailsSerializer_data)
        self.assertFalse(serializer.is_valid())        
        self.assertEqual(set(serializer.errors), set(['alternate_contact']))


    def test_update_student_details_serializer_alternate_contact_field_content_max_length(self):
        """
            To check if serializer is giving validation error if alternate contact field contains more then 10 digits
        """
        self.UpdateStudentDetailsSerializer_data['alternate_contact'] = '12345678900'
        serializer = UpdateStudentDetailsSerializer(data=self.UpdateStudentDetailsSerializer_data)
        self.assertFalse(serializer.is_valid())        
        self.assertEqual(set(serializer.errors), set(['alternate_contact']))


    def test_update_student_details_serializer_alternate_contact_field_invalid_content(self):
        """
            To check if serializer is giving validation error if alternate contact field contains invalid data
        """
        self.UpdateStudentDetailsSerializer_data['alternate_contact'] = '1234567890'
        serializer = UpdateStudentDetailsSerializer(data=self.UpdateStudentDetailsSerializer_data)
        self.assertFalse(serializer.is_valid())        
        self.assertEqual(set(serializer.errors), set(['alternate_contact']))


    def test_update_student_details_serializer_relation_with_alternate_contact_field_content_length(self):
        """
            To check if serializer is giving validation error if relation_with_alternate_contact field content length is more than 3
        """
        self.UpdateStudentDetailsSerializer_data['relation_with_alternate_contact'] = 'a'
        serializer = UpdateStudentDetailsSerializer(data=self.UpdateStudentDetailsSerializer_data)
        self.assertFalse(serializer.is_valid())        
        self.assertEqual(set(serializer.errors), set(['relation_with_alternate_contact']))


    def test_update_student_details_serializer_relation_with_alternate_contact_field_invalid_content(self):
        """
            To check if serializer is giving validation error if relation_with_alternate_contact field contains invalid data
        """
        self.UpdateStudentDetailsSerializer_data['relation_with_alternate_contact'] = '1232'
        serializer = UpdateStudentDetailsSerializer(data=self.UpdateStudentDetailsSerializer_data)
        self.assertFalse(serializer.is_valid())        
        self.assertEqual(set(serializer.errors), set(['relation_with_alternate_contact']))


    def test_update_student_details_serializer_yr_of_exp_field_invalid_content(self):
        """
            To check if serializer is giving validation error if yr_of_exp field contains invalid data
        """
        self.UpdateStudentDetailsSerializer_data['yr_of_exp'] = 'hhhhjkh'
        serializer = UpdateStudentDetailsSerializer(data=self.UpdateStudentDetailsSerializer_data)
        self.assertFalse(serializer.is_valid())        
        self.assertEqual(set(serializer.errors), set(['yr_of_exp']))


### Test cases for UpdateEducationDetails :

    def test_update_education_details_serializer_contains_expected_fields(self):
        """
            To check fields of UpdateEducationDetailsSerializer serializer 
        """
        data = self.education_detail_serializer.data
        self.assertCountEqual(data.keys(), ['id','student', 'course', 'institution', 'percentage', 'From', 'Till'])


    def test_update_education_details_serializer_fields_content(self):
        """ 
            To check if the serialized data is same as payload given in model object for each field 
        """
        data = self.education_detail_serializer.data
        self.assertEqual(data['institution'], self.education_details_data['institution'])
        self.assertEqual(data['percentage'], self.education_details_data['percentage'])
        self.assertEqual(data['From'], self.education_details_data['From'])
        self.assertEqual(data['Till'], self.education_details_data['Till'])


    def test_update_education_details_serializer_empty_fields_content(self):
        """
            To check if serializer is giving validation error if any field is empty
        """
        self.UpdateEducationDetailsSerializer_data['institution'] = ''
        self.UpdateEducationDetailsSerializer_data['percentage'] = ''
        self.UpdateEducationDetailsSerializer_data['From'] = ''
        self.UpdateEducationDetailsSerializer_data['Till'] = ''

        serializer = UpdateEducationDetailsSerializer(data=self.UpdateEducationDetailsSerializer_data)
        self.assertFalse(serializer.is_valid())        
        self.assertEqual(set(serializer.errors), set(['institution', 'percentage', 'From', 'Till']))


    def test_update_education_details_serializer_institution_field_invalid_content(self):
        """
            To check if serializer is giving validation error if institution contains integer
        """
        self.UpdateEducationDetailsSerializer_data['institution'] = '12331'

        serializer = UpdateEducationDetailsSerializer(data=self.UpdateEducationDetailsSerializer_data)
        self.assertFalse(serializer.is_valid())        
        self.assertEqual(set(serializer.errors), set(['institution']))


    def test_update_education_details_serializer_institution_field_invalid_content_length(self):
        """
            To check if serializer is giving validation error if institution contains less than 2 characters
        """
        self.UpdateEducationDetailsSerializer_data['institution'] = 'ab'

        serializer = UpdateEducationDetailsSerializer(data=self.UpdateEducationDetailsSerializer_data)
        self.assertFalse(serializer.is_valid())        
        self.assertEqual(set(serializer.errors), set(['institution']))


    def test_update_education_details_serializer_percentage_field_invalid_content(self):
        """
            To check if serializer is giving validation error if percentage contains invalid data
        """
        self.UpdateEducationDetailsSerializer_data['percentage'] = 'ab'

        serializer = UpdateEducationDetailsSerializer(data=self.UpdateEducationDetailsSerializer_data)
        self.assertFalse(serializer.is_valid())        
        self.assertEqual(set(serializer.errors), set(['percentage']))


    def test_update_education_details_serializer_From_field_invalid_content(self):
        """
            To check if serializer is giving validation error if From contains invalid data
        """
        self.UpdateEducationDetailsSerializer_data['From'] = 'ab'

        serializer = UpdateEducationDetailsSerializer(data=self.UpdateEducationDetailsSerializer_data)
        self.assertFalse(serializer.is_valid())        
        self.assertEqual(set(serializer.errors), set(['From']))


    def test_update_education_details_serializer_Till_field_invalid_content(self):
        """
            To check if serializer is giving validation error if Till contains invalid data
        """
        self.UpdateEducationDetailsSerializer_data['Till'] = 'ab'

        serializer = UpdateEducationDetailsSerializer(data=self.UpdateEducationDetailsSerializer_data)
        self.assertFalse(serializer.is_valid())        
        self.assertEqual(set(serializer.errors), set(['Till']))


    def test_update_education_details_serializer_From_and_Till_field_float_content(self):
        """
            To check if serializer is giving validation error if From and Till contains invalid data
        """
        self.UpdateEducationDetailsSerializer_data['Till'] = 2.0
        self.UpdateEducationDetailsSerializer_data['From'] = 3.3
        serializer = UpdateEducationDetailsSerializer(data=self.UpdateEducationDetailsSerializer_data)
        self.assertFalse(serializer.is_valid())        
        self.assertEqual(set(serializer.errors), set(['From', 'Till']))



from django.test import TestCase
from authentication.models import User
from authentication.serializers import UserCreationSerializer, UpdateUserSerializer, LoginSerializer, ResetPasswordSerializer, NewPasswordSerializer

class UserSerializersTest(TestCase):

    def setUp(self):
        self.user_attributes = {
            'first_name': 'bharti',
            'last_name': 'mali',
            'username': 'bharti',
            'email': 'user@gmail.com',
            'mobile_number': '1234567890',
            'role': 'Admin',
            'password': 'bharti',
        }

        self.user_creation_serializer_data = {
            'first_name': 'bharti',
            'last_name': 'mali',
            'username': 'bharti2',
            'email': 'user2@gmail.com',
            'mobile_number': '1234567890',
            'role': 'Student',
            'password': 'bharti',
        }
        self.update_user_serializer_data = {
            'first_name': 'bharti',
            'last_name': 'mali',
            'email': 'user2@gmail.com',
            'mobile_number': '1234567890',
            'role': 'Student',
        }
        self.login_serializer_data = {
            'username': 'bharti',
            'password': 'bharti',
        }
        self.reset_password_serializer_data = {
            'email': 'user@gmail.com',
        }

        self.user = User.objects.create(**self.user_attributes)
        self.user_creation_serializer = UserCreationSerializer(instance=self.user)
        self.update_user_serializer = UpdateUserSerializer(instance=self.user)
        self.login_serializer = LoginSerializer(instance=self.user)
        self.reset_password_serializer = ResetPasswordSerializer(instance=self.user)


### Test cases for UserCreationSerailizer

    def test_user_creation_serializer_contains_expected_fields(self):
        data = self.user_creation_serializer.data
        self.assertCountEqual(data.keys(), ['id','first_name', 'last_name', 'username', 'email', 'mobile_number', 'role', 'password'])

    def test_user_creation_serializer_fields_content(self):
        data = self.user_creation_serializer.data
        self.assertEqual(data['username'], self.user_attributes['username'])
        self.assertEqual(data['first_name'], self.user_attributes['first_name'])
        self.assertEqual(data['last_name'], self.user_attributes['last_name'])
        self.assertEqual(data['password'], self.user_attributes['password'])
        self.assertEqual(data['email'], self.user_attributes['email'])
        self.assertEqual(data['role'], self.user_attributes['role'])
        self.assertEqual(data['mobile_number'], self.user_attributes['mobile_number'])

    def test_user_creation_serializer_empty_fields_content(self):
        self.user_creation_serializer_data['first_name'] = ''
        self.user_creation_serializer_data['last_name'] = ''
        self.user_creation_serializer_data['email'] = ''
        self.user_creation_serializer_data['mobile_number'] = ''
        self.user_creation_serializer_data['username'] = ''
        self.user_creation_serializer_data['password'] = ''
        serializer = UserCreationSerializer(data=self.user_creation_serializer_data)
        self.assertFalse(serializer.is_valid())        
        self.assertEqual(set(serializer.errors), set(['first_name', 'last_name', 'email', 'mobile_number', 'username', 'password']))

    def test_user_creation_serializer__min_length_of_password_content(self):
        self.user_creation_serializer_data['password'] = 'bh'
        serializer = UserCreationSerializer(data=self.user_creation_serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['password']))

    def test_user_creation_serializer_duplicate_username_content(self):
        self.user_creation_serializer_data['username'] = 'bharti'
        serializer = UserCreationSerializer(data=self.user_creation_serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['username']))

    def test_user_creation_serializer_mobile_number_content_min_length(self):
        self.user_creation_serializer_data['mobile_number'] = '1234'
        serializer = UserCreationSerializer(data=self.user_creation_serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['mobile_number']))

    def test_user_creation_serializer_mobile_number_content_type(self):
        self.user_creation_serializer_data['mobile_number'] = 'bhartimali'
        serializer = UserCreationSerializer(data=self.user_creation_serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['mobile_number']))

    def test_user_creation_serializer_mobile_number_content_max_length(self):
        self.user_creation_serializer_data['mobile_number'] = '7778799908898'
        serializer = UserCreationSerializer(data=self.user_creation_serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['mobile_number']))

    def test_user_creation_serializer_duplicate_email_content(self):
        self.user_creation_serializer_data['email'] = 'user@gmail.com'
        serializer = UserCreationSerializer(data=self.user_creation_serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['email']))

    def test_user_creation_serializer_integer_email_content(self):
        self.user_creation_serializer_data['email'] = '123444'
        serializer = UserCreationSerializer(data=self.user_creation_serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['email']))

    def test_user_creation_serializer_invalid_email_content(self):
        self.user_creation_serializer_data['email'] = 'user@com'
        serializer = UserCreationSerializer(data=self.user_creation_serializer_data)
        self.assertFalse(serializer.is_valid())        
        self.assertEqual(set(serializer.errors), set(['email']))

### Test cases for UpdateUserSerailizer
    def test_update_user_serializer_contains_expected_fields(self):
        data = self.update_user_serializer.data
        self.assertCountEqual(data.keys(), ['id','first_name', 'last_name', 'username', 'email', 'mobile_number', 'role', 'password'])

    def test_update_user_serializer_fields_content(self):
        data = self.update_user_serializer.data
        self.assertEqual(data['username'], self.user_attributes['username'])
        self.assertEqual(data['first_name'], self.user_attributes['first_name'])
        self.assertEqual(data['last_name'], self.user_attributes['last_name'])
        self.assertEqual(data['password'], self.user_attributes['password'])
        self.assertEqual(data['email'], self.user_attributes['email'])
        self.assertEqual(data['role'], self.user_attributes['role'])
        self.assertEqual(data['mobile_number'], self.user_attributes['mobile_number'])

    def test_update_user_serializer_empty_fields_content(self):
        self.update_user_serializer_data['first_name'] = ''
        self.update_user_serializer_data['last_name'] = ''
        self.update_user_serializer_data['email'] = ''
        self.update_user_serializer_data['mobile_number'] = ''
        serializer = UpdateUserSerializer(data=self.update_user_serializer_data)
        self.assertFalse(serializer.is_valid())        
        self.assertEqual(set(serializer.errors), set(['first_name', 'last_name', 'email', 'mobile_number']))

    def test_update_user_serializer_mobile_number_content_min_length(self):
        self.update_user_serializer_data['mobile_number'] = '1234'
        serializer = UpdateUserSerializer(data=self.update_user_serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['mobile_number']))

    def test_update_user_serializer_mobile_number_content_type(self):
        self.update_user_serializer_data['mobile_number'] = 'bhartimali'
        serializer = UpdateUserSerializer(data=self.update_user_serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['mobile_number']))

    def test_update_user_serializer_mobile_number_content_max_length(self):
        self.update_user_serializer_data['mobile_number'] = '7778799908898'
        serializer = UpdateUserSerializer(data=self.update_user_serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['mobile_number']))

    def test_update_user_serializer_duplicate_email_content(self):
        self.update_user_serializer_data['email'] = 'user@gmail.com'
        serializer = UpdateUserSerializer(data=self.update_user_serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['email']))

    def test_update_user_serializer_integer_email_content(self):
        self.update_user_serializer_data['email'] = '123444'
        serializer = UpdateUserSerializer(data=self.update_user_serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['email']))

    def test_update_user_serializer_invalid_email_content(self):
        self.update_user_serializer_data['email'] = 'user@com'
        serializer = UpdateUserSerializer(data=self.update_user_serializer_data)
        self.assertFalse(serializer.is_valid())        
        self.assertEqual(set(serializer.errors), set(['email']))


### Test cases for LoginSerializer : 

    def test_login_serializer_contains_expected_fields(self):
        data = self.login_serializer.data
        self.assertCountEqual(data.keys(), ['id', 'username', 'password'])

    def test_login_serializer_fields_content(self):
        data = self.login_serializer.data
        self.assertEqual(data['username'], self.user_attributes['username'])
        self.assertEqual(data['password'], self.user_attributes['password'])

    def test_login_serializer_empty_fields_content(self):
        self.login_serializer_data['username'] = ''
        self.login_serializer_data['password'] = ''
        serializer = LoginSerializer(data=self.login_serializer_data)
        self.assertFalse(serializer.is_valid())        
        self.assertEqual(set(serializer.errors), set(['username', 'password']))

### Test cases for ResetPasswordSerailizer : 

    def test_reset_password_serializer_contains_expected_fields(self):
        data = self.reset_password_serializer.data
        self.assertCountEqual(data.keys(), ['email'])

    def test_reset_password_serializer_fields_content(self):
        data = self.reset_password_serializer.data
        self.assertEqual(data['email'], self.user_attributes['email'])

    def test_reset_password_serializer_empty_fields_content(self):
        self.reset_password_serializer_data['email'] = ''
        serializer = ResetPasswordSerializer(data=self.reset_password_serializer_data)
        self.assertFalse(serializer.is_valid())        
        self.assertEqual(set(serializer.errors), set(['email']))


from rest_framework import serializers
from learning_mgt.models import Student, EducationDetails, Course, Mentor


class UpdateStudentDetailsSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Student
        fields = ['image', 'contact', 'alternate_contact', 'relation_with_alternate_contact','current_location','Address','git_link','yr_of_exp']

class UpdateEducationDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationDetails
        fields = ['course', 'institution', 'percentage']

class AddCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_name']

class ListMentorsSerializer(serializers.ModelSerializer):
    mentor = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Mentor
        fields = ['mentor','course']

class MentorSerializer(serializers.ModelSerializer):
    mentor = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Mentor
        fields = ['mentor','course']

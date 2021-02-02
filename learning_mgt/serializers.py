from rest_framework import serializers
from learning_mgt.models import Student, EducationDetails, Course, Mentor, MentorStudent


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

class MentorsSerializer(serializers.ModelSerializer):
    mentor = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Mentor
        fields = ['mentor','course']

class MentorCourseMappingSerializer(serializers.ModelSerializer):
    mentor = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Mentor
        fields = ['mentor','course']

class MentorStudentMappingSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = MentorStudent
        fields = ['student', 'course', 'mentor']

class MentorStudentListSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True)
    mentor = serializers.StringRelatedField(read_only=True)
 
    class Meta:
        model = MentorStudent
        fields = ['student', 'course', 'mentor']





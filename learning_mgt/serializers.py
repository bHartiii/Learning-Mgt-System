from rest_framework import serializers
from learning_mgt.models import Student, EducationDetails, Course, Mentor, MentorStudent, Performance


class UpdateStudentDetailsSerializer(serializers.ModelSerializer):   
    student = serializers.StringRelatedField(read_only=True)
    contact = serializers.RegexField("^[7-9]{1}[0-9]{9}$")
    alternate_contact = serializers.RegexField("^[7-9]{1}[0-9]{9}$")
    relation_with_alternate_contact = serializers.RegexField("[a-zA-Z]{3,}", max_length=50)
    class Meta:
        model = Student
        fields = ['id', 'student', 'image', 'contact', 'alternate_contact', 'relation_with_alternate_contact','current_location','Address','git_link','yr_of_exp']

class UpdateEducationDetailsSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    institution = serializers.RegexField("[a-zA-Z]{3,}", max_length=50)
    class Meta:
        model = EducationDetails
        fields = ['id','student', 'course', 'institution', 'percentage', 'From', 'Till']
        extra_kwargs = {'course':{'read_only':True}}

class AddCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id','course_name']

class MentorsSerializer(serializers.ModelSerializer):
    mentor = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Mentor
        fields = ['id', 'mentor', 'course']

class MentorCourseMappingSerializer(serializers.ModelSerializer):
    mentor = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Mentor
        fields = ['id', 'mentor','course']

class MentorStudentMappingSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = MentorStudent
        fields = ['id', 'student', 'course', 'mentor']

class MentorStudentUpdateMappingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MentorStudent
        fields = ['student', 'course', 'mentor']
        extra_kwargs = {'student': {'read_only': True}}

class MentorStudentListSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True)
    mentor = serializers.StringRelatedField(read_only=True)
 
    class Meta:
        model = MentorStudent
        fields = ['student', 'course', 'mentor']

class PerformanceSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    mentor = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Performance
        fields = '__all__'





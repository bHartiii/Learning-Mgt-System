from rest_framework import serializers
from learning_mgt.models import Student, EducationDetails


class UpdateStudentDetailsSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Student
        fields = ['image', 'contact', 'alternate_contact', 'relation_with_alternate_contact','current_location','Address','git_link','yr_of_exp']

class UpdateEducationDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationDetails
        fields = ['course', 'institution', 'percentage']
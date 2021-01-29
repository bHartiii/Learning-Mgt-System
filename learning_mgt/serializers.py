from rest_framework import serializers
from learning_mgt.models import Student


class UpdateStudentDetailsSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Student
        fields = ['contact', 'alternate_contact', 'relation_with_alternate_contact','current_location','Address','git_link','yr_of_exp','image']

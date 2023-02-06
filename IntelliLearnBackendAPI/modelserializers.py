from rest_framework import serializers
from IntelliLearnBackendAPI.models import McqModel
from IntelliLearnBackendAPI.models import StudentModel
from IntelliLearnBackendAPI.models import classModel

class McqSerializer(serializers.ModelSerializer):

    class Meta:

        model = McqModel
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):

    class Meta:

        model = StudentModel
        fields = '__all__'

class ClassSerializer(serializers.ModelSerializer):

    class Meta:

        model = classModel
        fields = '__all__'

from rest_framework import serializers
from IntelliLearnBackendAPI.models import McqModel
from IntelliLearnBackendAPI.models import StudentModel
from IntelliLearnBackendAPI.models import classModel
from IntelliLearnBackendAPI.models import TeacherModel
from IntelliLearnBackendAPI.models import AttendanceModel
from IntelliLearnBackendAPI.models import EnrollmentModel
from IntelliLearnBackendAPI.models import MarksModel

class McqSerializer(serializers.ModelSerializer):

    class Meta:

        model = McqModel
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):

    class Meta:

        model = StudentModel
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):

    class Meta:

        model = TeacherModel
        fields = '__all__'


class ClassSerializer(serializers.ModelSerializer):

    class Meta:

        model = classModel
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:

        model = AttendanceModel
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):

    class Meta:

        model = EnrollmentModel
        fields = '__all__'

class MarksSerializer(serializers.ModelSerializer):

    class Meta:

        model = MarksModel
        fields = '__all__'
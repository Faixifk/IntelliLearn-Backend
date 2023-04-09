from rest_framework import serializers
from IntelliLearnBackendAPI.models import McqModel
from IntelliLearnBackendAPI.models import StudentModel
from IntelliLearnBackendAPI.models import classModel
from IntelliLearnBackendAPI.models import TeacherModel
from IntelliLearnBackendAPI.models import AttendanceModel
from IntelliLearnBackendAPI.models import EnrollmentModel
from IntelliLearnBackendAPI.models import TeacherAttendance
from IntelliLearnBackendAPI.models import MarksModel
from IntelliLearnBackendAPI.models import TeacherSchedule

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

#Example on how to return attributes from Foreign objects:

#return the actual key for foriegn key objects instead of object itself
#for example print teacher class id in the model
# class TeacherAttendanceSerializer(serializers.ModelSerializer):

#     teacher_ID = serializers.IntegerField(source='teacher.teacher_ID')
#     teacher_class_ID = serializers.IntegerField(source='teacher_class.class_ID')

#     class Meta:
#         model = TeacherAttendance
#         fields = ['attendance_ID', 'date', 'status', 'teacher_ID', 'teacher_class_ID']

class TeacherAttendancePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeacherAttendance
        fields = '__all__'

class TeacherAttendanceSerializer(serializers.ModelSerializer):

    class_level = serializers.CharField(source='teacher_class.class_level')
    section = serializers.CharField(source='teacher_class.section')
    subject = serializers.CharField(source='teacher_class.subject')

    class Meta:
        model = TeacherAttendance
        fields = ['attendance_ID', 'date', 'status', 'class_level', 'section', 'subject']

class TeacherScheduleSerializer(serializers.ModelSerializer):

    class Meta:

        model = TeacherSchedule
        fields = '__all__'

class TeacherScheduleGetSerializer(serializers.ModelSerializer):

    class_level = serializers.CharField(source='Class.class_level')
    section = serializers.CharField(source='Class.section')
    subject = serializers.CharField(source='Class.subject')
    startTime = serializers.TimeField(source='startTime')
    startTime = str(startTime)

    class Meta:

        model = TeacherSchedule
        fields = ['id', 'weekday', 'startTime', 'durationMinutes', 'roomNumber', 'class_level', 'section', 'subject']

from django.contrib import admin
from IntelliLearnBackendAPI.models import McqModel
from IntelliLearnBackendAPI.models import classModel
from IntelliLearnBackendAPI.models import StudentModel
from IntelliLearnBackendAPI.models import AttendanceModel, TeacherModel, MarksModel, EnrollmentModel

# Register your models here.
admin.site.register(McqModel)
admin.site.register(classModel)
admin.site.register(StudentModel)
admin.site.register(AttendanceModel)
admin.site.register(TeacherModel)
admin.site.register(MarksModel)
admin.site.register(EnrollmentModel)

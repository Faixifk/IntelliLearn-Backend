from django.db import models

# Create your models here.
class McqModel(models.Model):

    question_ID	= models.AutoField(primary_key=True)
    question = models.CharField(max_length=500, blank=False, default='None')
    option_a = models.CharField(max_length=100, blank=False, default='None')	
    option_b = models.CharField(max_length=100, blank=False, default='None')	
    option_c = models.CharField(max_length=100, blank=False, default='None')	
    option_d = models.CharField(max_length=100, blank=False, default='None')	
    correct_option = models.CharField(max_length=100, blank=False, default='None')	
    weight = models.IntegerField(blank=False, default=1)

    unit_number = models.IntegerField(blank=False, default=-1)
    topic = models.CharField(max_length=100, blank=False, default='None')	

class TeacherModel(models.Model):

    teacher_ID	= models.AutoField(primary_key=True)
    
    email = models.CharField(unique=True, max_length=50, blank=False, default='None')
    password = models.CharField(max_length=50, blank=False, default='None')

    name = models.CharField(max_length=50, blank=False, default='None')

class classModel(models.Model):

    class_ID	= models.AutoField(primary_key=True)
    teacher_ID	= models.ForeignKey(TeacherModel, default=None, on_delete=models.DO_NOTHING)
    class_level = models.CharField(max_length=10, blank=False, default='None')	
    section = models.CharField(max_length=10, blank=False, default='None')	
    subject = models.CharField(max_length=30, blank=False, default='None')	
    capacity = models.IntegerField(blank=False)
    num_students = models.IntegerField(blank=False)

class StudentModel(models.Model):

    student_ID	= models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False, default='None')
    
    email = models.CharField(max_length=50, blank=False, default='None')
    password = models.CharField(max_length=50, blank=False, default='None')

class AttendanceModel(models.Model):

    attendance_ID = models.AutoField(primary_key=True)
    date = models.DateField()
    student_class = models.ForeignKey(classModel, default=None, on_delete=models.DO_NOTHING)
    student = models.ForeignKey(StudentModel, default=None, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=1, blank=False, default='P')

class TeacherAttendance(models.Model):

    attendance_ID = models.AutoField(primary_key=True)
    date = models.DateField()
    teacher_class = models.ForeignKey(classModel, default=None, on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(TeacherModel, default=None, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=1, blank=False, default='P')

class EnrollmentModel(models.Model):

    enrollment_ID = models.AutoField(primary_key=True)
    date = models.DateField()
    class_ID = models.ForeignKey(classModel, default=None, on_delete=models.DO_NOTHING)
    student_ID = models.ForeignKey(StudentModel, default=None, on_delete=models.DO_NOTHING)

class MarksModel(models.Model):

    marks_ID = models.AutoField(primary_key=True)
    date = models.DateField()
    class_ID = models.ForeignKey(classModel, default=None, on_delete=models.DO_NOTHING)
    student_ID = models.ForeignKey(StudentModel, default=None, on_delete=models.DO_NOTHING)
    evaluationType = models.CharField(max_length=20)
    totalMarks = models.IntegerField()
    obtainedMarks = models.IntegerField()

class TeacherSchedule(models.Model):

    teacher = models.ForeignKey(TeacherModel, default=None, on_delete=models.DO_NOTHING)
    Class = models.ForeignKey(classModel, default=None, on_delete=models.DO_NOTHING)
    weekday = models.CharField(max_length=10)
    startTime = models.TimeField()
    durationMinutes = models.IntegerField()
    roomNumber = models.CharField(max_length=10)

class TeacherAnnouncement(models.Model):

    announcement_ID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    date_posted = models.DateField()
    author = models.ForeignKey(TeacherModel, default=None, on_delete=models.DO_NOTHING)
    content = models.CharField(max_length=500)
    class_ID = models.ForeignKey(classModel, default=None, on_delete=models.DO_NOTHING)

class BluetoothStudentMappings(models.Model):

    mac_address = models.CharField(primary_key=True, max_length=100)
    student = models.ForeignKey(StudentModel, default=None, on_delete=models.DO_NOTHING)

class UploadedBook(models.Model):
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='books/')
    className = models.CharField(max_length=255)
    txt_path = models.CharField(max_length=255, blank=True, null=True)


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

class classModel(models.Model):

    class_ID	= models.AutoField(primary_key=True)
    class_level = models.CharField(max_length=10, blank=False, default='None')	
    section = models.CharField(max_length=10, blank=False, default='None')	
    capacity = models.IntegerField(blank=False)
    num_students = models.IntegerField(blank=False)

class StudentModel(models.Model):

    student_ID	= models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False, default='None')
    student_class = models.ForeignKey(classModel, default=None, on_delete=models.DO_NOTHING)

class AttendanceModel(models.Model):

    attendance_ID = models.AutoField(primary_key=True)
    date = models.DateField()
    student_class = models.ForeignKey(classModel, default=None, on_delete=models.DO_NOTHING)
    student = models.ForeignKey(StudentModel, default=None, on_delete=models.DO_NOTHING)
    

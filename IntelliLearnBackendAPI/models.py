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

# Generated by Django 4.1.5 on 2023-01-09 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IntelliLearnBackendAPI', '0003_mcqmodel_topic_mcqmodel_unit_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mcqmodel',
            name='question',
            field=models.CharField(default='None', max_length=500),
        ),
    ]
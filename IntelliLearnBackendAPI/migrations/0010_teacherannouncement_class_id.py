# Generated by Django 4.1.5 on 2023-04-12 03:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('IntelliLearnBackendAPI', '0009_teacherannouncement'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacherannouncement',
            name='class_ID',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='IntelliLearnBackendAPI.classmodel'),
        ),
    ]

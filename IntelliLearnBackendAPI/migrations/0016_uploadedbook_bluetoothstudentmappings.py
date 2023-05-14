# Generated by Django 4.1.5 on 2023-04-21 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('IntelliLearnBackendAPI', '0015_alter_teacherannouncement_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('pdf_file', models.FileField(upload_to='books/')),
            ],
        ),
        migrations.CreateModel(
            name='BluetoothStudentMappings',
            fields=[
                ('mac_address', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('student', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='IntelliLearnBackendAPI.studentmodel')),
            ],
        ),
    ]

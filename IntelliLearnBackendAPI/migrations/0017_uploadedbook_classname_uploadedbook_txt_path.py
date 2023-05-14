# Generated by Django 4.1.5 on 2023-05-14 07:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('IntelliLearnBackendAPI', '0016_uploadedbook_bluetoothstudentmappings'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedbook',
            name='className',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='uploadedbook',
            name='txt_path',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

# Generated by Django 4.1.5 on 2023-01-07 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='McqModel',
            fields=[
                ('question_ID', models.AutoField(primary_key=True, serialize=False)),
                ('question', models.TextField(default='None')),
                ('option_a', models.TextField(default='None')),
                ('option_b', models.TextField(default='None')),
                ('option_c', models.TextField(default='None')),
                ('option_d', models.TextField(default='None')),
                ('correct_option', models.TextField(default='None')),
                ('weight', models.IntegerField(default=1)),
            ],
        ),
    ]
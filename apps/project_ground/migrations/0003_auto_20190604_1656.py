# Generated by Django 2.2.1 on 2019-06-04 16:56

import apps.project_ground.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_ground', '0002_auto_20190426_1743'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreprocessingTasks',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('type', models.IntegerField()),
                ('action_strategy', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='project',
            name='basefilename',
            field=models.TextField(blank=True, default='Main Dataset'),
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('basefilename', models.TextField(blank=True, default='Main Dataset')),
                ('PreprocessingTasks_id', models.ManyToManyField(to='project_ground.PreprocessingTasks')),
            ],
        ),
    ]

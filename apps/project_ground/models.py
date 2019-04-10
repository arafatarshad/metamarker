from django.db import models
import uuid
# Create your models here.

class DatasetType(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    author_first_name=models.CharField(max_length=100)
    author_last_name=models.CharField(max_length=100)
    description=models.TextField()

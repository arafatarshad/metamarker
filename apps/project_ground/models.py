from django.db import models
import datetime
import uuid
from django.conf import settings
from django.core.validators import FileExtensionValidator
import os
import random




class DatasetType(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Project(models.Model):

    def upload_path(instance, filename):
        basefilename, file_extension= os.path.splitext(filename)
        chars= 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
        randomstr= ''.join((random.choice(chars)) for x in range(10))
        return '{basename}_{randomstring}{ext}'.format(basename= basefilename, randomstring= randomstr, ext= file_extension)


    id = models.AutoField(primary_key=True)
    author_first_name=models.CharField(max_length=100,blank=False)
    author_last_name=models.CharField(max_length=100,blank=False)
    description=models.TextField(max_length=250,blank=True)
    email=models.EmailField(blank=False)

    # reference_id=models.UUIDField(default=uuid.uuid4, editable=False,unique=True)
    reference_id = models.CharField(max_length=64, verbose_name=u"Reference key",
                 default=uuid.uuid1)

    dataset= models.FileField(upload_to=upload_path,null=True,blank=False,validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    dataset_type_id = models.ForeignKey(DatasetType, on_delete=models.CASCADE,null=True)
    basefilename=models.TextField(blank=True)

    def __str__(self):
        return str(self.reference_id)

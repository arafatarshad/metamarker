from django.db import models
import datetime
import uuid
from django.conf import settings
from django.core.validators import FileExtensionValidator

class DatasetType(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)

class Project(models.Model):
    # author and project related field



    def upload_path(instance, filename):
        basefilename, file_extension= os.path.splitext(filename)
        chars= 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
        randomstr= ''.join((random.choice(chars)) for x in range(10))
        return 'uploads/{basename}_{randomstring}{ext}'.format(basename= basefilename, randomstring= randomstr, ext= file_extension)


    id = models.AutoField(primary_key=True)
    author_first_name=models.CharField(max_length=100,blank=False)
    author_last_name=models.CharField(max_length=100,blank=False)
    description=models.TextField(max_length=250,blank=True)
    email=models.EmailField(blank=False)
    project_reference=models.CharField(max_length=128, null=True, blank=True, unique=True)

    # dataset related fileds
    dataset= models.FileField(upload_to=upload_path,null=True,blank=False,validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    dataset_type_id = models.ForeignKey(DatasetType, on_delete=models.CASCADE,null=True)
    basefilename=models.TextField(blank=True)



    def __init__(self):
        super(Project, self).__init__()
        self.project_reference = str(uuid.uuid4())

    def __str__(self):
        return self.description

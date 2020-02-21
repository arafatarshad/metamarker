from django.db import models
import datetime
import uuid
from django.conf import settings
from django.core.validators import FileExtensionValidator
import os
import random

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)

class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)

class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)

class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)

class ComponentResult(models.Model):
    component_id = models.IntegerField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)  # This field type is a guess.
    pca_result = models.ForeignKey('PcaResult', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'component_result'
        unique_together = (('id', 'pca_result'),)

class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'

class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)

class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'

class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

class Extradataset(models.Model):
    name = models.CharField(max_length=100)
    basefilename = models.TextField()
    project_id = models.ForeignKey('Project', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'extradataset'

class Job(models.Model):
    status = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    processing_algorithm = models.ForeignKey('ProcessingAlgorithm', models.DO_NOTHING)
    extradataset = models.ForeignKey(Extradataset, models.DO_NOTHING, blank=True, null=True)
    project = models.ForeignKey('Project', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'job'
        unique_together = (('id', 'processing_algorithm', 'project'),)

class PcaJobParameters(models.Model):
    no_of_components = models.IntegerField()
    reduce_to = models.IntegerField(blank=True, null=True)
    job = models.ForeignKey(Job, models.DO_NOTHING)
    standard_scale = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pca_job_parameters'
        unique_together = (('id', 'job'),)

class PcaResult(models.Model):
    variance_explained = models.TextField(blank=True, null=True)  # This field type is a guess.
    job = models.ForeignKey(Job, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pca_result'
        unique_together = (('id', 'job'),)

class PreprocessingTasks(models.Model):
    name = models.CharField(max_length=100)
    type = models.IntegerField()
    action_strategy = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'preprocessingtasks'

class ProcessingAlgorithm(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    reference_id = models.CharField(max_length=11)
    class Meta:
        managed = False
        db_table = 'processing_algorithm'

class Project(models.Model):
    def upload_path(instance, filename):
        basefilename, file_extension= os.path.splitext(filename)
        chars= 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
        randomstr= ''.join((random.choice(chars)) for x in range(10))
        return '{basename}_{randomstring}{ext}'.format(basename= basefilename, randomstring= randomstr, ext= file_extension)


    author_first_name = models.CharField(max_length=100)
    author_last_name = models.CharField(max_length=100)
    description = models.TextField()
    email = models.CharField(max_length=254)
    # reference_id = models.CharField(max_length=64)
    # dataset = models.CharField(max_length=100, blank=True, null=True)


    basefilename = models.TextField()

    reference_id = models.CharField(max_length=64, verbose_name=u"Reference key",
                 default=uuid.uuid1)
    dataset= models.FileField(upload_to=upload_path,null=True,blank=False,validators=[FileExtensionValidator(allowed_extensions=['csv'])])


    class Meta:
        managed = False
        db_table = 'project'




class DaaResultAndParameter(models.Model):
    permute_diff_cor = models.TextField(blank=True, null=True)  # This field type is a guess.
    permute_sig_corr = models.TextField(blank=True, null=True)  # This field type is a guess.
    network_data = models.TextField(blank=True, null=True)  # This field type is a guess.
    sig_count = models.IntegerField(blank=True, null=True)
    job = models.ForeignKey('Job', models.DO_NOTHING)
    scaler_scale = models.IntegerField(blank=True, null=True)
    diff_cor = models.TextField(blank=True, null=True) # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'daa_result_and_parameter'

class PlsDa(models.Model):
    scaler_scale = models.IntegerField(blank=True, null=True)
    job = models.ForeignKey(Job, models.DO_NOTHING)
    no_of_components = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pls_da'
        unique_together = (('id', 'job'),)

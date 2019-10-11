from django.shortcuts import render

# Create your views here.
from background_task import background
from django.contrib.auth.models import User
from django.http import HttpResponse
import datetime
from apps.project_ground.models import Project, Job

from django.core.mail import send_mail
from django.core.mail import EmailMessage


def tellThemProjectStarts(job):
    subject= "Update: Project Processing About tor start"
    body="Dear Client the task that you have created for the projct with reference id " + job.project.reference_id + " is now being procesed by the server. we will update you once it is done !";
    to=[job.project.email]
    email = EmailMessage(subject, body, to=to)
    email.send()

def tellThemProjectCompletes(job):
    subject= "Update: Project Processing About tor start"
    body="Dear Client the task that you have created for the projct with reference id " + job.project.reference_id + " is complete. !";
    to=[job.project.email]
    email = EmailMessage(subject, body, to=to)
    email.send()

def notifyCompleteTakUser():
    all_complete_jobs = Job.objects.filter(status=0)
    for job in all_complete_jobs:
        tellThemProjectCompletes(job)
        job.status=0
        job.save()

    # print(all_complete_jobs)

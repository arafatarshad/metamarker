
from django.shortcuts import render
from django.shortcuts import redirect

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.forms.utils import ErrorList
from django.http import HttpResponse

from apps.project_ground.models import Project, ExtraDataset, PreprocessingTasks
from apps.project_ground.models import ExtraDataset, PreprocessingTasks , Project,AllParameters,Job, JobParameters

import json
from django.core import serializers
# Create your views here.
class JOB(APIView):

        def get(self, request, *args, **kwargs):
            return render(request,"job/job.html",{"page_title":"Task-Manager"})


        def getJobData(request,id):
            # job=Job.objects.all()
            job=Job.objects.filter(status__in=[0,1,2])

            data = []
            for single_job in job:
                query={}
                if single_job.status == 0:
                    query["status"]="Pending"
                elif  single_job.status == 1:
                    query["status"]="Processsing"
                else:
                    query["status"]="Complete"

                query["id"]=single_job.id
                query["dataset_name"]=single_job.extradataset.name
                query["processing_algorithm"]=single_job.processing_algorithm.name

                data.append(query)
            return HttpResponse(json.dumps(data), content_type='application/json')

        def deleteJOB(self,request,id):
            job = Job.objects.get(pk=id)
            job.status=50
            job.save()
            return render(request,"job/job.html",{"page_title":"Task-Manager"})

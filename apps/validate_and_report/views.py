from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse

import pandas as pd
import os
import random
from apps.project_ground.models import Project,Job
import json

class Main(APIView):

        def get(self, request, *args, **kwargs):
            project = Project.objects.get(reference_id=request.session['reference_id'])
            # dataset=ExtraDataset.objects.filter(project_id=project)
            # preprocessing_tasks=PreprocessingTasks.objects.all()
            return render(request,"validate_and_report/home.html",{"page_title":"Validate And Report","project":project})
            # return HttpResponse(project)

        def getJobData(request,id):
            # print(id)
            job=Job.objects.filter(status=3,project_id=id)
            data = []
            for single_job in job:
                query={}
                query["id"]=single_job.id
                if single_job.extradataset_id==None:
                    query["dataset_name"]="Main Dataset"
                else:
                    query["dataset_name"]=single_job.extradataset.name
                query["processing_algorithm"]=single_job.processing_algorithm.name
                query["created_at"]=single_job.created_at.strftime('%d  %b , %Y - %H : %M : %S')
                data.append(query)
                # print(query)
            return HttpResponse(json.dumps(data), content_type='application/json')


        def showResult(self, id):
            print(id)
        #     project = Project.objects.get(reference_id=request.session['reference_id'])
        #     project.description=request.POST['description']
        #     project.author_first_name=request.POST['author_first_name']
        #     project.author_last_name=request.POST['author_last_name']
        #     # project.email=request.POST['email']
        #     project.save()
        #     # print(request.POST)
        #     # dataset=ExtraDataset.objects.filter(project_id=project)
        #     # preprocessing_tasks=PreprocessingTasks.objects.all()
        #     # return HttpResponse(project)
        #     return render(request,"settings/settings.html",{"page_title":"settings","project":project})
        # def deleteProject(self,id):
            job = Job.objects.get(id=id)
            return HttpResponse(job)

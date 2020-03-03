from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework.views import APIView
from django.http import HttpResponse

import pandas as pd
import os
import random
from apps.project_ground.models import Project
class Settings(APIView):

        def get(self, request, *args, **kwargs):
            project = Project.objects.get(reference_id=request.session['reference_id'])
            # dataset=ExtraDataset.objects.filter(project_id=project)
            # preprocessing_tasks=PreprocessingTasks.objects.all()
            return render(request,"settings/settings.html",{"page_title":"settings","project":project})
            # return HttpResponse(project)
        def post(self, request, *args, **kwargs):
            project = Project.objects.get(reference_id=request.session['reference_id'])
            project.description=request.POST['description']
            project.author_first_name=request.POST['author_first_name']
            project.author_last_name=request.POST['author_last_name']
            # project.email=request.POST['email']
            project.save()
            # print(request.POST)
            # dataset=ExtraDataset.objects.filter(project_id=project)
            # preprocessing_tasks=PreprocessingTasks.objects.all()
            # return HttpResponse(project)
            return render(request,"settings/settings.html",{"page_title":"settings","project":project})
        def deleteProject(self,id):
            project = Project.objects.get(id=id)
            return HttpResponse(project)

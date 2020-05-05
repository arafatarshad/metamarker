import os
import uuid
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

from apps.project_ground.models import Project,Job
from apps.project_ground.models import Extradataset as ExtraDataset

import datetime
from sklearn import preprocessing


import pandas as pd


# Create your views here.
class compare_result(APIView):
        def get(self, request, *args, **kwargs):
            project = Project.objects.get(reference_id=request.session['reference_id'])
            
            jobs=Job.objects.filter(project_id=project.id,status=3)
            # print(jobs[0].proce)
            # dataset=ExtraDataset.objects.filter(project_id=project)
            # preprocessing_tasks=PreprocessingTasks.objects.all()
            return render(request,"compare_result/home.html",{"page_title":"Result Compare","project":project,"jobs":jobs})
            # return    HttpResponse(project.id)
        
        def post(self, request, *args, **kwargs):
            project = Project.objects.get(reference_id=request.session['reference_id'])
            dataset_id =request.POST['dataset_id']
            df=self.getUsProperDf(dataset_id,project)

            df=self.PreprocessDataframe(df,request)
            self.saveDataSet(project,request,df)
            now = datetime.datetime.now()
            html = "<html><body>It is now %s.</body></html>" % now
            return    HttpResponse(html)

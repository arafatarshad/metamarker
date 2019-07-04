import os
import uuid
from django.shortcuts import render
from django.shortcuts import redirect

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.forms.utils import ErrorList
from django.http import HttpResponse

from apps.project_ground.models import Project, ExtraDataset, PreprocessingTasks

from django.http import HttpResponse
import datetime
from .lib.missing_value_handler import MissingValueHandler
from .lib.scaling import ScalingDatasethandler


from apps.project_ground.models import ExtraDataset, PreprocessingTasks , Project

import pandas as pd
import os
import random


# Create your views here.
class showPreprocessingIndex(APIView):

        def __init__(self):
            self.missing_value_handler = MissingValueHandler()
            self.scaling_handler=ScalingDatasethandler()

        def file_name(self):
            chars= 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
            randomstr= ''.join((random.choice(chars)) for x in range(10))
            return '{randomstring}{ext}'.format(randomstring= randomstr, ext= '.csv')

        def get(self, request, *args, **kwargs):
            project = Project.objects.get(reference_id=request.session['reference_id'])
            dataset=ExtraDataset.objects.filter(project_id=project)
            preprocessing_tasks=PreprocessingTasks.objects.all()
            return render(request,"preprocessing/preprocessing.html",{"page_title":"Pre-processing","project":project,
                                                                    "dataset":dataset,"preprocessing_tasks":preprocessing_tasks})

        def post(self, request, *args, **kwargs):
            project = Project.objects.get(reference_id=request.session['reference_id'])
            dataset_id =request.POST['dataset_id']
            df=self.getUsProperDf(dataset_id,project)

            df=self.PreprocessDataframe(df,request)
            self.saveDataSet(project,request,df)
            now = datetime.datetime.now()
            html = "<html><body>It is now %s.</body></html>" % now
            return    HttpResponse(html)

        def saveDataSet(self,project,request,df):
            file_name=self.file_name()
            new_dataset= ExtraDataset()
            new_dataset.name=request.POST['name']
            new_dataset.project_id=project

            new_dataset.basefilename=file_name
            df.to_csv("uploads/"+file_name)
            new_dataset.save()
            for c in dict(request.POST)["PreprocessingTasks_id"]:
                new_dataset.PreprocessingTasks_id.add(c)
            new_dataset.save()


        def getUsProperDf(self,dataset_id,project):
            if dataset_id=='00000':
                return pd.read_csv(project.dataset)
            else:
                filenmae=ExtraDataset.objects.filter(id=dataset_id).first().basefilename
                return pd.read_csv("uploads/"+filenmae)
        def one(self,df):
            # global missing_value_handler
            columns = df.columns
            return self.missing_value_handler.fixTheColumnsDatatype(df,columns)
        def three(self,df):
            return self.scaling_handler.meanRemovalAndVarianceScaling(df)
        def four(self,df):
            return self.scaling_handler.UnivariateScaling(df)
        def five(self,df):
            return self.scaling_handler.ParetoScaling(df)
        def six(self,df):
            return self.scaling_handler.LnScaling(df)
        def seven(self,df):
            return self.scaling_handler.VastScaling(df)
        def eight(self,df):
            return self.scaling_handler.XVastScaliong(df)
        def nine(self,df):
            return self.scaling_handler.RangeScaling(df)
        def ten(self,df):
            return self.scaling_handler.XVastScaliong(df)


        def PreprocessDataframe(self,df,request):
            options={1:self.one,3:self.three,4:self.four,5:self.five,6:self.six,7:self.seven,8:self.eight,9:self.nine,10:self.ten}
            for c in dict(request.POST)["PreprocessingTasks_id"]:
                df= options[(int)(c)](df)
            return df

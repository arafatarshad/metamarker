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


from apps.project_ground.models import ExtraDataset, PreprocessingTasks , Project

import pandas as pd
import os
import random


from .lib.lib import PCA_Helper
# Create your views here.
class PCA(APIView):

        def get(self, request, *args, **kwargs):
            project = Project.objects.get(reference_id=request.session['reference_id'])
            dataset=ExtraDataset.objects.filter(project_id=project)
            totalColumns=range(len(pd.read_csv(project.dataset).columns)-1)
            return render(request,"processing/pca/pca_processing.html",{"page_title":"PCA-processing","project":project,"dataset":dataset,"total_columns":totalColumns})

        def post(self, request, *args, **kwargs):
            project = Project.objects.get(reference_id=request.session['reference_id'])
            dataset_id =request.POST['dataset_id']
            no_of_components =request.POST['no_of_components']
            df=self.getUsProperDf(dataset_id,project)


            helper=PCA_Helper(no_of_components,df)



            now = datetime.datetime.now()
            html = "<html><body>It is now %s.</body></html>" % now
            return    HttpResponse(html)

        def getUsProperDf(self,dataset_id,project):
            if dataset_id=='00000':
                return pd.read_csv(project.dataset)
            else:
                filenmae=ExtraDataset.objects.filter(id=dataset_id).first().basefilename
                return pd.read_csv("uploads/"+filenmae)

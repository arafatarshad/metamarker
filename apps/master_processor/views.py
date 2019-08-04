from apps.project_ground.models import Extradataset, PreprocessingTasks , Project,Job
from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework.views import APIView
from django.http import HttpResponse

import pandas as pd
import os
import random
# from django.conf import settings
from .lib.pca_processor import PCA_Helper

class Master(APIView):
    def __init__(self):
        if Job.objects.filter(status=1).exists()==False:
            self.nextInLine()

    def nextInLine(self):
        newjob=Job.objects.filter(status=0).first()
        newjob.status=0
        newjob.save()
        if newjob.processing_algorithm.reference_id == 'pc_001':
            pca=PCA_Helper(newjob)




        # def post(self, request, *args, **kwargs):
        #
        #
        #
        #
        #     project = Project.objects.get(reference_id=request.session['reference_id'])
        #     dataset_id =request.POST['dataset_id']
        #     no_of_components =request.POST['no_of_components']
        #     df=self.getUsProperDf(dataset_id,project)
        #
        #     helper=PCA_Helper(no_of_components,df)
        #
        #     if 'scaler_scale_check' in request.POST:
        #         helper.StandardScale()
        #
        #
        #
        #
        #
        #     now = datetime.datetime.now()
        #     html = "<html><body>It is now %s.</body></html>" % now
        #     return    HttpResponse(html)
        #

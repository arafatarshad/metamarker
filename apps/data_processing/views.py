import os
import uuid
from django.shortcuts import render
from django.shortcuts import redirect

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.forms.utils import ErrorList
from django.http import HttpResponse


from django.http import HttpResponse
from datetime import datetime


from apps.project_ground.models import Extradataset as ExtraDataset, PreprocessingTasks , Project,Job , PcaJobParameters,DaaResultAndParameter,PlsDa

import pandas as pd
import os
import random

from django.conf import settings
from .lib.lib import PCA_Helper
# Create your views here.
class PCA(APIView):

        def get(self, request, *args, **kwargs):
            project = Project.objects.get(reference_id=request.session['reference_id'])
            dataset=ExtraDataset.objects.filter(project_id=project)
            totalColumns=range(len(pd.read_csv(project.dataset).columns)-1)
            return render(request,"processing/pca/pca_processing.html",{"page_title":"PCA-processing","project":project,"dataset":dataset,"total_columns":totalColumns})

        def post(self, request, *args, **kwargs):
            self.saveTheJob(request)
            now = datetime.now()
            html = "<html><body>It is now %s.</body></html>" % now
            return    HttpResponse(html)

        def saveTheJob(self,request):
            project = Project.objects.get(reference_id=request.session['reference_id'])
            if request.POST['dataset_id'] == '00000':
                job= Job(status=0,created_at=datetime.now(),processing_algorithm_id=settings.PCA,project_id=project.id)
            else:
                job= Job(status=0,created_at=datetime.now(),processing_algorithm_id=settings.PCA,extradataset_id=request.POST['dataset_id'],project_id=project.id)
            job.save()
            pca_job=PcaJobParameters(no_of_components=request.POST['no_of_components'],reduce_to=request.POST['reduce_to'],job_id=job.id)
            pca_job.save()


class DCA(APIView):

        def get(self, request, *args, **kwargs):
            project = Project.objects.get(reference_id=request.session['reference_id'])
            dataset=ExtraDataset.objects.filter(project_id=project)
            return render(request,"processing/dca/dca_processing.html",{"page_title":"DCA-processing","project":project,"dataset":dataset})

        def post(self, request, *args, **kwargs):
            self.saveTheJob(request)
            now = datetime.now()
            html = "<html><body>It is now %s.</body></html>" % now
            return    HttpResponse(html)

        def saveTheJob(self,request):
            project = Project.objects.get(reference_id=request.session['reference_id'])
            if request.POST['dataset_id'] == '00000':
                job= Job(status=0,created_at=datetime.now(),processing_algorithm_id=settings.DCA,project_id=project.id)
            else:
                job= Job(status=0,created_at=datetime.now(),processing_algorithm_id=settings.DCA,extradataset_id=request.POST['dataset_id'],project_id=project.id)
            job.save()

            if 'scaler_scale_check' in request.POST:
                daa_job=DaaResultAndParameter(p_value_cutoff=request.POST['p_value_cutoff'],number_of_permutation=request.POST['number_of_permutation'],scaler_scale=request.POST['scaler_scale_check'],job_id=job.id)
            else:
                daa_job=DaaResultAndParameter(p_value_cutoff=request.POST['p_value_cutoff'],number_of_permutation=request.POST['number_of_permutation'],job_id=job.id)
            daa_job.save()



class PLSDA(APIView):

        def get(self, request, *args, **kwargs):
            project = Project.objects.get(reference_id=request.session['reference_id'])
            dataset=ExtraDataset.objects.filter(project_id=project)
            totalColumns=range(len(pd.read_csv(project.dataset).columns)-1)
            return render(request,"processing/pls_da/pls_da_processing.html",{"page_title":"PLSDA-processing","project":project,"dataset":dataset,"total_columns":totalColumns})

        def post(self, request, *args, **kwargs):
            self.saveTheJob(request)
            now = datetime.now()
            html = "<html><body>It is now %s.</body></html>" % now
            return    HttpResponse(html)

        def saveTheJob(self,request):
            project = Project.objects.get(reference_id=request.session['reference_id'])
            if request.POST['dataset_id'] == '00000':
                job= Job(status=0,created_at=datetime.now(),processing_algorithm_id=settings.PLS_DA,project_id=project.id)
            else:
                job= Job(status=0,created_at=datetime.now(),processing_algorithm_id=settings.PLS_DA,extradataset_id=request.POST['dataset_id'],project_id=project.id)
            job.save()

            if 'scaler_scale_check' in request.POST:
                pls_da=PlsDa(scaler_scale=request.POST['scaler_scale_check'],job_id=job.id,no_of_components=request.POST['no_of_components'],)
            else:
                pls_da=PlsDa(job_id=job.id,no_of_components=request.POST['no_of_components'],)
            pls_da.save()

            # print(request.POST)

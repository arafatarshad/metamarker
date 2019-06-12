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




import pandas as pd
# Create your views here.
class showPreprocessingIndex(APIView):

        def ProcessDataframe(self,project):

            df=pd.read_csv(project.dataset)

            missing_value_handler = MissingValueHandler()
            scaling_handler=ScalingDatasethandler()

            columns = df.columns
            missing_value_handler.fixTheColumnsDatatype(df,columns)
            scaling_handler.XVastScaliong(df)

        def get(self, request, *args, **kwargs):

            project = Project.objects.get(reference_id=request.session['reference_id'])
            dataset=ExtraDataset.objects.filter(project_id=project.id)
            preprocessing_tasks=PreprocessingTasks.objects.all()
            self.ProcessDataframe(project)
            return render(request,"preprocessing/preprocessing.html",{"page_title":"Pre-processing","project":project,
                                                                    "dataset":dataset,"preprocessing_tasks":preprocessing_tasks})

        def post(self, request, *args, **kwargs):
            now = datetime.datetime.now()
            html = "<html><body>It is now %s.</body></html>" % now
            return    HttpResponse(html)

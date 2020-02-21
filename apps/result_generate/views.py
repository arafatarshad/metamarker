# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.forms.utils import ErrorList
from django.http import HttpResponse

from apps.project_ground.models import Extradataset, PreprocessingTasks , Project,Job,DaaResultAndParameter,PcaResult

import json
from django.core import serializers

from background_task import background
from .lib.pca_result import PCAResultLIB,ComponentsResultLib
from .lib.dca_result import DCA_Result

from django.http import JsonResponse
import json


class JobResult(APIView):
        def showJobReult(request,id):
            job = Job.objects.get(pk=id)
            project=Project.objects.filter(reference_id=request.session['reference_id']).first()

            if job.processing_algorithm.reference_id == 'pc_001':
                pca_result =PCAResultLIB(PcaResult.objects.filter(job_id=id)[0])
                pie_chart=pca_result.generateThePieChart()
                pc_id=pca_result.getMeComponentsId()
                return render(request,"show_result/pca_result.html",{"page_title":"PCA-Result","project_id":project.id,"pie_chart":pie_chart,"pc_id":pc_id})

            if job.processing_algorithm.reference_id == 'pc_002':
                dca_result=DCA_Result(job)
                tables=dca_result.getMeHeatMaps()
                return render(request,"job/result/daa_result.html",{"title":"Dashboard",'table' : tables[0],'table1' : tables[1],'table2' : tables[2],'job':id})

        def getPCAComponentResult(request,id):
            figure=ComponentsResultLib().returnBarChart(id)
            # return JsonResponse(figure,safe=False)
            return HttpResponse(figure)
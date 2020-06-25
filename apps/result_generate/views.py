# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.forms.utils import ErrorList
from django.http import HttpResponse

from apps.project_ground.models import Extradataset, PreprocessingTasks , Project,Job,DaaResultAndParameter,PcaResult,PlsComponentResult,PlsDa

import json
from django.core import serializers

from background_task import background
from .lib.pca_result import PCAResultLIB,ComponentsResultLib
from .lib.dca_result import DCA_Result
from .lib.pls_da_result import PlsDaResult,PlsDaComponentResult

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
                print(id)
                dca_result=DCA_Result(job)
                tables=dca_result.getMeHeatMaps()
                # return render(request,"job/result/daa_result.html",{"title":"Dashboard",'table' : tables[0],'table1' : tables[1],'table2' : tables[2],'job':id})
                return render(request,"job/result/daa_result.html",{"title":"Dashboard",'table' : tables[0],'table1' : tables[1],'job':id})

            if job.processing_algorithm.reference_id == 'pc_003': 
                pls_da=PlsDa.objects.filter(job_id=id)[0]
                pls_da_result=PlsDaResult(pls_da)
                pls_da_components=pls_da_result.getMeComponentsId()
                vip_score_figure=PlsDaComponentResult().returnVIPBarChart(pls_da.id) 
                return render(request,"show_result/pls_result_new.html",{"vip_score_figure":vip_score_figure,"title":"Pls Da Result","pls_components":pls_da_components,'job_id':id,"pls_da_id":pls_da.id})

        def getPCAComponentResult(request,id):
            figure=ComponentsResultLib().returnBarChart(id)
            return HttpResponse(figure)
        
        def getPLSComponentResult(request):
            # return HttpResponse("hello world")
            # print(request.POST)
            component_id=PlsComponentResult.objects.filter(pls_da_id=request.POST['pls_da_id'],result_type=request.POST['result_type'],component_id=request.POST['component_id'])[0]
            component_figure=PlsDaComponentResult().returnBarChart(component_id.id)
            vip_score_figure=PlsDaComponentResult().returnVIPBarChart(request.POST['pls_da_id'])
            # return HttpResponse(vip_score_figure)

            pls_da=PlsDa.objects.filter(job_id=request.POST['job_id'])[0]
            pls_da_result=PlsDaResult(pls_da)
            pls_da_components=pls_da_result.getMeComponentsId()
            return render(request,"show_result/pls_result_new.html",{"vip_score_figure":vip_score_figure,"title":"Pls Da Result","pls_components":pls_da_components,'job_id':request.POST['job_id'],"pls_da_id":pls_da.id,"component_figure":component_figure})

        def MoreNetwork(request,id): 
            return render(request,"job/result/more_network.html",{"title":"MoreNetwork",'job_id':id})

        # def getPLSComponentResult(request,component_id,result_type,pls_id):
        #     # PlsDaComponentResultPlsComponentResult
        #     print(component_id)
        #     print(result_type)
        #     print(pls_id)
        #     component_id=PlsComponentResult.objects.filter(pls_da_id=pls_id,result_type=result_type,component_id=component_id)[0]
        #     print(component_id)
        #     figure=PlsDaComponentResult().returnBarChart(component_id.id)
        #     # return JsonResponse(figure,safe=False)
        #     return HttpResponse(figure)
        #
        #

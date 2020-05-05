# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.forms.utils import ErrorList
from django.http import HttpResponse

from apps.project_ground.models import Extradataset, PreprocessingTasks , Project,Job,DaaResultAndParameter

import json
from django.core import serializers

from background_task import background
from .email_update import email_update




from .lib.pca_processor import PCA_Helper
from .lib.dca_processor import DCA_Helper,DCA_Result
from .lib.pls_da_processor import PlsDa_Helper


from django.http import JsonResponse
import json


class JOB(APIView):
        def get(self, request, *args, **kwargs):
            project=Project.objects.filter(reference_id=request.session['reference_id']).first()
            checkBackgroundTask(repeat=60, repeat_until=None)
            return render(request,"job/job.html",{"page_title":"Task-Manager","project_id":project.id})


        def getJobData(request,id):
            job=Job.objects.filter(status__in=[0,2,3],project_id=id)
            data = []
            for single_job in job:
                query={}
                query["id"]=single_job.id
                query["name"]=single_job.name

                if single_job.status == 0:
                    query["status"]="Pending"
                elif  single_job.status == 1:
                    query["status"]="Processsing"
                elif  single_job.status == 2:
                    query["status"]="Complete"
                elif  single_job.status == 3:
                    query["status"]="Complete_and_Result_Generated"
                else:
                    query["status"]="Deleted"

                if single_job.extradataset_id==None:
                    query["dataset_name"]="Main Dataset"
                else:
                    query["dataset_name"]=single_job.extradataset.name
                query["processing_algorithm"]=single_job.processing_algorithm.name
                query["created_at"]=single_job.created_at.strftime('%d  %b , %Y - %H : %M : %S')
                data.append(query)
                # print(query)
            return HttpResponse(json.dumps(data), content_type='application/json')


        def deleteJOB(self,request,id):
            job = Job.objects.get(pk=id)
            job.status=50
            job.save()
            project=Project.objects.filter(reference_id=request.session['reference_id']).first()
            return render(request,"job/job.html",{"page_title":"Task-Manager","project_id":project.id})

        def showJobReult(self,request,id):
            job = Job.objects.get(pk=id)

            if job.processing_algorithm.reference_id == 'pc_002':
                dca_result=DCA_Result(job)
                tables=dca_result.getMeHeatMaps()
                
                return render(request,"job/result/daa_result.html",{"title":"Dashboard",'table' : tables[0],'table1' : tables[1],'job':id})
                # return render(request,"job/result/daa_result.html",{"title":"Dashboard",'table' : tables[0],'table1' : tables[1],'job':id})

            if job.processing_algorithm.reference_id == 'pc_003':
                pls_da_result=PlsDa_Helper(job)
                # tables=dca_result.getMeHeatMaps()
                # return render(request,"job/result/daa_result.html",{"title":"Dashboard",'table' : tables[0],'table1' : tables[1],'table2' : tables[2],'job':id})

            # dca=DCA_Helper(job)
            project=Project.objects.filter(reference_id=request.session['reference_id']).first()
            return render(request,"job/job.html",{"page_title":"Task-Manager","project_id":project.id})






        def getDiffCorApi(self,id):
            job = Job.objects.get(pk=id)
            dca=DaaResultAndParameter.objects.filter(job_id=job)[0]
            d = json.loads(dca.diff_cor)
            return JsonResponse(d,safe=False)


        def getSigCorApi(self,id):
            job = Job.objects.get(pk=id)
            dca=DaaResultAndParameter.objects.filter(job_id=job)[0]
            d = json.loads(dca.permute_sig_corr)
            return JsonResponse(d,safe=False)


        def getUsNetworkData(self,id):
            job = Job.objects.get(pk=id)
            dca=DaaResultAndParameter.objects.filter(job_id=job)[0]
            d = dca.network_data
            return JsonResponse(d,safe=False)



# the folowwing lines of codes are responsible for automation
def getAutomationAGo(request):
    project=Project.objects.filter(reference_id=request.session['reference_id']).first()
    checkBackgroundTask(repeat=60, repeat_until=None)
    return render(request,"job/job.html",{"page_title":"Task-Manager","project_id":project.id})

@background(queue='my-queue')
def checkBackgroundTask():
    # print("atlesat------------>")
    if Job.objects.filter(status=1).exists()==False:
        print("--------------------------------Processor ready-----------------------------")
        processNextInLine()

    if Job.objects.filter(status=2).exists()==True:
        email_update.notifyCompleteTakUser()


def processNextInLine():
    newjob=Job.objects.filter(status=0).first()

    if newjob != None:
        newjob.status=1
        newjob.save()
        if newjob.processing_algorithm.reference_id == 'pc_001':
            print("-----------------status updated from pending to complete for id --------------------"+str(newjob.id))
            pca=PCA_Helper(newjob)

        if newjob.processing_algorithm.reference_id == 'pc_002':
            print("-----------------status updated from pending to complete for id --------------------"+str(newjob.id))
            dca=DCA_Helper(newjob)

        if newjob.processing_algorithm.reference_id == 'pc_003':
            print("-----------------status updated from pending to complete for id --------------------"+str(newjob.id))
            dca=PlsDa_Helper(newjob)






























# def processNextInLine():
#     newjob=Job.objects.filter(status=0).first()
#     print("the status of the job is ")
#     print(newjob.status)
# #
#
# class Master(APIView):
#
#     def get(self, request, *args, **kwargs):
#         checkBackgroundTask(repeat=60, repeat_until=None)
#         print("inside first base")
#         return render(request,"job/job.html",{"page_title":"Task-Manager"})
#
#
#     def processNextInLine(self):
#         print("this method is working now")
#         newjob=Job.objects.filter(status=0).first()
#         newjob.status=1
#         newjob.save()
#         if newjob.processing_algorithm.reference_id == 'pc_001':
#             pca=PCA_Helper(newjob)
        # elif newjob.processing_algorithm.reference_id == 'pc_002':
        #     dca=DCA_Helper(newjob)


    # def runThisJob(self,request,id):
    #     job = Job.objects.get(pk=id)
    #     dca=DCA_Helper(job)
    #     dca.getUsCaseAndControl()
    #     return render(request,"job/job.html",{"page_title":"Task-Manager"})

    #
    #
    # def runThisJob(self,request,id):
    #     job = Job.objects.get(pk=id)
    #     job.status=50
    #     job.save()
    #     return render(request,"job/job.html",{"page_title":"Task-Manager"})

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.forms.utils import ErrorList
from django.http import HttpResponse

from apps.project_ground.models import Extradataset, PreprocessingTasks , Project,Job

import json
from django.core import serializers

from background_task import background
from .email_update import email_update




from .lib.pca_processor import PCA_Helper
from .lib.dca_processor import DCA_Helper




class JOB(APIView):
        def get(self, request, *args, **kwargs):
            return render(request,"job/job.html",{"page_title":"Task-Manager"})

        def getJobData(request,id):
            job=Job.objects.filter(status__in=[0,1,2,3])

            data = []
            for single_job in job:
                query={}
                if single_job.status == 0:
                    query["status"]="Pending"
                elif  single_job.status == 1:
                    query["status"]="Processsing"
                else:
                    query["status"]="Complete"

                query["id"]=single_job.id

                if single_job.extradataset_id==None:
                    query["dataset_name"]="Main Dataset"
                else:
                    query["dataset_name"]=single_job.extradataset.name

                query["processing_algorithm"]=single_job.processing_algorithm.name

                data.append(query)
            return HttpResponse(json.dumps(data), content_type='application/json')

        def deleteJOB(self,request,id):
            job = Job.objects.get(pk=id)
            job.status=50
            job.save()
            return render(request,"job/job.html",{"page_title":"Task-Manager"})



        def ProcessJobs(self):
            print("I am here____________")
            newjob=Job.objects.filter(status=0).first()
            email_update.tellThemProjectStarts(newjob)



        def job1(self):
        	print("inside job1")
        	self.checkBackgroundTask(repeat=10, repeat_until=None)
        	print("on the way out job one")



class Master(APIView):

    def get(self, request, *args, **kwargs):
        checkBackgroundTask(repeat=600, repeat_until=None)
        return render(request,"job/job.html",{"page_title":"Task-Manager"})

    @background(queue='my-queue')
    def checkBackgroundTask():
        if Job.objects.filter(status=1).exists()==False:
            self.processNextInLine()
        if Job.objects.filter(status=2).exists()==True:
            email_update.notifyCompleteTakUser()

    def processNextInLine(self):
        newjob=Job.objects.filter(status=0).first()
        newjob.status=1
        newjob.save()
        if newjob.processing_algorithm.reference_id == 'pc_001':
            pca=PCA_Helper(newjob)
        elif newjob.processing_algorithm.reference_id == 'pc_002':
            dca=DCA_Helper(newjob)


    def runThisJob(self,request,id):
        job = Job.objects.get(pk=id)
        dca=DCA_Helper(job)
        dca.getUsCaseAndControl()
        return render(request,"job/job.html",{"page_title":"Task-Manager"})

    #
    #
    # def runThisJob(self,request,id):
    #     job = Job.objects.get(pk=id)
    #     job.status=50
    #     job.save()
    #     return render(request,"job/job.html",{"page_title":"Task-Manager"})

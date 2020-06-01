from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework.views import APIView
from django.http import HttpResponse

import pandas as pd
import os
import random
from apps.project_ground.models import Project,Job,PcaJobParameters,ComponentResult,PcaResult,PlsComponentResult,PlsDa,DaaResultAndParameter,Extradataset
from django.conf import settings
class Settings(APIView):

    def get(self, request, *args, **kwargs):
        project = Project.objects.get(reference_id=request.session['reference_id'])
        # dataset=ExtraDataset.objects.filter(project_id=project)
        # preprocessing_tasks=PreprocessingTasks.objects.all()
        return render(request,"settings/settings.html",{"page_title":"settings","project":project})
        # return HttpResponse(project)

    def post(self, request, *args, **kwargs):
        project = Project.objects.get(reference_id=request.session['reference_id'])
        project.description=request.POST['description']
        project.author_first_name=request.POST['author_first_name']
        project.author_last_name=request.POST['author_last_name']
        # project.email=request.POST['email']
        project.save()
        # print(request.POST)
        # dataset=ExtraDataset.objects.filter(project_id=project)
        # preprocessing_tasks=PreprocessingTasks.objects.all()
        # return HttpResponse(project)
        return render(request,"settings/settings.html",{"page_title":"settings","project":project})
     
    # def deleteJobAndRelevants(self,job):
        # print(job) 
        # ComponentResult.objects.filter(id__in=[PcaResult.objects.filter(job_id=job)]).delete()
        # PcaResult.objects.filter(job_id=job).delete()
        # PcaJobParameters.objects.filter(job_id=job).delete()
 
        # PlsComponentResult.objects.filter(id__in=[PlsDa.objects.filter(job_id=job)]).delete()
        # PlsDa.objects.filter(job_id=job).delete()
         
        # DaaResultAndParameter.objects.filter(job_id=job).delete()    
    
    def deleteProject(self,request,id):
        project = Project.objects.get(id=id)
        jobs=Job.objects.filter(project=project)
        extradatasets=Extradataset.objects.filter(project_id_id=project)

        for job in jobs:
            pcaresults=PcaResult.objects.filter(job_id=job.id)
            for pcaresult in pcaresults:
                ComponentResult.objects.filter(id=pcaresult.id).delete()
        
            PcaResult.objects.filter(job_id=job.id).delete()
            PcaJobParameters.objects.filter(job_id=job.id).delete()
            
            plss=PlsDa.objects.filter(job_id=job.id)
            for pls in plss:
                PlsComponentResult.objects.filter(id=pls.id).delete()
                pls.delete() 
             
            DaaResultAndParameter.objects.filter(job_id=job.id).delete()    
                   
            job.delete()
                 
        for d in extradatasets:
            os.remove(settings.MEDIA_ROOT+"/"+d.basefilename)
            d.delete()

        project.dataset.delete() 
        project.delete()
        
        del request.session['reference_id'] 
        return redirect('/project_ground/')

        # return HttpResponse(project)


        
    # for pca in pcas:
            # pca_params     

        # if len(self.pcas) > 0:

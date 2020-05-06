import os
import uuid
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

from apps.project_ground.models import Project,Job,PcaJobParameters,DaaResultAndParameter,PlsDa
from apps.project_ground.models import Extradataset as ExtraDataset

import datetime
from sklearn import preprocessing

from django.conf import settings
import pandas as pd


# Create your views here.
class compare_result(APIView):
    def get(self, request, *args, **kwargs):
        project = Project.objects.get(reference_id=request.session['reference_id'])
        
        jobs=Job.objects.filter(project_id=project.id,status=3)
        # print(jobs[0].proce)
        # dataset=ExtraDataset.objects.filter(project_id=project)
        # preprocessing_tasks=PreprocessingTasks.objects.all()
        return render(request,"compare_result/home.html",{"page_title":"Result Compare","project":project,"jobs":jobs})
        # return    HttpResponse(project.id)
    
    def generate_panel_2(self, request, *args, **kwargs):
        job_1=Job.objects.get(id=request.POST['job1_select'])
        job_2=Job.objects.get(id=request.POST['job2_select'])
        job1_template=self.switcher(1,job_1)
        job2_template=self.switcher(2,job_2)
        return HttpResponse([job1_template,job2_template])
    
    def switcher(self,job_count,job): 
        if(job.processing_algorithm_id==settings.PCA):
            return self.generate_pca_form(job_count,PcaJobParameters.objects.get(job_id=job.id))
        elif(job.processing_algorithm_id==settings.DCA): 
            return self.generate_dca_form(job_count,DaaResultAndParameter.objects.get(job_id=job.id))
        else:
            return self.generate_pls_da_form(job_count,PlsDa.objects.get(job_id=job.id))

    def generate_pca_form(self,job_count,pca_job):
        if job_count==1: 
            part1= '<div class="box-body"><label>parameters For the First Job</label><br><div class="col-md-4"><div class="form-group"><label>Select Component</label><select class="form-control select2" style="width: 100%;" name="pca_component" id="pca_component">'
        else:
            part1= '<div class="box-body"><label>parameters For the Second Job</label><br><div class="col-md-4"><div class="form-group"><label>Select Component</label><select class="form-control select2" style="width: 100%;" name="pca_component" id="pca_component">'
            
        part_2=''
        for i in range(0,pca_job.no_of_components):
            part_2=part_2+'<option value="'+str(i)+'">Component'+str(i+1) +'</option>'
        part3='</select></div></div></div><hr>'
        part4= '<div class="box-body"><div class="col-md-12"> <div class="form-group"><label>Submit</label><button type="button" id="panel_2_submit" class="btn btn-success form-control" style="width: 100%;" onclick="go_to_third_panel()">Submit</button></div></div></div>'
        if(job_count==2):
            return part1+part_2+part3+part4
        else :
            return part1+part_2+part3




    def generate_dca_form(self,job_count,dca):
        if job_count==1: 
            part1= '<div class="box-body"><label>parameters For the First Job</label><br><div class="col-md-4"><div class="form-group"><label>Type Of Procedures</label><select class="form-control select2" style="width: 100%;" name="centrality_type" id="centrality_type">'
        else:
            part1= '<div class="box-body"><label>parameters For the Second Job</label><br><div class="col-md-4"><div class="form-group"><label>Type Of Procedures</label><select class="form-control select2" style="width: 100%;" name="centrality_type" id="centrality_type">'
            
        part_2='<option value="degree_centrality">Degree Centrality</option><option value="page-rank_centrality">Page Rank Centrality</option><option value="betweenness_centrality">Betweennes Centrality</option><option value="closeness_centrality">Closeness Centrality</option>'
                 

        part3='</select></div></div></div><hr>'
        part4= '<div class="box-body"><div class="col-md-12"> <div class="form-group"><label>Submit</label><button type="button" id="panel_2_submit" class="btn btn-success form-control" style="width: 100%;" onclick="go_to_third_panel()">Submit</button></div></div></div>'
        if(job_count==2):
            return part1+part_2+part3+part4
        else :
            return part1+part_2+part3



    def generate_pls_da_form(self,job_count,pls):
        if job_count==1: 
            part1= '<div class="box-body"><label>parameters For the First Job</label><br><div class="col-md-4"><div class="form-group"><label>Select Component</label><select class="form-control select2" style="width: 100%;" name="component_id" id="component_id">'
        else:
            part1= '<div class="box-body"><label>parameters For the Second Job</label><br><div class="col-md-4"><div class="form-group"><label>Select Component</label><select class="form-control select2" style="width: 100%;" name="component_id" id="component_id">'
            
        part_2=''
        for i in range(0,pca_job.no_of_components):
            part_2=part_2+'<option value="'+str(i)+'">Component'+str(i+1) +'</option>'
        part3='</select></div></div>'
        
        part4= '<div class="box-body"><div class="col-md-4"><div class="form-group"><label>Select Result Type</label><select class="form-control select2" style="width: 100%;" name="result_type" id="pls_result_type">'+'<option value="weight">Weight</option><option value="score">Score</option>'        

        part6='</div><hr>'
        part4= '<div class="box-body"><div class="col-md-12"> <div class="form-group"><label>Submit</label><button type="button" id="panel_2_submit" class="btn btn-success form-control" style="width: 100%;" onclick="go_to_third_panel()">Submit</button></div></div></div>'
        if(job_count==2):
            return part1+part_2+part3+part4
        else :
            return part1+part_2+part3







        # def post(self, request, *args, **kwargs):
        #     project = Project.objects.get(reference_id=request.session['reference_id'])
        #     dataset_id =request.POST['dataset_id']
        #     df=self.getUsProperDf(dataset_id,project)

        #     df=self.PreprocessDataframe(df,request)
        #     self.saveDataSet(project,request,df)
        #     now = datetime.datetime.now()
        #     html = "<html><body>It is now %s.</body></html>" % now
        #     return    HttpResponse(html)

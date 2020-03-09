from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse

import pandas as pd
import os
import random
from apps.project_ground.models import Project,Job,DaaResultAndParameter,PcaResult,PcaJobParameters,ComponentResult,PlsDa,PlsComponentResult
import json
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib import pdfencrypt




from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from django.contrib.auth.models import User
from datetime import datetime

class Main(APIView):

        def get(self, request, *args, **kwargs):
            project = Project.objects.get(reference_id=request.session['reference_id'])
            return render(request,"validate_and_report/home.html",{"page_title":"Validate And Report","project":project})

        # def post(self, request, *args, **kwargs):
        #     project = Project.objects.get(reference_id=request.session['reference_id'])
        #     return render(request,"validate_and_report/home.html",{"page_title":"Validate And Report","project":project})


        def getJobData(request,id):
            job=Job.objects.filter(status=3,project_id=id)
            data = []
            for single_job in job:
                query={}
                query["id"]=single_job.id
                if single_job.extradataset_id==None:
                    query["dataset_name"]="Main Dataset"
                else:
                    query["dataset_name"]=single_job.extradataset.name
                query["processing_algorithm"]=single_job.processing_algorithm.name
                query["created_at"]=single_job.created_at.strftime('%d  %b , %Y - %H : %M : %S')
                data.append(query)
            return HttpResponse(json.dumps(data), content_type='application/json')



class ShowResult:
    def __init__(self):
        self.name="asdas"

    def showResult(self,request,id):
        job=Job.objects.get(id=id)
        if(job.processing_algorithm.reference_id=="pc_002"):
            return render(request,"validate_and_report/download_for_dca.html",{"page_title":"Downloads","job":job})
        elif(job.processing_algorithm.reference_id=="pc_001"):
            total_component=PcaJobParameters.objects.get(job_id=id).no_of_components
            components=[]
            for i in range(total_component):
                components.append(i+1)
            pca_result_id=PcaResult.objects.get(job_id=id).id
            return render(request,"validate_and_report/download_for_pca.html",{"page_title":"Downloads","job":job,"components":components,"pca_result_id":pca_result_id})
        else:
            total_component=PlsDa.objects.get(job_id=id).no_of_components
            components=[]
            for i in range(total_component):
                components.append(i+1)
            pls_da_id=PlsDa.objects.get(job_id=id).id
            return render(request,"validate_and_report/download_for_pls.html",{"page_title":"Downloads","components":components,"pls_da_id":pls_da_id})

class downloadResultDCA:

    def dcaDownloadSelect(self,request):
        job_id=request.POST['job_id']
        dca_option=request.POST['dca_option']
        if dca_option=="network_data":
            data=DaaResultAndParameter.objects.get(job_id=job_id).network_data
            filename="network_data.json"
        elif dca_option=="init_dc":
            data=DaaResultAndParameter.objects.get(job_id=job_id).diff_cor
            filename="differential_dorrelation.json"
        elif dca_option=="final_dc":
            data=DaaResultAndParameter.objects.get(job_id=job_id).permute_diff_cor
            filename="permute_diff_cor.json"
        else:
            data=DaaResultAndParameter.objects.get(job_id=job_id).permute_sig_corr
            filename="permute_sig_cor.json"
        response = HttpResponse(data, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename='+filename
        return response

class downloadResultPCA:

    def pcaDownloadSelect(self,request):
        job_id=request.POST['job_id']
        pca_result_id=request.POST['pca_result_id']
        component_id=int(request.POST['component_id'])-1

        filename="component"+str(component_id+1)+".json"
        # print(component_id)
        data=ComponentResult.objects.get(pca_result_id=pca_result_id,component_id=component_id).result
        response = HttpResponse(data, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename='+filename
        return response

class downloadResultPLS:

    def plsDownloadSelect(self,request):
        pls_da_id=request.POST['pls_da_id']
        component_id=int(request.POST['component_id'])-1
        result_type=int(request.POST['result_type'])
        # print(pls_da_id)
        # print(component_id)
        # print(result_type)
        filename="component"+str(component_id+1)+".json"
        data=PlsComponentResult.objects.filter(pls_da_id=pls_da_id,component_id=component_id,result_type=result_type)[0].result
        # print(data[0])
        response = HttpResponse(data, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename='+filename
        return response
        # return HttpResponse("sad")




    #
    #
    #     filename = self.getMeFilename(id)
    #     # report=Report(created_at=datetime.now(),name=filename,delete=0,job_id=id).save()
    #
    #     response = HttpResponse(content_type='application/pdf')
    #     response['Content-Disposition'] = "'attachment; filename='"+filename
    #
    #     buffer = BytesIO()
    #     p = canvas.Canvas(buffer)
    #
    #
    #     p.drawString(100, 100, "Hello world.")
    #
    #
    #
    #
    #
    #     p.showPage()
    #     p.save()
    #     pdf = buffer.getvalue()
    #     buffer.close()
    #     response.write(pdf)
    #     return response
    # #
    # # def findOutWhichReport(id,canvas):
    # #     job=Job.objects.get(id=id)
    # #     if(job.processing_algorithm.reference_id=="pc_002"):
    # #         self.generateDCAPDF(id,canvas)
    #
    # def getMeFilename(self,reference_id):
    #     job=Job.objects.get(id=reference_id)
    #     project=Project.objects.get(id=job.project_id)
    #
    #     dateTimeObj = datetime.now()
    #     timeObj = dateTimeObj.time()
    #     timeStr = timeObj.strftime("%H:%M:%S.%f")
    #     filename=str(project.reference_id)+str(dateTimeObj.year)+str(dateTimeObj.month)+str(dateTimeObj.day)+str(dateTimeObj.hour)+str(dateTimeObj.minute)+str(dateTimeObj.second)+str(dateTimeObj.microsecond)+".pdf"
    #     # filename=str(project.reference_id)+str(timeStr)
    #     # filename=str(reference_id)+str(timeStr)
    #     return filename
    #
    # # def generateDCAPDF(self,id,canvas)

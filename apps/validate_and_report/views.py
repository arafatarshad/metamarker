from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse

import pandas as pd
import os
import random
from apps.project_ground.models import Project,Job,Report
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
            # dataset=ExtraDataset.objects.filter(project_id=project)
            # preprocessing_tasks=PreprocessingTasks.objects.all()
            return render(request,"validate_and_report/home.html",{"page_title":"Validate And Report","project":project})
            # return HttpResponse(project)

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
        filename = self.getMeFilename(id)
        # report=Report(created_at=datetime.now(),name=filename,delete=0,job_id=id).save()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = "'attachment; filename='"+filename

        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 100, "Hello world.")
        p.showPage()
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
        # project = Project.objects.get(reference_id=request.session['reference_id'])
        # dataset=ExtraDataset.objects.filter(project_id=project)
        # preprocessing_tasks=PreprocessingTasks.objects.all()
        # return render(request,"validate_and_report/home.html",{"page_title":"Validate And Report","project":project})

    def getMeFilename(self,reference_id):
        job=Job.objects.get(id=reference_id)
        # print(job.id)

        project=Project.objects.get(id=job.project_id)

        dateTimeObj = datetime.now()
        timeObj = dateTimeObj.time()
        timeStr = timeObj.strftime("%H:%M:%S.%f")
        filename=str(project.reference_id)+str(dateTimeObj.year)+str(dateTimeObj.month)+str(dateTimeObj.day)+str(dateTimeObj.hour)+str(dateTimeObj.minute)+str(dateTimeObj.second)+str(dateTimeObj.microsecond)+".pdf"
        # filename=str(project.reference_id)+str(timeStr)
        # filename=str(reference_id)+str(timeStr)
        return filename
        # response.write(pdf)
        # return response

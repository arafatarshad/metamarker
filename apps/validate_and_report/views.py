from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse

import pandas as pd
import os
import random
from apps.project_ground.models import Project,Job
import json
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib import pdfencrypt




from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from django.contrib.auth.models import User
import uuid

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


        def showResult(self, id):
            response = HttpResponse(content_type='application/pdf')
            filename = '%s%s' % ("demopdf", uuid.uuid4())
            response['Content-Disposition'] = "'attachment; filename='"+filename+".pdf"
            buffer = BytesIO()
            p = canvas.Canvas(buffer)
            p.drawString(100, 100, "Hello world.")
            p.showPage()
            p.save()
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            return response

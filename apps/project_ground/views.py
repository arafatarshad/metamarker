import os
import uuid
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import DatasetType
from .models import Project
from .forms import ProjectForm

from django.forms.utils import ErrorList

from django.http import HttpResponse

# Create your views here.
class StartProject(APIView):
        def get(self, request, *args, **kwargs):
            return render(request,"project_ground/start.html",{"page_title":"Start Project"})


class CreateOrSelectProject(APIView):

        def get(self, request, *args, **kwargs):
            print(kwargs.get('value'))
            if kwargs.get('value') == 0 :
                template_name = "project_ground/create_project.html"
                return render(request,template_name,{"page_title":"Create New Project","dataset_types":DatasetType.objects.all()})
            else :
                template_name = "project_ground/select_project.html"
                return render(request,template_name,{"page_title":"Select Existing Project"})


        def post(self, request, *args, **kwargs):
            if 'select' in request.POST:
                form = request.POST
                reference = request.POST['project_reference']
                email = request.POST['email']
                project  = Project.objects.filter(reference_id=reference).filter(email=email).first()

                if project !=None :
                    print(project.reference_id)
                    template_name = "project_ground/dashboard/dashboard.html"
                    return render(request,template_name,{"page_title":"Select Existing Project","project":project,})
                else :
                    template_name = "errors/project_not_found.html"
                    return render(request,template_name,{"page_title":"Project not found"})

            else :
                form = ProjectForm(request.POST,  request.FILES)
                new_project=form.save(commit=False)
                new_project.dataset_type_id_id=request.POST['dataset_type_id']
                new_project.save() 

                template_name = "project_ground/dashboard/dashboard.html"
                return render(request,template_name,{"page_title":"Select Existing Project","project":new_project})

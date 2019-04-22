import os
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import DatasetType
from .models import Project
from .forms import ProjectForm


from django.http import HttpResponse

# Create your views here.


class CreateProject(APIView):

        def get(self, request, *args, **kwargs):
            form = ProjectForm()
            return render(request,"project_ground/create_project.html",{"page_title":"Create New Project",
                                                                        "dataset_types":DatasetType.objects.all(),
                                                                        "form":form})

        def post(self, request, *args, **kwargs):
            form = ProjectForm(request.POST,  request.FILES)
            if form.is_valid():
                new_project=form.save(commit=False)
                new_project.dataset_type_id_id=request.POST['dataset_type_id']
                new_project.save()
                print(new_project.dataset_type_id)

                template_name = 'project_ground/project_entry.html'

                return render(request, template_name, {new_project:new_project})
            else :
                return render(request,"project_ground/create_project.html",{"page_title":"Create New Project",
                                                                        "dataset_types":DatasetType.objects.all(),
                                                                        "form":form})

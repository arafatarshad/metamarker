from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import DatasetType
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
                html = "<html><body>It is now %s.</body></html>"
                return HttpResponse(html)
            else :
                return render(request,"project_ground/temp.html",{"page_title":"Create New Project",
                                                                        "dataset_types":DatasetType.objects.all(),
                                                                        "form":form})

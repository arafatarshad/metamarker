from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework.views import APIView
from django.http import HttpResponse

import pandas as pd
import os
import random
from apps.project_ground.models import Project
class Settings(APIView):

        def get(self, request, *args, **kwargs):
            project = Project.objects.get(reference_id=request.session['reference_id'])
            # dataset=ExtraDataset.objects.filter(project_id=project)
            # preprocessing_tasks=PreprocessingTasks.objects.all()
            # return render(request,"settings/settings.html",{"page_title":"settings"})
            return HttpResponse(project)

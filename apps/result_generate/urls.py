
from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
path('show_job_result/<int:id>/',views.JobResult.showJobReult,name="resultOfJob"),


]

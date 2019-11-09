from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path('',views.JOB.as_view(),name="job"),
    # path('api/jobs',views.JOB().as_view({'post': 'getJobData'}),name="alljob")
    path('api/jobs',views.JOB().getJobData,name="alljob"),
    # path('delete/<id>/',views.JOB().deleteJOB,name="deleteSinglejob"),
    path('test/<int:id>/',views.JOB().deleteJOB,name="deleteSinglejob"),
    # path('/automate_the_job_cycle',views.Master.as_view(),name="automate"),
    path('checkon/',views.Master.as_view(),name="lijani"),

    path('run_this_job/<int:id>/',views.Master().runThisJob,name="run_this_job"),

    # path('check_dca/<int:id>/',views.Master.runThisJob(),name="run_this_job"),





]

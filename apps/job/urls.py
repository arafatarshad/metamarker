from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path('',views.JOB.as_view(),name="job"),
    path('delete/<id>/',views.JOB().deleteJOB,name="deleteSinglejob"),
    path('showJobReult/<int:id>/',views.JOB().showJobReult,name="showJobReult"),
    path('api/all_jobs/<int:id>/',views.JOB.getJobData,name="alljob_with_parameter"),



    path('api/get_diff_cor/<int:id>/',views.JOB.getDiffCorApi,name="api_get_diff_cor"),
    path('api/get_sig_cor/<int:id>/',views.JOB.getSigCorApi,name="api_get_sig_cor"),
    path('api/get_network_data/<int:id>/',views.JOB.getUsNetworkData,name="api_network_data"),






    # path('api/jobs',views.JOB().as_view({'post': 'getJobData'}),name="alljob")



    # path('test/<int:id>/',views.JOB()   .deleteJOB,name="deleteSinglejob"),


    # path('api/jobs/',views.JOB().getJobData,name="alljob"),



    # path('checkon/',views.getAutomationAGo,name="lijani"),


    # path('checkon/',views.Master.as_view(),name="lijani"),

    # path('checkon/',views.JOB().manualAutomation,name="lijani"),
#
    # path('check_dca/<int:id>/',views.Master.runThisJob(),name="run_this_job"),


    # path('run_this_job/<int:id>/',views.Master().runThisJob,name="run_this_job"),
    # path('/automate_the_job_cycle/',views.Master.as_view(),name="automate"),


]

from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path('',views.JOB.as_view(),name="job"),
    # path('api/jobs',views.JOB().as_view({'post': 'getJobData'}),name="alljob")
    path('api/jobs',views.JOB().getJobData,name="alljob"),
    # path('delete/<id>/',views.JOB().deleteJOB,name="deleteSinglejob"),
    path('test/<int:id>/',views.JOB().deleteJOB,name="deleteSinglejob"),

    path('showJobReult/<int:id>/',views.JOB().showJobReult,name="showJobReult"),
    # path('/automate_the_job_cycle',views.Master.as_view(),name="automate"),
    path('checkon/',views.Master.as_view(),name="lijani"),





    path('run_this_job/<int:id>/',views.Master().runThisJob,name="run_this_job"),
    path('api/get_diff_cor/<int:id>/',views.JOB.getDiffCorApi,name="api_get_diff_cor"),
    path('api/get_sig_cor/<int:id>/',views.JOB.getSigCorApi,name="api_get_sig_cor"),



    path('api/get_network_data/<int:id>/',views.JOB.getUsNetworkData,name="api_network_data"),

    # path('check_dca/<int:id>/',views.Master.runThisJob(),name="run_this_job"),

     # url(r'^api/diff_cor$', views.parallelPlot.as_view(),name="api_parallel_plot"),





]

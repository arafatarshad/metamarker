
from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
path('show_job_result/<int:id>/',views.JobResult.showJobReult,name="resultOfJob"),
path('show_job_result/network_options/daa/<int:id>/',views.JobResult.MoreNetwork,name="more_networks_options"),


path('get_component_result/<int:id>/',views.JobResult.getPCAComponentResult,name="get_component_result"),

# path('get_pls_component_result/<int:component_id>/<int:result_type>/<int:pls_id>/',views.JobResult.getPLSComponentResult,name="get_pls_component_result"),
path('pls_component_result_generator/',views.JobResult.getPLSComponentResult,name="get_pls_component_result"),


]

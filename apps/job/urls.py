from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path('',views.JOB.as_view(),name="job"),
    # path('api/jobs',views.JOB().as_view({'post': 'getJobData'}),name="alljob")
    path('api/jobs',views.JOB().getJobData,name="alljob"),
    # path('delete/<id>/',views.JOB().deleteJOB,name="deleteSinglejob"),
    path('test/<int:id>/',views.JOB().deleteJOB,name="deleteSinglejob")
]

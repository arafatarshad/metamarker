from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path('',views.showDashBoard.as_view(),name="dashboard"), 
     url(r'^api/parallel_plot$', views.parallelPlot.as_view(),name="api_parallel_plot"),
]

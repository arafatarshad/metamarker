
from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
path('',views.compare_result.as_view(),name="compare_result"),
# path('generate_panel_2/<int:id>/<int:id2>/',views.compare_result().generate_panel_2,name="generate_panel_2"),
path('generate_panel_2/',views.compare_result().generate_panel_2,name="generate_panel_2"),

 

]

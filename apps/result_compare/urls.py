
from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
path('',views.compare_result.as_view(),name="compare_result"),

 

]

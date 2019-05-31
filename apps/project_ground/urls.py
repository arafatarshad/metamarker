from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path('',views.StartProject.as_view(),name="start_project"),
    path('create/<int:value>/',views.CreateOrSelectProject.as_view(),name="create_project")
]

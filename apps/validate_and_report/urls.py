"""Metamarker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.views import generic
from django.conf.urls import url,include

from . import views
# from apps.job.views import hello

urlpatterns = [
    path('',views.Main.as_view(),name="validate_and_report"),
    path('showResult/<int:id>/',views.ShowResult().showResult,name="download_report_result"),
    path('api/alljob_with_validation/<int:id>/',views.Main.getJobData,name="alljob_with_validation"),
]

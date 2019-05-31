from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path('',views.showDashBoard.as_view(),name="dashboard")
]

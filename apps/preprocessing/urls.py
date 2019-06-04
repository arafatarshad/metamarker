from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path('',views.showPreprocessingIndex.as_view(),name="preprocessing")

]

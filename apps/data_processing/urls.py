from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path('pca',views.PCA.as_view(),name="pca_processing")

]

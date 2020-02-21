from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path('pca',views.PCA.as_view(),name="pca_processing"),
    path('dca',views.DCA.as_view(),name="dca_processing"),
    path('pls_da',views.PLSDA.as_view(),name="pls_da_processing"),


]

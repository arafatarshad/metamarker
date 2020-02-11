import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import pandas as pd


import json
from django.core import serializers

from io import BytesIO
import base64
import math
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from apps.project_ground.models import Extradataset, PreprocessingTasks , Project,Job,PcaJobParameters,PcaResult, ComponentResult


import plotly.offline as opy
import plotly.graph_objs as go
import plotly.figure_factory as ff


class PCAResultLIB:
    pca=None
    def __init__(self,pca):
        self.pca=pca
    def getMeComponentsId(self):
        components=ComponentResult.objects.filter(pca_result_id=self.pca.id)
        components_id=[]
        iterator=1
        for com in components:
            name="PC_"+(str)(iterator)
            components_id.append({'id':com.id,'name':name})
            iterator=iterator+1
        components_id
        return components_id

    def generateThePieChart(self):
        labels=[]
        values=[]
        pcas= json.loads(self.pca.variance_explained)
        for key in pcas:
            labels.append(key)
            values.append(pcas[key])
        figure = go.Figure(data=[go.Pie(labels=labels, values=values)])
        return  opy.plot(figure, auto_open=False, output_type='div')




class ComponentsResultLib:

    def returnBarChart(self,id):
        com_result=json.loads(ComponentResult.objects.filter(id=id)[0].result)
        labels=[]
        values=[]
        # print(com_result)
        for key in com_result:
            labels.append(key)
            values.append(com_result[key])
        figure = go.Figure(data=[go.Bar(x=labels, y=values)])
        return  opy.plot(figure, auto_open=False, output_type='div')

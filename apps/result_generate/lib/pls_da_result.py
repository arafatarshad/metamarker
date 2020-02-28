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
from apps.project_ground.models import Job,PlsDa,PlsComponentResult


import plotly.offline as opy
import plotly.graph_objs as go
import plotly.figure_factory as ff


class PlsDaResult:
    pls_da=None

    def __init__(self,pls_da):
        self.pls_da=pls_da

    def getMeComponentsId(self):
        components_id=[]
        iterator=1
        for com in range(self.pls_da.no_of_components):
            name="PC_"+(str)(iterator)
            components_id.append({'id':com,'name':name})
            iterator=iterator+1
        # print(components_id)
        return components_id

class PlsDaComponentResult:
    def returnBarChart(self,id):
        com_result=json.loads(PlsComponentResult.objects.filter(id=id)[0].result)
        labels=[]
        values=[]
        # print(com_result)
        for key in com_result:
            labels.append(key['id'])
            values.append(key['value'])
        figure = go.Figure(data=[go.Bar(x=labels, y=values)])
        return  opy.plot(figure, auto_open=False, output_type='div')

    def returnVIPBarChart(self,id):
        com_result=json.loads(PlsComponentResult.objects.filter(pls_da_id=id)[0].result)
        labels=[]
        values=[]
        # print(com_result)
        for key in com_result:
            labels.append(key['id'])
            values.append(key['value'])
        figure = go.Figure(data=[go.Bar(x=labels, y=values)])
        return  opy.plot(figure, auto_open=False, output_type='div')

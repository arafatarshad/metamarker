import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.decomposition import PCA
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

import json
from django.core import serializers

from io import BytesIO
import base64
import math
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from apps.project_ground.models import Extradataset,DaaResultAndParameter
import random
import plotly.offline as opy
import plotly.graph_objs as go
import plotly.figure_factory as ff



class DCA_Result:
    job=None
    dca=None

    def __init__(self,job):
        self.job=job
        self.dca=DaaResultAndParameter.objects.filter(job_id=self.job.id)[0]

    def TableCellsOnly(self,df):
        column_list=[]
        cell_list=[]

        column_list=list(df.columns)
        for value in column_list:
            cell_list.append(df[value])
        return [column_list,cell_list]


    def getMeHeatMaps(self):
        diff_cor=pd.read_json(self.dca.diff_cor)
        permute_diff_cor=pd.read_json(self.dca.permute_diff_cor)
        permute_sig_corr=pd.read_json(self.dca.permute_sig_corr)

        cell_column1=self.TableCellsOnly(diff_cor)
        cell_column2=self.TableCellsOnly(permute_diff_cor)
        cell_column3=self.TableCellsOnly(permute_sig_corr)

        trace1= go.Heatmap(
            x=cell_column1[0],
            y=cell_column1[0],
            z=cell_column1[1]
            )
        data1=[trace1]

        trace2= go.Heatmap(
            x=cell_column2[0],
            y=cell_column2[0],
            z=cell_column2[1]
            )
        data2=[trace2]
        trace3= go.Heatmap(
            x=cell_column3[0],
            y=cell_column3[0],
            z=cell_column3[1]
            )
        data3=[trace3]


        layout = None
        width= len(diff_cor.columns) * 20
        height= len(diff_cor.columns) * 20
        # if len(diff_cor.columns) > 50 :
        #     layout=go.Layout(title="Your Uploaded DataSet", width=width,height=height)
        # else :
        #     layout=go.Layout(title="Your Uploaded DataSet")
        layout1=go.Layout(title="Correlation Matrix", width=width,height=height)
        layout2=go.Layout(title="1000 Fold Permutaed Correlation Matrix", width=width,height=height)
        layout3=go.Layout(title="Significance Matrix", width=width,height=height)
        figure1=go.Figure(data=data1,layout=layout1)
        figure2=go.Figure(data=data2,layout=layout2)
        figure3=go.Figure(data=data3,layout=layout3)
        div1=opy.plot(figure1, auto_open=False, output_type='div')
        div2=opy.plot(figure2, auto_open=False, output_type='div')
        div3=opy.plot(figure3, auto_open=False, output_type='div')

        return [div1,div2,div3]




            # def getMeDiffCorTable(self):
            #     diff_cor=pd.read_json(self.dca.diff_cor)
            #     cell_column=self.TableCellsOnly(diff_cor)
            #
            #     trace= go.Table(
            #         header = dict(values=cell_column[0],fill=dict(color='#C2D4FF'),font=dict(size=10),align="left"),
            #         cells = dict(values=cell_column[1],fill=dict(color='#F5F8FF'),align="left")
            #         )
            #     data=[trace]
            #     layout = None
            #
            #     if len(diff_cor.columns) > 50 :
            #         layout=go.Layout(title="Your Uploaded DataSet", width=12500,height=750)
            #     else :
            #         layout=go.Layout(title="Your Uploaded DataSet", height=750)
            #
            #     figure=go.Figure(data=data,layout=layout)
            #     return  opy.plot(figure, auto_open=False, output_type='div')

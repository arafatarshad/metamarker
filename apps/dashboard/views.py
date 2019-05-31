from django.shortcuts import render
from rest_framework.views import APIView

import scipy
import plotly.offline as opy
import plotly.graph_objs as go
import plotly.figure_factory as ff

import pandas as pd
import dash_core_components as dcc
import dash_html_components as dht
import dash_table_experiments as dt
import dash.dependencies
from dash.dependencies import Input, Output, State
import plotly
import random

import numpy as np
from apps.project_ground.models import Project as Project

class showDashBoard(APIView):

    def hex_code_colors(self):
        a = hex(random.randrange(0,256))
        b = hex(random.randrange(0,256))
        c = hex(random.randrange(0,256))
        a = a[2:]
        b = b[2:]
        c = c[2:]
        if len(a)<2:
            a = "0" + a
        if len(b)<2:
            b = "0" + b
        if len(c)<2:
            c = "0" + c
        z = a + b + c
        return "#" + z.upper()

    def generate_hex_codes(self,length):
        color_codes=[]
        while len(color_codes) != length:
            color= self.hex_code_colors()
            if color not in color_codes:
                color_codes.append(color)
        return color_codes


    def getMeDataFrame(self,project):
        return pd.read_csv(project.dataset)

    def getMeListOfCells(self,df):
        cell_list=[]
        for value in list(df.columns):
            cell_list.append(df[value])
        return cell_list


    def getMeColorCode(self,column_data):
        uniq_list=column_data.unique()
        color_codes= self.generate_hex_codes(len(uniq_list))
        colorscale=[]
        i = 0
        for x in uniq_list:
            temp=[]
            temp.append(x)
            temp.append(color_codes[i])
            colorscale.append(temp)
            i=i+1
        return colorscale


    def getMeTheTable(self,df):


        cell_list=self.getMeListOfCells(df)
        trace= go.Table(
            header = dict(values=list(df.columns),fill=dict(color='#C2D4FF'),  height = 40),
            cells = dict(values=cell_list,fill=dict(color='#F5F8FF'),  height = 30)
            )
        data=[trace]

        layout = None

        if len(df.columns) > 35 :
            layout=go.Layout(title="Your Uploaded DataSet", width=15000,height=750)
        else :
             layout=go.Layout(title="Your Uploaded DataSet", height=750)

        figure=go.Figure(data=data,layout=layout)
        return  opy.plot(figure, auto_open=False, output_type='div')






    def getMetheParallelPlot(self,df1):

        colorscale=self.getMeColorCode(df1[df1.columns[-1]])
        print(colorscale)
        dimension_list=list()

        for value in list(df1.columns):
            dimension_list.append(dict(label = value , values = df1[value]))

        trace=go.Parcoords(
            # line = dict(color = df1[df1.columns[-1]],colorscale = colorscale,showscale = True,reversescale = True,cmin = -4000,cmax = -100),dimensions=dimension_list)
            line = dict(color = df1[df1.columns[-1]],cmin = -4000,cmax = -100),dimensions=dimension_list)
        data=[trace]
        layout = go.Layout(plot_bgcolor = '#E5E5E5',paper_bgcolor = '#E5E5E5',dragmode = 'zoom')

        if len(df1.columns) > 35 :
            layout = go.Layout(plot_bgcolor = '#E5E5E5',paper_bgcolor = '#E5E5E5',dragmode = 'zoom',width=8000)
        else :
             layout = go.Layout(plot_bgcolor = '#E5E5E5',paper_bgcolor = '#E5E5E5',dragmode = 'zoom')

        figure=go.Figure(data=data,layout=layout)
        return opy.plot(figure, auto_open=False, output_type='div')










    def get(self, request, *args, **kwargs):
        project = Project.objects.get(reference_id=request.session['reference_id'])
        df= self.getMeDataFrame(project)
        div =self.getMeTheTable(df)
        div1=self.getMetheParallelPlot(df)
        return render(request,"dashboard/dashboard.html",{"title":"Dashboard",'table' : div,'graph':div1})

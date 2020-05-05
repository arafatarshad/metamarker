from django.shortcuts import render
from rest_framework.views import APIView

from django.http import JsonResponse
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
import pandas as pd
from apps.project_ground.models import Project as Project

class showDashBoard(APIView):
    def getMeDataFrame(self,project):
        return pd.read_csv(project.dataset)

    def getMeListOfCells(self,df):
        cell_list=[]
        for value in list(df.columns):
            cell_list.append(df[value])
        return cell_list


    #
    # def hex_code_colors(self):
    #     a = hex(random.randrange(0,256))
    #     b = hex(random.randrange(0,256))
    #     c = hex(random.randrange(0,256))
    #     a = a[2:]
    #     b = b[2:]
    #     c = c[2:]
    #     if len(a)<2:
    #         a = "0" + a
    #     if len(b)<2:
    #         b = "0" + b
    #     if len(c)<2:
    #         c = "0" + c
    #     z = a + b + c
    #     return "#" + z.upper()
    #
    # def generate_hex_codes(self,length):
    #     color_codes=[]
    #     while len(color_codes) != length:
    #         color= self.hex_code_colors()
    #         if color not in color_codes:
    #             color_codes.append(color)
    #     return color_codes
    #
    #


    #
    #
    # def getMeColorCode(self,column_data):
    #     uniq_list=column_data.unique()
    #     # color_codes= self.generate_hex_codes(len(uniq_list))
    #     # color_codes= self.generate_hex_codes(len(uniq_list))
    #     # print(self.generateRGB())
    #
    #     colorscale=[]
    #     i = 0
    #     for x in uniq_list:
    #         temp=[]
    #         temp.append(x)
    #         # temp.append(color_codes[i])
    #         temp.append(self.generateRGB())
    #         colorscale.append(temp)
    #         i=i+1
    #     return colorscale

    def numericTableCellsOnly(self,df):
        column_list=[]
        cell_list=[]
        all_columns=list(df.columns)
        if len(all_columns)>50:
            column_list=all_columns[:50]
        else:
            column_list=all_columns

        for value in column_list:
            cell_list.append(df[value])
        return [column_list,cell_list]

    def getMeTheTable(self,df):
        # cell_list=self.getMeListOfCells(df)
        df=df._get_numeric_data()
        cell_column=self.numericTableCellsOnly(df)
        trace= go.Table(
            header = dict(values=cell_column[0],fill=dict(color='#C2D4FF'),font=dict(size=10),align="left"),
            cells = dict(values=cell_column[1],fill=dict(color='#F5F8FF'),align="left")
            )
        data=[trace]
        layout = None

        if len(df.columns) > 50 :
            layout=go.Layout(title="Your Uploaded DataSet", width=2500,height=750)
        else :
            layout=go.Layout(title="Your Uploaded DataSet", height=750)

        figure=go.Figure(data=data,layout=layout)
        return  opy.plot(figure, auto_open=False, output_type='div')



    def descriptionTableValues(self,df):
        column_list=["No",'Name Of Column','Value Type','Missing Value']
        names=[]
        value_types=[]
        missing_value=[]
        counter_array=[]
        counter=0
        for name in list(df.columns):
            counter=counter+1
            counter_array.append(counter)
            names.append(name)
            value_types.append(str(df[name].dtype))
            missing_value_percent=(df[name].isnull().sum().sum()/len(df[name]))*100
            if missing_value_percent==0:
                missing_value.append(str(0)+"  %")
            else:
                missing_value.append("{0:.4f}".format(missing_value_percent)+" %")
        cell_list=[counter_array,names,value_types,missing_value]
        return [column_list,cell_list]


    def descriptionTable(self,df):
        cell_column=self.descriptionTableValues(df)
        trace= go.Table(
            header = dict(values=cell_column[0],fill=dict(color='#C2D4FF'),font=dict(size=10),align="left"),
            cells = dict(values=cell_column[1],fill=dict(color='#F5F8FF'),align="left")
            )
        data=[trace]
        layout = go.Layout(title="Observations about the dataset", height=750)
        figure=go.Figure(data=data,layout=layout)
        return  opy.plot(figure, auto_open=False, output_type='div')

    def generateRGB(self):
        colors= list(np.random.choice(range(256), size=3))
        return "rgb"+"("+str(colors[0])+","+str(colors[1])+","+str(colors[2])+")"


    def proper_color_scale(self,last_column_values):
        # uniq_list=list.sort(last_column_values.unique())
        uniq_list=np.sort(last_column_values.unique())
        colorscale=[]
        for value in uniq_list:
            temp =[]
            temp.append(value)
            temp.append(self.generateRGB())
            colorscale.append(temp)

        return colorscale


    def plot_the_table(self,df1,colorscale=None):
        dimension_list=list()
        trace=None
        # print(colorscale)
        colorscale=[# Let first 10% (0.1) of the values have color rgb(0, 0, 0)
        [0, "rgb(223, 169, 102)"],
        [0.1, "rgb(223, 169, 102)"],

        # Let values between 10-20% of the min and max of z
        # have color rgb(20, 20, 20)
        [0.1, "rgb(147, 133, 64)"],
        [0.2, "rgb(147, 133, 64)"],

        # Values between 20-30% of the min and max of z
        # have color rgb(40, 40, 40)
        [0.2, "rgb(20, 17, 177)"],
        [0.3, "rgb(20, 17, 177)"],

        [0.3, "rgb(160, 17, 2)"],
        [0.4, "rgb(160, 17, 2)"],

        [0.4, "rgb(80, 80, 80)"],
        [0.5, "rgb(80, 80, 80)"],

        [0.5, "rgb(100, 100, 100)"],
        [0.6, "rgb(100, 100, 100)"],

        [0.6, "rgb(120, 120, 120)"],
        [0.7, "rgb(120, 120, 120)"],

        [0.7, "rgb(140, 140, 140)"],
        [0.8, "rgb(140, 140, 140)"],

        [0.8, "rgb(160, 160, 160)"],
        [0.9, "rgb(160, 160, 160)"],

        [0.9, "rgb(180, 180, 180)"],
        [1.0, "rgb(180, 180, 180)"]]
        for value in df1.columns:
            dimension_list.append(dict(label = value , values = df1[value]))
            if colorscale ==None:
                trace=go.Parcoords(line = dict(color = df1[df1.columns[-1]]),dimensions=dimension_list)
            else:
                trace=go.Parcoords(line = dict(color = df1[df1.columns[-1]],colorscale=colorscale),dimensions=dimension_list)

        data=[trace]
        layout =None

        if len(df1.columns) > 35 :
            layout = go.Layout(plot_bgcolor = '#E5E5E5',paper_bgcolor = '#E5E5E5',dragmode = 'zoom',width=8000,height=1000)
        else :
             layout = go.Layout(plot_bgcolor = '#E5E5E5',paper_bgcolor = '#E5E5E5',dragmode = 'zoom',height=1000)

        return go.Figure(data=data,layout=layout)

    def getMetheParallelPlot(self,df1):

        last_column_values=df1[df1.columns[-1]]
        data=None
        figure=None
        if last_column_values.dtype.kind in 'bifc':
            colorscale=self.proper_color_scale(last_column_values)
            figure=self.plot_the_table(df1,colorscale)
        else:
            figure=self.plot_the_table(df1)
        return opy.plot(figure, auto_open=False, output_type='div')



    def get(self, request, *args, **kwargs):
        project = Project.objects.get(reference_id=request.session['reference_id'])
        df= self.getMeDataFrame(project)
        div =self.getMeTheTable(df)
        div1=self.getMetheParallelPlot(df)
        div2=self.descriptionTable(df)
        return render(request,"dashboard/dashboard.html",{"title":"Dashboard",'table' : div,'graph':div1,'description':div2})







class parallelPlot(APIView):
    def getMeDataFrame(self,project):
        return pd.read_csv(project.dataset)

    def get(self, request, *args, **kwargs):
            project = Project.objects.get(reference_id=request.session['reference_id'])
            # print(project)
            df=self.getMeDataFrame(project)
            df=df._get_numeric_data()
            df.fillna(df.mean(),inplace=True)
            df=df.sample(frac =.3)
            return JsonResponse(df.to_json(orient='records'),safe=False)

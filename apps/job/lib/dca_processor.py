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
from apps.project_ground.models import Extradataset, PreprocessingTasks , Project,Job,PcaJobParameters,PcaResult, ComponentResult,DaaResultAndParameter
import random
import plotly.offline as opy
import plotly.graph_objs as go
import plotly.figure_factory as ff


class DCA_Helper:
    df=None
    features=None
    target=None
    job=None
    case=None
    control=None
    caseCopy=None
    controlCopy=None
    unique_values=None
    m=0
    n=0
    n1=0
    n2=0
    daa=None
    caseCorelation =None
    controlCorelation=None
    diffCorelation=None
    caseCorelationCopy=None
    controlCorelationCopy=None
    diffCorelationCopy=None
    count_permuteSig=None

    # p_value=0.05
    # sig_count=50

    p_value=0.05
    sig_count=50
    number_of_permutation=1000
    def __init__(self,job):
        self.job=job
        self.daa=DaaResultAndParameter.objects.filter(job_id=self.job.id)[0]
        self.df=self.getUsProperDf(job)._get_numeric_data()

        # the following line may needs to be commented
        # self.df=self.df.replace(to_replace=[None], value=np.nan, inplace=True)

        self.features=list(self.df.columns.values)
        self.target=self.features[-1]
        self.features.remove(self.target)
        # self.sig_count=self.daa.sig_count
        self.p_value=self.daa.p_value_cutoff
        self.number_of_permutation=self.daa.number_of_permutation
        self.sig_count=self.daa.p_value_cutoff*self.daa.number_of_permutation
        self.getUsCaseAndControl()


    def getUsCaseAndControl(self):
        self.job.status=1
        self.job.save()  
        self.unique_labels=self.df[self.target].unique()
        case,control = [x for _, x in self.df.groupby(self.df[self.target] ==self.unique_labels[0])]
        self.case=case
        self.control=control
        self.case.drop(self.target,axis=1, inplace=True)
        self.control.drop(self.target,axis=1, inplace=True)
        pcor=self.case.corr()
        self.caseCorelation=self.case.corr()
        self.controlCorelation=self.control.corr()
        self.n1=self.case.shape[0]
        self.n2=self.control.shape[0]
        self.n=self.n1+self.n2
        self.m=self.case.shape[1]
        rows, cols = (self.m,self.m)
        # self.count_permuteSig=pd.DataFrame([[0]*cols]*rows)


        self.getUsDiffCorelation()
        # self.createPermutedCaseControl()
        self.runThousandPermutationTest()

    def getUsDiffCorelation(self):
        zcase=np.log((self.caseCorelation+1)/(1-self.caseCorelation))*0.5
        zcontrol=np.log((self.controlCorelation+1)/(1-self.controlCorelation))*0.5
        self.diffCorelation=(math.sqrt((self.n1-3)/2)*zcase)-(math.sqrt((self.n2-3)/2)*zcontrol)
        # print(self.diffCorelation)
        # print("reached get us case control")


    def runThousandPermutationTest(self):
        self.count_permuteSig=abs(self.diffCorelation)*0
        # print(self.diffCorelation)
        # iter=1
        # for i in range (0,1000): 
        for i in range (0,self.number_of_permutation):
            print("------->"+str(i))
            self.createPermutedCaseControl()
            self.createNewCaseControlCopyCorelation()
            self.generatecount_permuteSig_with_strategyA()
        # self.count_permuteSig=self.count_permuteSig/1000 
        print(self.count_permuteSig)


        self.saveTheResultsInDB()

    def createPermutedCaseControl(self):
        new_df=self.getUsProperDf(self.job)._get_numeric_data()
        n_swap = int(self.n1*self.n2/(self.n))
        case_swap=n_swap
        control_swap=n_swap
        flag=True
        while flag:
            r1 = random.randint(0, self.n1)
            r2 = random.randint(0, self.n2)
            temp=None
            if case_swap>0 and new_df[self.target][r1] == self.unique_labels[0]:
                new_df[self.target][r1]=self.unique_labels[1]
                case_swap=case_swap-1
            if control_swap>0 and new_df[self.target][r1] == self.unique_labels[1]:
                new_df[self.target][r2]=self.unique_labels[0]
                control_swap=control_swap-1

            if control_swap ==0 and case_swap ==0:
                flag=False
        case,control = [x for _, x in self.df.groupby(new_df[self.target]==self.unique_labels[0])]
        self.caseCopy=case
        self.controlCopy=control
        self.caseCopy.drop(self.target,axis=1, inplace=True)
        self.controlCopy.drop(self.target,axis=1, inplace=True)
        # self.count_permuteSig=abs(self.controlCopy.corr())*0



    def createNewCaseControlCopyCorelation(self):
        self.caseCorelationCopy=self.caseCopy.corr()
        self.controlCorelationCopy=self.controlCopy.corr()

        n1=self.caseCorelationCopy.shape[0]
        # n2=self.caseCorelationCopy.shape[0]
        n2=self.controlCorelationCopy.shape[0]
        zcase=np.log((self.caseCorelationCopy+1)/(1-self.caseCorelationCopy))*0.5
        zcontrol=np.log((self.controlCorelationCopy+1)/(1-self.controlCorelationCopy))*0.5
        self.diffCorelationCopy=(math.sqrt((n1-3)/2)*zcase)-(math.sqrt((n2-3)/2)*zcontrol)
        # print(self.diffCorelationCopy)




    def generatecount_permuteSig_with_strategyA(self):
        for i in range(0,self.m):
            for j in range(0,self.m):
                if(abs(float(self.diffCorelation.iat[i,j]))<abs(float(self.diffCorelationCopy.iat[i,j]))):
                    self.count_permuteSig.iat[i,j]=self.count_permuteSig.iat[i,j]+1

        # for i in range(0,self.m):
        #     for j in range(0,self.m): 
        #         self.count_permuteSig.iat[i,j]=self.count_permuteSig.iat[i,j]/self.number_of_permutation
                # self.count_permuteSig.iat[i,j]=self.count_permuteSig.iat[i,j]

        # print(self.count_permuteSig)
    def generatecount_permuteSig_with_strategyB(self):
         df1=self.diffCorelation
         df2=self.diffCorelationCopy
         self.count_permuteSig = self.count_permuteSig+((abs(df2)<abs(df1))*1)



    def getUsProperDf(self,job):
        project = Project.objects.get(id=job.project.id)
        if job.extradataset_id ==None:
            return pd.read_csv(project.dataset)
        else:
            filename=job.extradataset.basefilename
            return pd.read_csv("uploads/"+filename)

    def checkTargetAttribute(self):
            if len(self.df[self.target].unique()) >2:
                return False
            else:
                return True

    def generateNetworkData(self):
        iterator=1
        network_array=[]
        for feature in self.features:
            network_array.append({"data": { "id": feature},"group": "nodes"})
            for feature1 in self.features:
                # if self.count_permuteSig[feature][feature1]==1:
                # if self.count_permuteSig[feature][feature1]>=1:
                if self.count_permuteSig[feature][feature1]<=self.sig_count:
                # if self.count_permuteSig[feature][feature1]<=self.p_value:
                     network_array.append({
                                            "data": { "id": "e"+str(iterator),  "source": feature, "target": feature1},
                                            "group": "edges"
                                            })
                     iterator=iterator+1
        self.daa.network_data=json.dumps(network_array)
        self.daa.save()

    def saveTheResultsInDB(self):
        self.generateNetworkData()
        self.daa.diff_cor=self.diffCorelation.to_json()
        self.daa.permute_diff_cor=self.diffCorelationCopy.to_json()
        self.daa.permute_sig_corr=self.count_permuteSig.to_json()
        self.daa.save()

        self.job.status=2
        self.job.save()





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
        permute_sig_corr=pd.read_json(self.dca.permute_sig_corr)

        cell_column1=self.TableCellsOnly(diff_cor) 
        cell_column3=self.TableCellsOnly(permute_sig_corr)
 
        trace1= go.Heatmap(
            x=cell_column1[0],
            y=cell_column1[0],
            z=cell_column1[1]
            )
        data1=[trace1] 
        trace3= go.Heatmap(
            x=cell_column3[0],
            y=cell_column3[0],
            z=cell_column3[1]/self.daa.number_of_permutation
            # z=cell_column3[1]
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
        layout3=go.Layout(title="Significance Matrix", width=width,height=height)
        
        figure1=go.Figure(data=data1,layout=layout1)
        figure3=go.Figure(data=data3,layout=layout3)
        
        div1=opy.plot(figure1, auto_open=False, output_type='div')
        div3=opy.plot(figure3, auto_open=False, output_type='div')

        return [div1,div3]

    # def getMeHeatMaps(self):
    #     diff_cor=pd.read_json(self.dca.diff_cor)
    #     permute_diff_cor=pd.read_json(self.dca.permute_diff_cor)
    #     permute_sig_corr=pd.read_json(self.dca.permute_sig_corr)

    #     cell_column1=self.TableCellsOnly(diff_cor)
    #     cell_column2=self.TableCellsOnly(permute_diff_cor)
    #     cell_column3=self.TableCellsOnly(permute_sig_corr)

    #     trace1= go.Heatmap(
    #         x=cell_column1[0],
    #         y=cell_column1[0],
    #         z=cell_column1[1]
    #         )
    #     data1=[trace1]

    #     trace2= go.Heatmap(
    #         x=cell_column2[0],
    #         y=cell_column2[0],
    #         z=cell_column2[1]
    #         )
    #     data2=[trace2]
    #     trace3= go.Heatmap(
    #         x=cell_column3[0],
    #         y=cell_column3[0],
    #         z=cell_column3[1]
    #         )
    #     data3=[trace3]


    #     layout = None
    #     width= len(diff_cor.columns) * 20
    #     height= len(diff_cor.columns) * 20
    #     # if len(diff_cor.columns) > 50 :
    #     #     layout=go.Layout(title="Your Uploaded DataSet", width=width,height=height)
    #     # else :
    #     #     layout=go.Layout(title="Your Uploaded DataSet")
    #     layout1=go.Layout(title="Correlation Matrix", width=width,height=height)
    #     layout2=go.Layout(title="1000 Fold Permutaed Correlation Matrix", width=width,height=height)
    #     layout3=go.Layout(title="Significance Matrix", width=width,height=height)
    #     figure1=go.Figure(data=data1,layout=layout1)
    #     figure2=go.Figure(data=data2,layout=layout2)
    #     figure3=go.Figure(data=data3,layout=layout3)
    #     div1=opy.plot(figure1, auto_open=False, output_type='div')
    #     div2=opy.plot(figure2, auto_open=False, output_type='div')
    #     div3=opy.plot(figure3, auto_open=False, output_type='div')

    #     return [div1,div2,div3]




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

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
from apps.project_ground.models import Extradataset, PreprocessingTasks , Project,Job,PcaJobParameters,PcaResult, ComponentResult
import random


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

    caseCorelation =None
    controlCorelation=None
    diffCorelation=None
    caseCorelationCopy=None
    controlCorelationCopy=None
    diffCorelationCopy=None
    count_permuteSig=None

    def __init__(self,job):
        self.job=job
        self.df=self.getUsProperDf(job)._get_numeric_data()
        # self.df=self.df.replace(to_replace=[None], value=np.nan, inplace=True)
        self.features=list(self.df.columns.values)
        self.target=self.features[-1]
        self.features.remove(self.target)

    def getUsCaseAndControl(self):
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
        # self.getUsDiffCorelation()
        self.createPermutedCaseControl()

    def getUsDiffCorelation(self):
        zcase=np.log((self.caseCorelation+1)/(1-self.caseCorelation))*0.5
        zcontrol=np.log((self.controlCorelation+1)/(1-self.controlCorelation))*0.5
        self.diffCorelation=(math.sqrt((self.n1-3)/2)*zcase)-(math.sqrt((self.n2-3)/2)*zcontrol)
        # print(diffCorelation)

    def createPermutedCaseControl(self):
        new_df=self.getUsProperDf(self.job)._get_numeric_data()
        n_swap = int(self.n1*self.n2/(self.n))
        case_swap=n_swap
        control_swap=n_swap
        flag=True
        while flag:
            r1 = random.randint(0, self.n1)
            r2 = random.randint(0, self.n2)

            if case_swap>0 and new_df[self.target][r1] == self.unique_labels[0]:
                new_df[self.target][r1]=self.unique_labels[1]
                case_swap=case_swap-1
            if control_swap>0 and new_df[self.target][r1] == self.unique_labels[1]:
                new_df[self.target][r2]=self.unique_labels[0]
                control_swap=control_swap-1

            if control_swap ==0 and case_swap ==0:
                flag=False
        case,control = [x for _, x in self.df.groupby(self.df[self.target] ==self.unique_labels[0])]
        self.caseCopy=case
        self.controlCopy=control
        self.caseCopy.drop(self.target,axis=1, inplace=True)
        self.controlCopy.drop(self.target,axis=1, inplace=True)
        self.count_permuteSig=abs(self.controlCopy.corr())*0
        self.createNewCaseControlCopyCorelation()

    def generatecount_permuteSig(self):
        print(self.m)
        for i in range(0,self.m):
            for j in range(1,self.m):
                if((abs(float(self.diffCorelation[i][j])))<abs(float(self.diffCorelationCopy[i][j]))):
                    print(True)
                    self.count_permuteSig[i][j]=self.count_permuteSig[i][j]+1

        print(self.count_permuteSig)






    def createNewCaseControlCopyCorelation(self):
        self.caseCorelationCopy=self.caseCopy.corr()
        self.controlCorelationCopy=self.controlCopy.corr()

        n1=self.caseCorelationCopy.shape[0]
        n2=self.caseCorelationCopy.shape[0]
        zcase=np.log((self.caseCorelationCopy+1)/(1-self.caseCorelationCopy))*0.5
        zcontrol=np.log((self.controlCorelationCopy+1)/(1-self.controlCorelationCopy))*0.5
        self.diffCorelationCopy=(math.sqrt((n1-3)/2)*zcase)-(math.sqrt((n2-3)/2)*zcontrol)
        # print(self.diffCorelationCopy)
        self.generatecount_permuteSig()



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

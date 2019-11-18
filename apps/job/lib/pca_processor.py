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
class PCA_Helper:
    df=None
    X=None
    Y=None
    features=None
    target=None
    job=None

    def __init__(self,job):
        self.job=job
        self.df=self.getUsProperDf(job)._get_numeric_data()
        self.features=list(self.df.columns.values)
        self.target=self.features[-1]
        self.features.remove(self.target)

        self.X=self.df
        self.Y=self.df[self.target]
        self.X.drop(self.target,axis=1, inplace=False)

        self.X= self.X.fillna(self.X.mean())
        # self.Y= self.X.fillna(self.X.mean())
        self.StandardScale()

    def StandardScale(self):
        job_params= PcaJobParameters.objects.filter(job_id=self.job.id)[0]
        if job_params.standard_scale==1:
            self.X = StandardScaler().fit_transform(self.X)

        pca = PCA(n_components=job_params.no_of_components).fit(self.X)
        pca.transform(self.X)
        n_pcs= pca.components_.shape[0]

        self.updateDB(pca,job_params)

    def getUsProperDf(self,job):
        project = Project.objects.get(id=job.project.id)
        if job.extradataset_id ==None:
            return pd.read_csv(project.dataset)
        else:
            filename=job.extradataset.basefilename
            return pd.read_csv("uploads/"+filename)

    def updateDB(self,pca,job_params):

        variance_ratio={}
        component_values=pca.components_[0]
        n_target_features=math.floor((job_params.reduce_to/100.00)*len(self.features))
        counter = 1

        for i in pca.explained_variance_ratio_:
            variance_ratio["PC_"+str(counter)] = i
            counter=counter+1

        pca_result=PcaResult(job_id=self.job.id,variance_explained=json.dumps(variance_ratio))
        pca_result.save()


        for i in range(job_params.no_of_components):
            feature_list={}
            for j in range(n_target_features):
                location=np.abs(component_values).argmax()
                value=pca.components_[0][location]
                component_values[location]=0
                feature_list[self.features[location-1]]=value
            ComponentResult(component_id=i,result=json.dumps(feature_list),pca_result_id=pca_result.id).save()





        # x_new = pca.fit_transform(self.X)

        # # n=len(self.X)
        # # self.myplot(x_new[:,0:n],np.transpose(pca.components_[0:n, :]))
        # print(x_new[:,0:len(self.X)])
        # print(40*'-')
        # print(pca.components_[0:len(self.X), :][0])
        # print(x_new[0,0:3])
        # print(self.X)

        # most_important = [np.abs(pca.components_[i]).argmax() for i in range(n_pcs)]
        # most_important_names = [self.features[most_important[i]] for i in range(n_pcs)]
        # print(most_important)
        # dic = {'PC{}'.format(i): most_important_names[i] for i in range(n_pcs)}
        # #
        # # # build the dataframe
        # newdf = pd.DataFrame(dic.items())
        # print(pca.components_[0])

        # print(pca.components_[0])
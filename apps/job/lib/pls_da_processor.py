import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn import datasets
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.cross_decomposition import PLSRegression
import json
from django.core import serializers

from io import BytesIO
import base64
import math
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from apps.project_ground.models import Extradataset, PreprocessingTasks , Project,Job,PlsDa,PlsComponentResult

class PlsDa_Helper:
    df=None
    X=None
    Y=None
    features=None
    target=None
    job=None
    pls_da=None

    def __init__(self,job):
        self.job=job
        self.df=self.getUsProperDf(job)._get_numeric_data()
        self.features=list(self.df.columns.values)
        self.target=self.features[-1]
        self.features.remove(self.target)

        self.X=self.df
        self.Y=self.df[self.target]
        self.X.drop(self.target,axis=1, inplace=True)

        self.X= self.X.fillna(self.X.mean())
        self.pls_da=PlsDa.objects.filter(job_id=job).first()
        # print(self.Y)
        if (self.pls_da.scaler_scale==1):
            self.X = StandardScaler().fit_transform(self.X)
        # self.Y= self.X.fillna(self.X.mean())
        # print(self.X)
        self.applyPlsDa()

    def getUsProperDf(self,job):
        project = Project.objects.get(id=job.project.id)
        if job.extradataset_id ==None:
            return pd.read_csv(project.dataset)
        else:
            filename=job.extradataset.basefilename
            return pd.read_csv("uploads/"+filename)

    def applyPlsDa(self):
        model = PLSRegression(n_components=self.pls_da.no_of_components)
        #
        # print(y_scores)
        # self.VIPScore(model)
        self.updateDB(model)

    def VIPScore(self,model):
        # model.fit_transform(self.X,self.Y)
        t = model.x_scores_
        w = model.x_weights_
        q = model.y_loadings_

        m, p = self.X.shape
        _, h = t.shape
        vips = np.zeros((p,))

        s = np.diag(t.T @ t @ q.T @ q).reshape(h, -1)
        total_s = np.sum(s)

        for i in range(p):
            weight = np.array([ (w[i,j] / np.linalg.norm(w[:,j]))**2 for j in range(h) ])
            vips[i] = np.sqrt(p*(s.T @ weight)/total_s)
        print(vips)
        return vips


    def updateDB(self,model):
        # n_target_features=math.floor((job_params.reduce_to/100.00)*len(self.features))
        x_scores, y_scores=model.fit_transform(self.X,self.Y)
        x_loadings=model.x_loadings_
        y_loadings=model.y_loadings_
        x_weights=model.x_weights_
        y_weights=model.y_weights_

        vip_scores=self.VIPScore(model)
        # print(vip_scores[0])

        counter = 1
        length=len(model.x_loadings_)
        no_of_components=self.pls_da.no_of_components
        # model.fit_transform(self.X,self.Y)
        # print(len(model.predict(self.X)))
        # print(model.score(self.X,self.Y))
        for component_id in range(no_of_components):
            single_component_x_score=[]
            single_component_x_weight=[]
            for i in range(length):
                loading_x=x_loadings[i]
                weight_x=x_weights[i]
                single_component_x_score.append({"id":self.features[i],"value":loading_x[component_id]})
                single_component_x_weight.append({"id":self.features[i],"value":weight_x[component_id]})
            PlsComponentResult(component_id=component_id,result=json.dumps(single_component_x_score),result_type=2,pls_da_id=self.pls_da.id).save()
            PlsComponentResult(component_id=component_id,result=json.dumps(single_component_x_weight),result_type=0,pls_da_id=self.pls_da.id).save()
            # print(single_component_x_score)

        vip_scores_component=[]
        for i in range(length):
            vip_scores_component.append({"id":self.features[i],"value":vip_scores[i]})
        PlsComponentResult(component_id=component_id,result=json.dumps(vip_scores_component),result_type=4,pls_da_id=self.pls_da.id).save()

        self.job.status=2
        self.job.save()






        # for i in range(self.pls_da.no_of_components):
        #
        #     for j in range(model.):
        #         value=pca.components_[0][location]
        #         component_values[location]=0
        #         feature_list[self.features[location-1]]=value
            # ComponentResult(component_id=i,result=json.dumps(feature_list),pca_result_id=pca_result.id).save()

        # print("-------------pca applied success-----------")
        # self.job.status=2
        # self.job.save()

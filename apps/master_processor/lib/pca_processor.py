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

from io import BytesIO
import base64
import math
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

class PCA_Helper:
    df=None
    X=None
    Y=None
    features=None
    target=None
    job=None
    def __init__(self,job):
        self.job=job
        self.df=self.getUsProperDf(job)
        self.features=list(self.df.columns.values)
        self.target=self.features[-1]
        self.features.remove(self.target)
        # self.X=df.loc[:, self.features].values
        # self.Y = df.loc[:,self.target].values
        self.X=self.df
        self.Y=self.df[self.target]
        self.X.drop(self.target,axis=1, inplace=False)
        self.X= self.X.fillna(self.X.mean())
        self.Y= self.X.fillna(self.X.mean())
        self.StandardScale()

    def StandardScale(self):
        self.X = StandardScaler().fit_transform(self.X)
        pca = PCA(n_components=3).fit(self.X)
        # x_new = pca.fit_transform(self.X)

        # # n=len(self.X)
        # # self.myplot(x_new[:,0:n],np.transpose(pca.components_[0:n, :]))
        # print(x_new[:,0:len(self.X)])
        # print(40*'-')
        # print(pca.components_[0:len(self.X), :][0])
        # print(x_new[0,0:3])
        # print(self.X)
        pca.transform(self.X)
        n_pcs= pca.components_.shape[0]
        n_target_features=math.floor((75.00/100.00)*len(self.features))
        # print(n_target_features)

        feature_list={}
        # # for i in range n_pcs:
        component_values=pca.components_[0]
        for j in range(n_target_features):
            location=np.abs(component_values).argmax()
            value=pca.components_[0][location]
            component_values[location]=0
            feature_list[location]=value
        # print(feature_list)
        # most_important = [np.abs(pca.components_[i]).argmax() for i in range(n_pcs)]
        # most_important_names = [self.features[most_important[i]] for i in range(n_pcs)]
        # print(most_important)
        # dic = {'PC{}'.format(i): most_important_names[i] for i in range(n_pcs)}
        # #
        # # # build the dataframe
        # newdf = pd.DataFrame(dic.items())
        # print(pca.components_[0])

        print(pca.get_covariance)

    def getUsProperDf(self,job):
        if job.extradataset_id =='NULL':
            return pd.read_csv(job.project.dataset)
        else:
            return pd.read_csv("uploads/"+job.extradataset.basefilename)

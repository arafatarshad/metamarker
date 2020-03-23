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

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

class PCA_Helper:
    df=None
    X=None
    Y=None
    features=None
    target=None

    def __init__(self,components,df):
        self.df=df
        self.features=list(df.columns.values)
        self.target=self.features[-1]
        self.features.remove(self.target)
        # self.X=df.loc[:, self.features].values
        # self.Y = df.loc[:,self.target].values
        self.X=df
        self.Y=df[self.target]
        self.X.drop(self.target,axis=1, inplace=True)
        self.X= self.X.fillna(self.X.mean())
        self.Y= self.X.fillna(self.X.mean())


    def StandardScale(self):
        self.X = StandardScaler().fit_transform(self.X)
        pca = PCA()
        x_new = pca.fit_transform(self.X)

        # # n=len(self.X)
        # # self.myplot(x_new[:,0:n],np.transpose(pca.components_[0:n, :]))
        # print(x_new[:,0:len(self.X)])
        # print(40*'-')
        # print(pca.components_[0:len(self.X), :][0])
        # print(pca.components_)

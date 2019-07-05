import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.decomposition import PCA
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

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
        self.encodeXY()


    def encodeXY(self):
        for c in self.features:
            if self.df[c].dtypes=='object':
                self.df = pd.concat([self.df,pd.get_dummies(self.df[c], prefix=c,dummy_na=True)],axis=1).drop([c],axis=1)
        print(self.df.dtypes)

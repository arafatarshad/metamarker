
import pandas as pd
from random import randint
from sklearn import preprocessing as pre
import numpy as np
class ScalingDatasethandler:

    def removeClassVariable(self,df):
        numeric_df = df._get_numeric_data()
        if df[df.columns[-1]].equals(numeric_df[numeric_df.columns[-1]]):
            numeric_df.drop([numeric_df.columns[-1]],axis=1, inplace=True)
        # print(numeric_df)
        return numeric_df

    def meanRemovalAndVarianceScaling(self,df):
        # numeric_df = df._get_numeric_data()
        numeric_df = self.removeClassVariable(df)
        for c in numeric_df.columns:
            df[c]=pre.scale(numeric_df[c])
        return df
    def UnivariateScaling(self,df):
        # numeric_df = df._get_numeric_data()

        numeric_df = self.removeClassVariable(df)
        for c in numeric_df.columns:
            std=df.loc[:,c].std()
            df[c]= df[c]/std
        return df


    def ParetoScaling(self,df):
        # numeric_df = df._get_numeric_data()

        numeric_df = self.removeClassVariable(df)
        for c in numeric_df.columns:
            std=df.loc[:,c].std()
            df[c]= df[c]/math.sqrt(std)
        return df

    def LnScaling(self,df):
        numeric_df = self.removeClassVariable(df)
        for c in numeric_df.columns:
            df[c]= np.log(df[c])
        # print(df)
        return df

    def VastScaling(self,df):
        numeric_df = self.removeClassVariable(df)
        for c in numeric_df.columns:
            mean=df[c].mean()
            std=df.loc[:,c].std()
            df[c]=[mean/std]*df[c]
        return df

    def XVastScaliong(self,df):
        numeric_df = self.removeClassVariable(df)
        means=[]
        for c in numeric_df.columns:
            means.append(df[c].mean()/df.loc[:,c].std())
        max_value=max(means)
        for c in numeric_df.columns:
            df[c] = df[c] * max_value
        return df

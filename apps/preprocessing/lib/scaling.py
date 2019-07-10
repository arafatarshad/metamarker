
import pandas as pd
from random import randint
from sklearn import preprocessing as pre
import numpy as np
import math
class ScalingDatasethandler:

    def removeClassVariable(self,df):
        numeric_df = df._get_numeric_data()
        if df[df.columns[-1]].equals(numeric_df[numeric_df.columns[-1]]):
            numeric_df.drop([numeric_df.columns[-1]],axis=1, inplace=True)
        return numeric_df

    def meanRemovalAndVarianceScaling(self,df):
        numeric_df = self.removeClassVariable(df)
        for c in numeric_df.columns:
            df[c]=pre.scale(numeric_df[c])

        return df
    def UnivariateScaling(self,df):
        # numeric_df = df._get_numeric_data()

        numeric_df = self.removeClassVariable(df)
        for c in numeric_df.columns:
            std=df.loc[:,c].std()
            # df[c]= df[c]/std
            df[c]= df[c].divide(std)
            df[c].replace([np.inf, -np.inf], 0)
        return df


    def ParetoScaling(self,df):
        # numeric_df = df._get_numeric_data()

        numeric_df = self.removeClassVariable(df)
        for c in numeric_df.columns:
            std=df.loc[:,c].std()
            df[c]= df[c].divide(math.sqrt(std))
            df[c].replace([np.inf, -np.inf], 0)
        return df

    def LnScaling(self,df):
        numeric_df = self.removeClassVariable(df)
        for c in numeric_df.columns:
            df[c]= np.log(df[c])
            df[c].replace([np.inf, -np.inf], 0)
        # print(df)
        return df

    def VastScaling(self,df):
        numeric_df = self.removeClassVariable(df)
        for c in numeric_df.columns:
            mean=df[c].mean()
            std=df.loc[:,c].std()
            # df[c]=[mean/std]*df[c]
            df[c]=[mean/std]*df[c]
            df[c].replace([np.inf, -np.inf], 0)
        return df

    def XVastScaliong(self,df):
        numeric_df = self.removeClassVariable(df)
        means=[]
        for c in numeric_df.columns:
            # means.append(df[c].mean()/df.loc[:,c].std())
            means.append(df[c].mean().divide(df.loc[:,c].std()))
            df[c].replace([np.inf, -np.inf], 0)
        max_value=max(means)
        for c in numeric_df.columns:
            df[c] = df[c] * max_value
        return df

    def RangeScaling(self,df):
        numeric_df = self.removeClassVariable(df)
        for c in numeric_df.columns:
            mean=df[c].mean()
            max=mean=df[c].max()
            min=mean=df[c].min()
            # df[c] = ((df[c] - mean) / (max - min) )
            df[c] = ((df[c] - mean).divide(max - min) )
            df[c].replace([np.inf, -np.inf], 0)
        return df


    def LevelScaling(self,df):
        numeric_df = self.removeClassVariable(df)
        for c in numeric_df.columns:
            mean=df[c].mean()
            # df[c] = ((df[c] - mean) / mean )
            df[c] = ((df[c] - mean).divide(mean) )
            df[c].replace([np.inf, -np.inf], 0)
        return df


import pandas as pd
from random import randint
from sklearn import preprocessing as pre
import numpy as np
class ScalingDatasethandler:


    def meanRemovalAndVarianceScaling(self,df):
        numeric_df = df._get_numeric_data()
        for c in numeric_df.columns:
            df[c]=pre.scale(numeric_df[c])
        return df
    def UnivariateScaling(self,df):
        numeric_df = df._get_numeric_data()
        for c in numeric_df.columns:
            std=df.loc[:,c].std()
            df[c]= df[c]/std
        return df


    def ParetoScaling(self,df):
        numeric_df = df._get_numeric_data()
        for c in numeric_df.columns:
            std=df.loc[:,c].std()
            df[c]= df[c]/math.sqrt(std)
        return df

    def LnScaling(self,df):
        numeric_df = df._get_numeric_data()
        for c in numeric_df.columns:
            df[c]= np.log(df[c])
            # return df
        print(df)

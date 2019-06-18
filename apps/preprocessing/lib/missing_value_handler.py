
import pandas as pd
from random import randint

class MissingValueHandler:

    def getPctMissing(self,series):
        num = series.isnull().sum()
        den = series.count()
        return 100*(num/den)

    def fixTheColumnsDatatype(self,df,columns,limit=80):

        for c in columns:
            if df[c].dtype.kind in 'bifc':
                df[c] = pd.to_numeric(df[c], errors='coerce')

        if self.getPctMissing(df[c]) >= limit:
            df[c].drop
        return df

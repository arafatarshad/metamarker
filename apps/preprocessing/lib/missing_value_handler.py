
import pandas as pd
from random import randint

class MissingValueHandler:

    def getPctMissing(self,series):
        num = series.isnull().sum()
        den = series.count()
        return 100*(num/den)

    def fixTheColumnsDatatype(self,df,columns):
        for c in columns:
            if df[c].dtype.kind in 'bifc':
                df[c] = pd.to_numeric(df[c], errors='coerce')

        if self.getPctMissing(df[c]) >= 80:
            df[c].drop

        print(df.index[-1])

    # def fixtheObjects(self,df,c):
    #
    #     M=0
    #     O=0
    #     S=0
    #     n=(total_rows*5)
    #     m=(total_rows*2)
    #     total_rows=df.shape[0]
    #     range=df.sample(int(m/100))
    #     sample=df.sample(int(n/100))
    #
    #     for i in range:
    #         if df.loc[df.index[i],c].dtype.kind == 'M':
    #             M++
    #         elif df.loc[df.index[i],c].dtype.kind == 'O':
    #             O++
    #         elif df.loc[df.index[i],c].dtype.kind == 'S':
    #             S++
    #

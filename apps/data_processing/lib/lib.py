import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.decomposition import PCA
import pandas as pd
from sklearn.preprocessing import StandardScaler

class PCA_Helper:
    components=None
    df=None
    X=None
    Y=None
    def __init__(self,components,df):
        self.components=components
        self.df=df
        self.X=self.df.drop(self.df.columns[-1], axis=1)
        self.Y=self.df[self.df.columns[-1]]


    def myplot(score,coeff,labels=None):
        xs = score[:,0]
        ys = score[:,1]
        n = coeff.shape[0]
        scalex = 1.0/(xs.max() - xs.min())
        scaley = 1.0/(ys.max() - ys.min())
        plt.scatter(xs * scalex,ys * scaley, c = y)
        for i in range(n):
            plt.arrow(0, 0, coeff[i,0], coeff[i,1],color = 'r',alpha = 0.5)
            if labels is None:
                plt.text(coeff[i,0]* 1.15, coeff[i,1] * 1.15, "Var"+str(i+1), color = 'g', ha = 'center', va = 'center')
            else:
                plt.text(coeff[i,0]* 1.15, coeff[i,1] * 1.15, labels[i], color = 'g', ha = 'center', va = 'center')

    def showBiPlot(self):
        pca = PCA()
        x_new = pca.fit_transform(X)

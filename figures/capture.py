#!/usr/bin/env python3

from matplotlib.figure import Figure

class FigureCAM(Figure):
    def __init__(self,*args,figsize=(11/2.54,8/2.54),axsize=[2/11,2/11,7/11,5/8],**kwargs):
        super().__init__(**kwargs)
        #matplotlib multiplies axes size with large figure size 
        self.set_size_inches(figsize)
        self.my_ax=self.add_axes(axsize)
        
    def plot_data(self,axes,x,y):
        axes.axhline(color='k',linewidth=1,y=0)
        axes.axvline(color='k',linewidth=1,x=0)
        axes.plot(x,y)
        
    def update_label(self, axes, label, string):
        if label=='x_label':
            axes.set_xlabel(string,fontsize=10, position=(0.5,0),labelpad=5)
        elif label=='y_label':
            axes.set_ylabel(string,fontsize=10, position=(0.5,0),labelpad=5)
            


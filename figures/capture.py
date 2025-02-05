#!/usr/bin/env python3

from matplotlib.figure import Figure

class FigureCAM(Figure):
    def __init__(self,*args,**kwargs):
        super().__init__()
        #matplotlib multiplies axes size with large figure size 
        if not args:
            args=[15.5,13]
        figwidth=args[0]/(50*2.54)
        figheight=args[1]/(50*2.54)
        x0=0.1
        y0=0.1
        w=0.8
        h=0.8
        self.set_size_inches((figwidth,figheight))
        #self.set_size_inches((1,1))
        self.my_ax=self.add_axes([x0,y0,w,h])
        
    def plot_data(self,axes,x,y):
        axes.axhline(color='k',linewidth=1,y=0)
        axes.axvline(color='k',linewidth=1,x=0)
        axes.plot(x,y)
        
    def update_label(self, axes, label, string):
        if label=='x_label':
            axes.set_xlabel(string,fontsize=10, position=(0.5,0),labelpad=5)
        elif label=='y_label':
            axes.set_ylabel(string,fontsize=10, position=(0.5,0),labelpad=5)
            


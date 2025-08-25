#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 16:02:13 2022

@author: tze
"""
import numpy as np
from RW_data.RW_files import Files_RW
import tkinter as tk
from figures.capture import FigureCAM
from PIL import Image, ImageTk
from tkWindget.tkWindget import Rotate, OnOffButton, AppFrame, FigureFrame
import cv2
import os
from tkinter.filedialog import asksaveasfilename

class container():
    pass

         
#to do take image frame should be destroyed and then remade depending on the resolution of the camera used

    
class GUI_cam(AppFrame):
    def __init__(self,**kwargs):
        super().__init__(**kwargs,file=__file__,appgeometry=(1300, 600, 25, 25))
        self.approot.title("UWC")
        self.find_cams()
        self.init_variables()
        self.init_frames()
        self.init_image_frame()
        self.init_command_frame()
        if self.cam_list:
            self.init_cam(self.active_cam.get_var())
            #self.figure.plot.set_size_inches((self.sizex/(180*2.54),self.sizey/(180*2.54)),forward=True)
            #self.figure.plot.set_size_inches((1,1))
            print(self.figure.plot)
            self.figure.canvas.draw()
            self.figure.grid(column=2,row=0)
            
        try:
            tmp=Files_RW().check_IV_measure_ini(self.scriptdir,self.ini_name,self.split)
            self.savedir=tmp.savedir
        except:
            self.savedir='Documents'
            self.write_to_ini()
    
    def write_to_ini(self):
        write=[]
        write.append(f'save_file_path{self.split}{self.savedir}')
        Files_RW().write_to_file(self.scriptdir,self.ini_name,write)
    #you need to google how to do this
    def find_cams(self):
        cams= [item.strip() for item in os.popen('ls /dev/ | grep video').readlines()]
        self.cam_list=[]
        for item in cams:
            capture=cv2.VideoCapture(f'/dev/{item}')
            if capture.isOpened():
                self.cam_list.append(f'/dev/{item}')
                capture.release()
        
    def init_cam(self,cam):
        self.capture=cv2.VideoCapture(cam)
        frame=self.read_out_cam()
        self.capture.release()
        #self.remove_crosshair(self.pressnames.index('cross'))
        self.remove_crosshair()
        self.plot_image(frame)
        
    def init_variables(self):
        self.split=':='
        self.scriptdir=os.path.dirname(__file__)#path of this __file__ not the __main__
        self.ini_name=os.path.basename(__file__).replace(os.path.basename(__file__).split('.')[-1],'ini')
        #self.pressnames=['cam','cross']
        self.command_list={'cam':{'on':self.start_live_cam,'off':self.stop_live_cam},'cross':{'on':self.add_crosshair,'off':self.remove_crosshair},'color':{'on':self.placeholder,'off':self.placeholder}}
    def init_frames(self):    
        self.frameroot.pack(pady = (10,10), padx = (10,10))
        #for the buttons and file list
        self.command_frame=tk.Frame(self.frameroot)
        self.command_frame.grid(column=0,row=0,rowspan=3)
        #for the figure
        self.image_frame=tk.Frame(self.frameroot)
        self.image_frame.grid(column=1,row=0)
        
        
        self.figure=FigureFrame(parent=self.frameroot,figclass=FigureCAM)
        self.figure.plot.set_size_inches((2,2),forward=True)
        self.figure.plot.myaxes=self.figure.plot.add_axes([0.1,0.1,0.8,0.8])
        #self.figure.canvas.update()
        self.figure.grid(column=2,row=0)

        
    def placeholder(self,*args):
        if args:
            print(args[0])
    
    def init_command_frame(self):
        rowcount=1
        self.active_cam=Rotate(parent=self.command_frame,direction='horizontal',width=12,choice_list=self.cam_list,command=self.change_cam)
        self.active_cam.grid(column=1,row=rowcount,columnspan=2)
        rowcount+=1
        buttonframe=tk.Frame(self.command_frame)
        buttonframe.grid(column=1,row=rowcount,columnspan=2)
        self.btn_list={}
        #for idx,item in enumerate(self.pressnames):
            #tmp=OnOffButton(parent=self.command_frame,imagepath=os.path.join(self.scriptdir,'images'),images=[f'{self.pressnames[idx]}_{image}' for image in ['on.png','off.png']],command=lambda litem=item: self.press_test(litem))
        for idx, item in enumerate(self.command_list.keys()):
            tmp=OnOffButton(parent=buttonframe,imagepath=os.path.join(self.scriptdir,'images'),images=[f'{item}_{image}' for image in ['on.png','off.png']],command=lambda litem=item: self.press_test(litem))
            tmp.grid(row=rowcount,column=1+idx)
            self.btn_list[item]=tmp
        self.btn_list['cam'].enable_press()
        rowcount+=1
        self.avg_num=Rotate(parent=self.command_frame,direction='horizontal',width=5,choice_list=[1,15,25],typevar=tk.IntVar)
        self.avg_num.grid(column=1,row=rowcount,columnspan=2)
        
        rowcount+=1
        tk.Button(self.command_frame, text="Record\nimage", command=self.take_image,width=10,bg='lightgray').grid(row=rowcount,column=1)
        tk.Button(self.command_frame, text="Save\ndata", command=self.placeholder,width=10,bg='lightgray').grid(row=rowcount,column=2)

    def press_test(self,item):
        self.command_list[item][self.btn_list[item].get_state()]()
        #self.btn_list[item].change_state()
    
    def grab_frame(self):
        if self.btn_list['cam'].get_state()=='on':
            frame=self.read_out_cam()
            self.plot_image(frame)
            #self.canvas.draw()
            self.image_frame.after(1,self.grab_frame)#check this one
     
    def plot_image(self,frame):
        #here you need to adjust crosshair to the frame
        if self.sizez:
            for idx in range(np.shape(frame)[2]-1):
                frame[:,:,idx]=np.fmax(frame[:,:,idx],self.crosshair)
        else:
            frame=np.fmax(frame,self.crosshair)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.imgtk = imgtk
        self.img_label.configure(image=self.imgtk)
        
    def read_out_cam(self,*args):
        ret, frame = self.capture.read()
        frame=frame.astype(int)
        if args:
            counter=args[0]
            while counter>1:
                _,tmp=self.capture.read()
                frame=frame+tmp.astype(int)
                counter-=1
            frame=frame/args[0]
        if self.btn_list['color'].get_state()=='on':
            gray = cv2.cvtColor(frame.astype('uint8'), cv2.COLOR_BGR2RGBA)
        #    gray=frame
        elif self.btn_list['color'].get_state()=='off':
            gray = cv2.cvtColor(frame.astype('uint8'), cv2.COLOR_RGB2GRAY)
            
        self.sizey,self.sizex,*tmp=np.shape(gray)
        if tmp:
            self.sizez=tmp[0]
        else:
            self.sizez=None
        return gray
        
    def change_cam(self,*args):
        #self.pressmarker=[1,1]
        self.btn_list['cam'].change_state('off')
        self.stop_live_cam()
        self.init_cam(args[0])
    
    def start_live_cam(self):
        cam=self.active_cam.get_var()
        self.capture = cv2.VideoCapture(cam)
        self.grab_frame()
        self.btn_list['cross'].enable_press()
        self.btn_list['color'].enable_press()
        
    def remove_crosshair(self):
        self.crosshair=np.zeros((self.sizey,self.sizex)).astype('uint8')
        
    def add_crosshair(self):
        self.crosshair[int(self.sizey/2)-1,:]=255
        self.crosshair[int(self.sizey/2),:]=255
        self.crosshair[:,int(self.sizex/2)-1]=255
        self.crosshair[:,int(self.sizex/2)]=255
            
    def stop_live_cam(self):
        self.capture.release()
        self.remove_crosshair()
        self.init_cam(self.active_cam.get_var())
        self.btn_list['cross'].change_state('off')
        self.btn_list['cross'].disable_press()
        self.btn_list['color'].change_state('off')
        self.btn_list['color'].disable_press()
        
    
    def take_image(self):
        if self.btn_list['cam'].get_state()=='on':
            frame=self.read_out_cam(self.avg_num.get_var())
            self.plot_figure(frame.astype('uint8'))
            self.canvas.draw()
    
    def init_image_frame(self):
        rowcount=1
        self.img_label=tk.Label(master=self.image_frame)
        self.img_label.grid(row=rowcount,column=1)
   
        
    def plot_figure(self,frame):
        if len(self.plot.images)!=0:
            self.test.set_data(frame)
        else:
            self.test=self.plot.my_ax.imshow(frame, cmap='gray', vmin=0, vmax=255)
    
    
       
        
if __name__=='__main__':
    GUI_cam.init_start(GUI_cam())
        
        

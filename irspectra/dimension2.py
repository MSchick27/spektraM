#from ast import Delete
import tkinter as tk
#import tkmacosx as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk

import numpy as np
from scipy import optimize as opt
from scipy import signal
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
#import matplotlib.gridspec as gridspec

import os

class d2analyzer:
    def __init__(self):
        global root2d
        root2d = tk.Tk()
        root2d.title('2D GUI"')
        root2d.geometry('1300x700')
        root2d.configure(background='grey25')

        d2analyzer.windowsetup()
        d2analyzer.toolframesetup()

        def on_closing():
            if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
                plt.close()
                root2d.destroy()

        root2d.protocol("WM_DELETE_WINDOW", on_closing)
        root2d.mainloop()
       

    def windowsetup():
        global fig,main_ax,y_hist,x_hist,canvas
        dframe = tk.Frame(root2d)
        dframe.config(background='grey25')
        
        fig = plt.figure(figsize=(10, 8))
        grid = fig.add_gridspec(4, 4, hspace=0.2, wspace=0.2)
        main_ax = fig.add_subplot(grid[:-1, 1:])
        y_hist = fig.add_subplot(grid[:-1, 0], sharey=main_ax)
        x_hist = fig.add_subplot(grid[-1, 1:], sharex=main_ax)


        canvas = FigureCanvasTkAgg(fig, master= root2d)
        canvas.get_tk_widget().place(x=420,y=35,width=900,height=600)
        toolbar = NavigationToolbar2Tk(canvas,dframe)
        toolbar.pack(side=tk.TOP, fill=tk.BOTH) 

        main_ax.set_xlabel('x')
        main_ax.set_ylabel('y')
    
        dframe.place(x=420,y=0,width=900,height=35)

    def toolframesetup():
        global statusbox,toolf
        toolf = tk.Frame(root2d, borderwidth=2, relief="ridge",bg='grey20', width=400)#
        tk.Label(toolf,text='Toolbar:',font=('Arial',11),fg='white',bg='grey25',width = 55).place(x=0,y=0)

        #statustask = tk.Label(self.toolframe ,text='root',font=('Courier',10),bg ='white',fg='black',width=60,height=2)
        #statustask.pack(anchor = "w", side = "bottom")
        commandf = tk.Frame(toolf, borderwidth=2, relief="ridge", width=400)
        commandf.pack(anchor = "w", side = "bottom")
        statusbox2d = tk.Listbox(commandf,font=('Courier',10),bg ='white',fg='black',width=60,height=4)
                #listbox.pack(side = tk.LEFT, fill = tk.BOTH)
        statusbox2d.pack(anchor = "w", side = "bottom")
        commandscroll = tk.Scrollbar(commandf)
        statusbox2d.insert(0, 'root')

        toolf.pack(side= tk.LEFT, fill=tk.Y, expand=0, anchor= tk.S)

        def buttons2D():
            print('button setup')

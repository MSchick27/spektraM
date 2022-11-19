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
from matplotlib import cm
#import matplotlib.gridspec as gridspec

import os
dirpath2d = os.path.dirname(os.path.dirname(__file__))
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
        global fig,main_ax,y_hist,x_hist,canvas2d
        dframe = tk.Frame(root2d)
        dframe.config(background='grey25')
        
        fig = plt.figure(figsize=(10, 8))
        grid = fig.add_gridspec(6, 6, hspace=0.7, wspace=0.7)
        main_ax = fig.add_subplot(grid[1:-1, 1:])
        y_hist = fig.add_subplot(grid[1:-1, 0],sharey=main_ax)
        x_hist = fig.add_subplot(grid[0, 1:-1], sharex=main_ax)
        

        canvas2d = FigureCanvasTkAgg(fig, master= root2d)
        canvas2d.get_tk_widget().place(x=420,y=35,width=900,height=600)
        toolbar2d = NavigationToolbar2Tk(canvas2d,dframe)
        toolbar2d.pack(side=tk.TOP, fill=tk.BOTH) 

        main_ax.set_xlabel('x')
        main_ax.set_ylabel('y')
    
        dframe.place(x=420,y=0,width=900,height=35)

    def clear2d():
        main_ax.cla()
        y_hist.cla()
        x_hist.cla()
        canvas2d.draw()

    def plot2d(datalistentry):
        d2analyzer.clear()
        arr=1
        map=main_ax.contourf(arr[0,1:],arr[1:,0],arr[1:,1:],levels=20,cmap='RdBu_r')
        fig.colorbar(map, ax=main_ax)

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
        commandscroll2d = tk.Scrollbar(commandf)
        statusbox2d.insert(0, 'root')

        

        class buttoncommands2d():
            def initplot2d():
                a=1

            def clearplot2d():
                d2analyzer.clear2d()
                #statustask.configure(text='Plotting area cleared',fg='black')
                #statusbox.insert(0, 'Plotting area cleared')

        def buttons2D():
            def imageset2d():
                global PLOTT2d
                PLOTT2d = Image.open(str(dirpath2d)+'/pics/Plotbut.png')
                PLOTT2d = PLOTT2d.resize((150, 30), Image.ANTIALIAS)
                PLOTT2d = ImageTk.PhotoImage(PLOTT2d)
                global CLEAR2d
                CLEAR2d = Image.open(str(dirpath2d)+'/pics/clearbut.png')
                CLEAR2d = CLEAR2d.resize((100, 20), Image.ANTIALIAS)
                CLEAR2d = ImageTk.PhotoImage(CLEAR2d)
                global arrow2d
                arrow_g2d = Image.open(str(dirpath2d)+'/pics/arrow.jpeg')
                arrow_g2d = arrow_g2d.resize((18, 18), Image.ANTIALIAS)
                arrow2d = ImageTk.PhotoImage(arrow_g2d)
                global washer2d
                washer2d = Image.open(str(dirpath2d)+'/pics/backg.png')
                washer2d = washer2d.resize((18, 18), Image.ANTIALIAS)
                washer2d = ImageTk.PhotoImage(washer2d)
                global export2d
                export2d = Image.open(str(dirpath2d)+'/pics/export.jpg')
                export2d = export2d.resize((18, 18), Image.ANTIALIAS)
                export2d = ImageTk.PhotoImage(export2d)

            imageset2d()
            plotbutton2d =tk.Button(toolf,image=PLOTT2d,borderwidth=0 ,fg='skyblue',bg='grey25',command=buttoncommands2d.initplot2d).place(x=10,y=20)
            clearbutton2d =tk.Button(toolf,bg='grey25',fg='white',borderwidth=0,image=CLEAR2d, command=buttoncommands2d.clearplot2d).place(x=180,y=25)
            #axisbutton = tk.Button(toolf,bg='grey90',fg='darkred',borderwidth=1,text='axis', command=buttoncommands2d.set_ax).place(x=290,y=95)
            #trailsbutton =tk.Button(self.toolframe,bg='grey25',borderwidth=0,text='trails', command=buttoncommands.trails).place(x=280,y=200)
            #loadjson = tk.Button(toolf,bg='grey90',fg='darkred',font=('Arial',10),borderwidth=1,text='json', command=buttoncommands2d.load_json).place(x=280,y=230)
            #loaddata = tk.Button(toolf,image=arrow, bg='grey25',fg='white',borderwidth=0, command=buttoncommands2d.load_data).place(x=280,y=270)
            #deldata = tk.Button(toolf,image=washer, bg='grey25',fg='white',borderwidth=0, command=buttoncommands2d.delete_data).place(x=305,y=270)
            #exjson = tk.Button(toolf,image=export, bg='grey25',fg='white',borderwidth=0, command=buttoncommands2d.export_json).place(x=330,y=270)
            #d2plot = tk.Button(toolf,bg='grey90',fg='darkred',font=('Arial',10),borderwidth=1,text='2D', command=buttoncommands2d.dimension2).place(x=300,y=25)


        def inputset():
            global xlow2d,xhigh2d,ylow2d,yhigh2d
            global xlabel2d,ylabel2d,titleentry2d, zmulti2d
            global gridbox2d

            tk.Label(toolf,bg='grey25',text='x:',font=('Arial',10),fg='white').place(x=10,y=100)
            xlow2d = tk.Entry(toolf,bg='black',fg='white',width=12,borderwidth=0,font=('Arial',10))
            xlow2d.insert(0,'')
            xlow2d.place(x=25,y=110)
            xhigh2d = tk.Entry(toolf,bg='black',fg='white',width=12,borderwidth=0,font=('Arial',10))
            xhigh2d.insert(0,'')
            xhigh2d.place(x=25,y=90)

            xlabel2d = tk.Entry(toolf,bg='black',fg='white',width=20,borderwidth=0,font=('Arial',10))
            xlabel2d.insert(1,'xlabel')
            xlabel2d.place(x=10,y=130)


            tk.Label(toolf,bg='grey25',text='y:',font=('Arial',10),fg='white').place(x=160,y=100)
            ylow2d = tk.Entry(toolf,bg='black',fg='white',width=12,borderwidth=0,font=('Arial',10))
            ylow2d.insert(0,'')
            ylow2d.place(x=200,y=110)
            yhigh2d = tk.Entry(toolf,bg='black',fg='white',width=12,borderwidth=0,font=('Arial',10))
            yhigh2d.insert(0,'')
            yhigh2d.place(x=200,y=90)

            ylabel2d = tk.Entry(toolf,bg='black',fg='white',width=20,borderwidth=0,font=('Arial',10))
            ylabel2d.insert(-1,'ylabel')
            ylabel2d.place(x=200,y=130)

            tk.Label(toolf,bg='grey25',text='Z_fac:',font=('Arial',10),fg='white').place(x=160,y=150)
            zmulti2d = tk.Entry(toolf,bg='black',fg='white',width=12,borderwidth=0,font=('Arial',10))
            zmulti2d.insert(-1,'')
            zmulti2d.place(x=200,y=150)

            titleentry2d = tk.Entry(toolf,bg='black',fg='white',width=20,borderwidth=0,font=('Arial',10))
            titleentry2d.insert(0,'Title')
            titleentry2d.place(x=10,y=65)


            tk.Label(toolf,bg='grey25',fg='white',text='Grid:',font=('Arial',10)).place(x=10,y=160)
            gridbox2d = tk.BooleanVar()
            tk.Checkbutton(toolf,variable=gridbox2d,bg='grey20').place(x=45,y=157)

        buttons2D()
        inputset()
        toolf.pack(side= tk.LEFT, fill=tk.Y, expand=0, anchor= tk.S)
#d2analyzer()






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


from irspectra import *
from fitwindow import *

import os
softwarepath = str(os.path.abspath(__file__))
dirpath = os.path.dirname(__file__)
print(dirpath)
import pathlib

from initval import *   
init_dict = init()  
jsondict = {}
import json

class plotwindow:
    def __init__(self):
        global root1
        root1 = tk.Tk()
        root1.title('Plotting GUI')
        root1.geometry('1300x700')
        root1.configure(background='grey25')
        plotwindow.init_toolbar(self)
        plotwindow.init_plotframe(self)

        def on_closing():
            if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
                plt.close()
                root1.destroy()

        root1.protocol("WM_DELETE_WINDOW", on_closing)
        root1.mainloop()


    def init_plotframe(self): 
        self.mframe = tk.Frame(root1)
        self.mframe.config(background='grey25')

        figure, self.ax = plt.subplots(2,1,gridspec_kw={'height_ratios': [2, 1]},figsize=(12,8))
        self.canvas = FigureCanvasTkAgg(figure, master= root1)#self.mframe)
        self.canvas.get_tk_widget().place(x=420,y=35,width=900,height=600)
        toolbar = NavigationToolbar2Tk(self.canvas,self.mframe)
        toolbar.pack(side=tk.TOP, fill=tk.BOTH) 

        self.ax[0].set_xlabel(init_dict['xlabel'])
        self.ax[0].set_ylabel(init_dict['ylabel'])
        self.ax[1].set_xlabel(init_dict['xlabel'])
        self.ax[1].set_ylabel(init_dict['ylabel'])
    
        self.mframe.place(x=420,y=0,width=900,height=35)


    def plot(self):
        self.ax[0].cla()
        self.ax[1].cla()
        self.canvas.draw()

        #print(jsondict)
        for key in jsondict:
            x = list(jsondict[key]['xdata'])
            y = list(jsondict[key]['ydata'])
            subnum = int(jsondict[key]['subplot'])
            farb = str(jsondict[key]['color'])
            bgdatakey = jsondict[key]['bgkey']
            linest = jsondict[key]['linestyle']
            print(linest)
 
            if jsondict[key]['bg'] == True:
                xbg= list(jsondict[bgdatakey]['xdata'])
                ybg= list(jsondict[bgdatakey]['ydata'])
                scale = float(jsondict[key]['bgscale'])
                x,y = substract_bg(x,y,xbg,ybg,scale)
                print('bg substracted')

            multi = float(ymulti.get())
            y = [(item*multi) for item in y]

            if jsondict[key]['show'] == True:
                self.ax[subnum].plot(x,y,color=farb,linestyle=str(linest))

        #self.ax.legend()
        
        self.ax[0].set_xlabel(str(xlabel.get()))
        self.ax[0].set_ylabel(str(ylabel.get()))
        self.ax[1].set_xlabel(str(xlabel.get()))
        self.ax[1].set_ylabel(str(ylabel.get()))
        self.ax[0].grid(gridbox.get())
        self.ax[0].set_xlim(float(xlow.get()),float(xhigh.get()))
        self.ax[0].set_ylim(float(ylow.get()),float(yhigh.get()))
        self.ax[1].set_xlim(float(xlow.get()),float(xhigh.get()))
        self.canvas.draw()
    


    def clear(self):
        self.ax[0].cla()
        self.ax[1].cla()
        self.canvas.draw()




    def init_toolbar(self):
        global statusbox
        self.toolframe = tk.Frame(root1, borderwidth=2, relief="ridge",bg='grey20', width=400)#
        tk.Label(self.toolframe,text='Toolbar:',font=('Arial',11),fg='white',bg='grey25',width = 55).place(x=0,y=0)

        #statustask = tk.Label(self.toolframe ,text='root',font=('Courier',10),bg ='white',fg='black',width=60,height=2)
        #statustask.pack(anchor = "w", side = "bottom")
        commandframe = tk.Frame(self.toolframe, borderwidth=2, relief="ridge", width=400)
        commandframe.pack(anchor = "w", side = "bottom")
        statusbox = tk.Listbox(commandframe,font=('Courier',10),bg ='white',fg='black',width=60,height=4)
                #listbox.pack(side = tk.LEFT, fill = tk.BOTH)
        statusbox.pack(anchor = "w", side = "bottom")
        commandscroll = tk.Scrollbar(commandframe)
        statusbox.insert(0, 'root')

        
        def imageset():
            global PLOTT
            PLOTT = Image.open(str(dirpath)+'/pics/Plotbut.png')
            PLOTT = PLOTT.resize((150, 30), Image.ANTIALIAS)
            PLOTT = ImageTk.PhotoImage(PLOTT)
            global CLEAR
            CLEAR = Image.open(str(dirpath)+'/pics/clearbut.png')
            CLEAR = CLEAR.resize((100, 20), Image.ANTIALIAS)
            CLEAR = ImageTk.PhotoImage(CLEAR)
            global arrow
            arrow_g = Image.open(str(dirpath)+'/pics/arrow.jpeg')
            arrow_g = arrow_g.resize((18, 18), Image.ANTIALIAS)
            arrow = ImageTk.PhotoImage(arrow_g)
            global washer
            washer = Image.open(str(dirpath)+'/pics/backg.png')
            washer = washer.resize((18, 18), Image.ANTIALIAS)
            washer = ImageTk.PhotoImage(washer)
            global export
            export = Image.open(str(dirpath)+'/pics/export.jpg')
            export = export.resize((18, 18), Image.ANTIALIAS)
            export = ImageTk.PhotoImage(export)

        class buttoncommands:
            def __init__(self):
                a=1
            def test():
                print('click')

            def plotplot():
                scrollframe.change_json(datalistbox)
                plotwindow.plot(self)
                #statustask.configure(text='Plotting',fg='black')
                statusbox.insert(0, 'Plotting...')

            def clearplot():
                plotwindow.clear(self)
                #statustask.configure(text='Plotting area cleared',fg='black')
                statusbox.insert(0, 'Plotting area cleared')
                xlow.delete(0,tk.END)
                xhigh.delete(0,tk.END)
                ylow.delete(0,tk.END)
                yhigh.delete(0,tk.END)
                xlow.insert(0,float(init_dict['xlow']))
                xhigh.insert(0,float(init_dict['xhigh']))
                ylow.insert(0,float(init_dict['ylow']))
                yhigh.insert(0,float(init_dict['yhigh']))

            def set_ax():
                points = plt.ginput(n=3,timeout=30, show_clicks=True, mouse_add = plt.MouseButton.LEFT,mouse_pop= plt.MouseButton.RIGHT,mouse_stop = plt.MouseButton.MIDDLE)
                print(points)
                x_margin = [round(float(points[0][0]),6),round(float(points[1][0]),6)]
                x_margin.sort()
                y_margin = [round(float(points[0][1]),6),round(float(points[1][1]),6)]
                y_margin.sort()
                #print(x_margin)
                xlow.delete(0,tk.END)
                xhigh.delete(0,tk.END)
                ylow.delete(0,tk.END)
                yhigh.delete(0,tk.END)
                xlow.insert(0,str(x_margin[0]))
                xhigh.insert(0,str(x_margin[1]))
                ylow.insert(0,str(y_margin[0]))
                yhigh.insert(0,str(y_margin[1]))
                buttoncommands.plotplot()

            def load_json():
                global jsondict
                #statustask.configure(text='json.err',fg='red')
                statusbox.insert(0, 'json.err')

                filename = filedialog.askopenfilename(initialdir = str(dirpath), 
                                          title = "Open Files") 
                jsonfile = open(str(filename),'r')
                jsondict = json.load(jsonfile)
                #print(jsondict)
                #statustask.configure(text='json imported',fg='red')
                statusbox.insert(0, 'json imported')

                listbox.delete(0,tk.END)
                for key in jsondict:
                    listbox.insert(tk.END, key)

                #statustask.configure(text='Project loaded',fg='green')
                statusbox.insert(0, 'Project loaded')

            def export_json():
                a = filedialog.asksaveasfilename(initialdir = str(dirpath),title = "Save file")
                newjsonfile = open(str(str(a) + '.json'),'w')
                json.dump(jsondict, newjsonfile)
                newjsonfile.close()
                
            
            def load_data():
                global jsondict
                #statustask.configure(text='app.err',fg='red')
                statusbox.insert(0, 'app.err')
                filenames = filedialog.askopenfilenames(initialdir = str(dirpath), 
                                          title = "Open Files") 
                datatup = filenames
                for datapath in datatup:
                    buttoncommands.gen_json_label(datapath)
                #statustask.configure(text='data appended',fg='green')
                statusbox.insert(0, 'data appended')

            def gen_json_label(datapath):
                dataname = os.path.basename(datapath)
                print('new data appended to json')
                delimiter = str(delimitervar.get())
                
                if delimiter == 'tab':
                    print('tab')
                    x,y = import_data(datapath,'\t')
                if delimiter == 'space':
                    x,y = import_data(datapath,' ')
                
                dataset = {'xdata': x,
                            'ydata': y,
                            'bg': False,
                            'bgkey':'',
                            'bgscale': 0,
                            'show': True,       #defaults
                            'color': 'black',    #...
                            'linewidth': 0.9 ,
                            'linestyle':'solid',
                            'label':"import" ,
                            'subplot': 0         
                            }

                
                counter=0
                while dataname in jsondict:
                    counter = counter+1
                    dataname = str(dataname + str(counter))

                jsondict[str(dataname)]= dataset
                listbox.insert(tk.END, dataname)



            def delete_data():
                listbox.delete(tk.ANCHOR)
                jsondict.pop(str(datalistbox), None)

            def change_key(data):
                new_key = str(datalabelentry.get())
                jsondict[new_key] = jsondict[data]
                del jsondict[data]
                listbox.delete(tk.ANCHOR)
                listbox.insert(tk.ANCHOR , str(new_key))
            
            def change_res(les):
                scales.configure(resolution= scales_res.get())

            def findpeaks(data):
                x = list(jsondict[data]['xdata'])
                y = list(jsondict[data]['ydata'])
                num = int(jsondict[data]['subplot'])
                bgdatakey = jsondict[data]['bgkey']

                if jsondict[data]['bg'] == True:
                    xbg= list(jsondict[bgdatakey]['xdata'])
                    ybg= list(jsondict[bgdatakey]['ydata'])
                    scale = float(jsondict[data]['bgscale'])
                    x,y = substract_bg(x,y,xbg,ybg,scale)
                
                yarr = np.array(y)
                #print(y)
                peaks,_ = signal.find_peaks(yarr,prominence=0.0005)#height=0.001)
                print(peaks,_)
                xpeaks = []
                ypeaks = []
                for item in peaks:
                    xpeaks.append(x[item])
                    ypeaks.append(y[item]*1000)
                
                print(ypeaks)
                for c in range(len(xpeaks)):
                    self.ax[num].text(xpeaks[c],ypeaks[c],s=str(round(xpeaks[c],4))+'\n',size=10)
                self.ax[num].scatter(xpeaks,ypeaks,marker='x',color='r')
                self.canvas.draw()




            def export_data(data):
                a = filedialog.asksaveasfilename(initialdir = dirpath,title = "Save file")#,filetypes = (("textfiles", "*.txt*"))) 
                x = list(jsondict[data]['xdata'])
                y = list(jsondict[data]['ydata'])
                bgdatakey = jsondict[data]['bgkey']
                if jsondict[data]['bg'] == True:
                    xbg= list(jsondict[bgdatakey]['xdata'])
                    ybg= list(jsondict[bgdatakey]['ydata'])
                    scale = float(jsondict[data]['bgscale'])
                    x,y = substract_bg(x,y,xbg,ybg,scale)

                newfile = open(a,'w')
                for i in range(len(x)):
                    wav = x[i]
                    wav = format(wav,'.9f')
                    ab = y[i]
                    ab = format(ab,'.9f')
                    newfile.write(str(wav)+'\t'+str(ab)+'\n')
                newfile.close()

            def polyfit_data(data):
                if jsondict[data]['bg'] == True:
                    print('mit bg auto anpassung des grades des Polyfits')

                if jsondict[data]['bg'] == False:
                    polydeg = int(polyentry.get())
                    print('manuelle eingabe des grades')
                    waveval = waveentry.get()
                    xpoly = list(waveval.split(','))
                    if waveval =='':
                        polypoints = plt.ginput(n=5,timeout=30, show_clicks=True, mouse_add = plt.MouseButton.LEFT,mouse_pop= plt.MouseButton.RIGHT,mouse_stop = plt.MouseButton.MIDDLE)
                        xpoly = [polypoints[0][0],polypoints[1][0],polypoints[2][0],polypoints[3][0]]

                    xpoly = [float(item) for item in xpoly]
                    xpoly.sort()
                    statusbox.insert(0, str(xpoly))
                    print(xpoly)

                    x = list(jsondict[data]['xdata'])
                    y = list(jsondict[data]['ydata'])

                    xred,yred = data_red(x,y,xpoly[0],xpoly[1])
                    xred2, yred2 = data_red(x,y,xpoly[2],xpoly[3])

                    for c in range(len(xred2)):
                        xred.append(xred2[c])
                        yred.append(yred2[c])
                    
                    polypar = np.polyfit(xred,yred,polydeg)
                    polyfunk = np.poly1d(polypar)
                    statusbox.insert(0, str(polyfunk))
                    xdatapoly,ydatad = data_red(x,y,xpoly[0],xpoly[3])
                    ydatapoly = []
                    for i in range(len(xdatapoly)):
                        yval = polyfunk(xdatapoly[i])
                        ydatapoly.append(yval)
                    
                    polyset = {'xdata': xdatapoly,
                            'ydata': list(polyfunk(xdatapoly)) ,
                            'bg': False,
                            'bgkey':'',
                            'bgscale': 0,
                            'show': True,       #defaults
                            'color': 'grey',    #...
                            'linewidth': 0.9 ,
                            'linestyle':'dashed',
                            'label':str('Polyfit') ,
                            'subplot': 0         
                            }
                    
                    datapol = str(data+'_polyfit')
                    counter=0
                    while datapol in jsondict:
                        counter = counter+1
                        datapol = str(datapol + str(counter))

                    jsondict[datapol] = polyset
                    listbox.insert(tk.END, datapol)
                    
                    doubledset = {'xdata': xdatapoly,
                            'ydata': ydatad ,
                            'bg': True,
                            'bgkey':str(str(data)+'_polyfit'),
                            'bgscale': 1,
                            'show': True,       #defaults
                            'color': 'darkorange',    #...
                            'linewidth': 0.9 ,
                            'linestyle':'solid',
                            'label':str('Data for substraktion') ,
                            'subplot': 0         
                            }
                    
                    datadub = str(data+'_data')
                    counter=0
                    while datadub in jsondict:
                        counter = counter+1
                        datadub = str(datadub + str(counter))

                    jsondict[datadub] = doubledset
                    listbox.insert(tk.END, datadub)
                    


            def fit_data(data):
                x = list(jsondict[data]['xdata'])
                y = list(jsondict[data]['ydata'])
                bgdatakey = jsondict[data]['bgkey']
                if jsondict[data]['bg'] == True:
                    xbg= list(jsondict[bgdatakey]['xdata'])
                    ybg= list(jsondict[bgdatakey]['ydata'])
                    scale = float(jsondict[data]['bgscale'])
                    x,y = substract_bg(x,y,xbg,ybg,scale)

                tpoints = plt.ginput(n=3,timeout=30, show_clicks=True, mouse_add = plt.MouseButton.LEFT,mouse_pop= plt.MouseButton.RIGHT,mouse_stop = plt.MouseButton.MIDDLE)
                print(tpoints)
                xps = [tpoints[0][0],tpoints[1][0],tpoints[2][0]]
                yps = [tpoints[0][1],tpoints[1][1],tpoints[2][1]]
                xh = max(xps)
                xl = min(xps)
                width = (xh-xl)/2.4
                xps.remove(xl)
                xps.remove(xh)
                xpeak = xps[0]
                amp = max(yps)-min(yps)
                height = min(yps)
                fittype = ftype.get()
                fname = fitname.get()
                x,y = data_red(x,y,xl,xh)

                if fittype == 'Gauss':
                    fitx, fity,parstr,par = gaussfit_data(x,y,amp,xpeak,width,height)
                    yfwhm = par[0]/2 + par[3]
                    w = abs(par[2]) *2
                    xfwhm1 = par[1] - w/2
                    xfwhm2 = par[1] + w/2
                    fwhmset = {'xdata': [xfwhm1,xfwhm2],
                            'ydata': [yfwhm,yfwhm] ,
                            'bg': False,
                            'bgkey':'',
                            'bgscale': 0,
                            'show': True,       #defaults
                            'color': 'grey',    #...
                            'linewidth': 0.9 ,
                            'linestyle':'dashed',
                            'label':str('FWHM:'+str(round(w,3))) ,
                            'subplot': 0         
                            }

                if fittype == 'Lorentz':
                    fitx, fity,parstr,par = lorentzfit(x,y,amp,xpeak,width,height)
                    yfwhm = par[0]/2 + par[3]
                    w = abs(par[2]) *2
                    xfwhm1 = par[1] - w/2
                    xfwhm2 = par[1] + w/2
                    fwhmset = {'xdata': [xfwhm1,xfwhm2],
                            'ydata': [yfwhm,yfwhm] ,
                            'bg': False,
                            'bgkey':'',
                            'bgscale': 0,
                            'show': True,       #defaults
                            'color': 'grey',    #...
                            'linewidth': 0.9 ,
                            'linestyle':'dotted',
                            'label':str('FWHM:'+str(round(w,3))) ,
                            'subplot': 0         
                            }
                    

                
                dataset = {'xdata': fitx,
                            'ydata': fity,
                            'bg': False,
                            'bgkey':'',
                            'bgscale': 0,
                            'show': True,       #defaults
                            'color': 'red',    #...
                            'linewidth': 0.9 ,
                            'linestyle':'solid',
                            'label':str(fname) ,
                            'subplot': 0         
                            }

                #statustask.configure(text=str(parstr),fg='magenta')
                statusbox.insert(0, str(parstr))
                fwhmstr = str('fwhm: ' + str(round(w,3)))
                statusbox.insert(0, str(fwhmstr))
                jsondict[str(fname)]= dataset
                jsondict[str(str(fname)+' '+ str(fwhmstr))] = fwhmset
                listbox.insert(tk.END, fname)
                listbox.insert(tk.END, str(str(fname)+' '+ str(fwhmstr)))



        def buttonset():
            plotbutton =tk.Button(self.toolframe,image=PLOTT,borderwidth=0 ,fg='skyblue',bg='grey25',command=buttoncommands.plotplot).place(x=10,y=20)
            clearbutton =tk.Button(self.toolframe,bg='grey25',fg='white',borderwidth=0,image=CLEAR, command=buttoncommands.clearplot).place(x=180,y=25)
            axisbutton = tk.Button(self.toolframe,bg='grey25',fg='darkred',borderwidth=0,text='axis', command=buttoncommands.set_ax).place(x=290,y=95)
            #trailsbutton =tk.Button(self.toolframe,bg='grey25',borderwidth=0,text='trails', command=buttoncommands.trails).place(x=280,y=200)
            loadjson = tk.Button(self.toolframe,bg='grey80',fg='darkred',font=('Arial',10),borderwidth=0,text='json', command=buttoncommands.load_json).place(x=280,y=230)
            loaddata = tk.Button(self.toolframe,image=arrow, bg='grey25',fg='white',borderwidth=0, command=buttoncommands.load_data).place(x=280,y=270)
            deldata = tk.Button(self.toolframe,image=washer, bg='grey25',fg='white',borderwidth=0, command=buttoncommands.delete_data).place(x=305,y=270)
            exjson = tk.Button(self.toolframe,image=export, bg='grey25',fg='white',borderwidth=0, command=buttoncommands.export_json).place(x=330,y=270)
        
        def inputset():
            global xlow,xhigh,ylow,yhigh
            global xlabel,ylabel,titleentry, ymulti
            global gridbox,delimiteropt,delimitervar

            tk.Label(self.toolframe,bg='grey25',text='x:',font=('Arial',10),fg='white').place(x=10,y=100)
            xlow = tk.Entry(self.toolframe,bg='black',fg='white',width=12,borderwidth=0,font=('Arial',10))
            xlow.insert(0,float(init_dict['xlow']))
            xlow.place(x=25,y=110)
            xhigh = tk.Entry(self.toolframe,bg='black',fg='white',width=12,borderwidth=0,font=('Arial',10))
            xhigh.insert(0,float(init_dict['xhigh']))
            xhigh.place(x=25,y=90)

            xlabel = tk.Entry(self.toolframe,bg='black',width=20,borderwidth=0,font=('Arial',10))
            xlabel.insert(1,str(init_dict['xlabel']))
            xlabel.place(x=10,y=130)


            tk.Label(self.toolframe,bg='grey25',text='y:',font=('Arial',10),fg='white').place(x=160,y=100)
            ylow = tk.Entry(self.toolframe,bg='black',fg='white',width=12,borderwidth=0,font=('Arial',10))
            ylow.insert(0,float(init_dict['ylow']))
            ylow.place(x=200,y=110)
            yhigh = tk.Entry(self.toolframe,bg='black',fg='white',width=12,borderwidth=0,font=('Arial',10))
            yhigh.insert(0,float(init_dict['yhigh']))
            yhigh.place(x=200,y=90)

            ylabel = tk.Entry(self.toolframe,bg='black',fg='white',width=20,borderwidth=0,font=('Arial',10))
            ylabel.insert(-1,str(init_dict['ylabel']))
            ylabel.place(x=200,y=130)

            tk.Label(self.toolframe,bg='grey25',text='y_fac:',font=('Arial',10),fg='white').place(x=160,y=150)
            ymulti = tk.Entry(self.toolframe,bg='black',fg='white',width=12,borderwidth=0,font=('Arial',10))
            ymulti.insert(-1,str(init_dict['ymulti']))
            ymulti.place(x=200,y=150)

            titleentry = tk.Entry(self.toolframe,bg='black',fg='white',width=20,borderwidth=0,font=('Arial',10))
            titleentry.insert(0,'Title')
            titleentry.place(x=10,y=65)


            tk.Label(self.toolframe,bg='grey25',fg='white',text='Grid:',font=('Arial',10)).place(x=10,y=160)
            gridbox = tk.BooleanVar()
            tk.Checkbutton(self.toolframe,variable=gridbox,bg='grey20').place(x=45,y=157)

            delimitervar = tk.StringVar()
            delimiteroptions = ['tab','space',',',';']
            delimitervar.set(delimiteroptions[0])
            delimiteropt = tk.OptionMenu(self.toolframe, delimitervar, *delimiteroptions)
            delimiteropt.config(width=3,font=('Arial',10),bg='grey25',fg='white')
            delimiteropt.place(x=280,y=295)

        class scrollframe:
            def __init__():
                global listbox,RES_LIST,scales_res
                listboxframe = tk.Frame(self.toolframe, borderwidth=1, relief="ridge")
                listboxframe.place(x= 25,y=230,width=240,height=100)
                listbox = tk.Listbox(listboxframe)
                #listbox.pack(side = tk.LEFT, fill = tk.BOTH)
                listbox.place(x=0,y=0,width = 230,height= 99)
                scrollbar = tk.Scrollbar(listboxframe)
                listbox.insert(tk.END, 'no files')

                listbox.config(yscrollcommand = scrollbar.set)
                listbox.bind("<<ListboxSelect>>",scrollframe.listboxchange)
                scrollbar.config(command = listbox.yview)

                global container
                container = tk.Frame(self.toolframe, borderwidth=2,bg='grey25', relief="ridge")
                container.place(x= 25,y=330,width=320,height=310)

                RES_LIST = [0.1,0.01,0.001,0.0001]
                scales_res= tk.DoubleVar()
                scales_res.set(RES_LIST[1])
                
                
                
                
            #diese Funktion startet bei listbox change, führt daraufhin data_set aus um den dataframe anzupassen, Knöpfe füren dann change_json aus
            def listboxchange(event):
                global datalistbox
                selection = event.widget.curselection()
                if selection:
                    index = selection[0]
                    datalistbox = event.widget.get(index)
                    scrollframe.data_set(datalistbox)
                    #print(str(data))
                else:
                    print('')

            def data_set(dataname):
                print('i will setup the frame for:'+str(dataname))
                global data_frame
                data_frame = tk.Frame(container,bg='grey25')
                data_frame.place(x= 0,y=0,width=398,height=340)
                
                global col
                col = tk.StringVar()
                col.set(str(jsondict[dataname]['color']))
                coloptions = ['black','red','blue','green','cyan','magenta','darkorange','skyblue','grey','chocolate'] 
                global line
                line = tk.StringVar()
                line.set(str(jsondict[dataname]['linestyle']))
                lineoptions = ['solid','dashed','dotted','dashdot'] 
#1. row---------------------------------------------------------
                global showbox, datalabelentry, subplotnum

                #SETUP für SHOW checkbox
                tk.Label(data_frame,text='Show:',font=('Arial',10),bg='grey25',fg='white').place(x=10,y=10)
                showbox = tk.BooleanVar()
                showcheckbutton = tk.Checkbutton(data_frame,onvalue=True,offvalue=False,variable=showbox,bg='grey25',command=lambda:scrollframe.change_json(dataname))
                showcheckbutton.place(x=40,y=8)
                #print(jsondict[str(dataname)])
                if jsondict[str(dataname)]['show'] == True:
                    showbox.set(True)
                    showcheckbutton.select()
                else:
                    showbox.set(False)
                    showcheckbutton.deselect()

                #Setup für den LABEL ENTRY
                tk.Label(data_frame,bg='grey25',text='Label:',font=('Arial',10),fg='white').place(x=70,y=10)
                datalabelentry = tk.Entry(data_frame,bg='black',font=('Arial',10),fg='white',width=15,borderwidth=0)
                datalabelentry.insert(0,str(jsondict[str(dataname)]['label']))
                datalabelentry.place(x=115,y=10)

                subplotnum = tk.IntVar()
                subplotnumoptions = [0,1]
                subplotnum.set(subplotnumoptions[int(jsondict[str(dataname)]['subplot'])])
                subplotopt = tk.OptionMenu(data_frame, subplotnum, *subplotnumoptions)
                #subplotopt.config(width=1)
                subplotopt.config(font=('Arial',10),bg='grey25',fg='white')
                subplotopt.place(x=10,y=55,width=30)

                labelchangebutton = tk.Button(data_frame,text='->', bg='grey80',fg='darkred',font=('Arial',10),borderwidth=0, command=lambda:buttoncommands.change_key(dataname)).place(x=240,y=7)

#2. row---------------------------------------------------------
                global bgbox,bgkeyentry, scales, scales_res

                #SETUP für BG checkbox
                tk.Label(data_frame,bg='grey25',text='Bg:',font=('Arial',10),fg='white').place(x=10,y=30)
                bgbox = tk.BooleanVar()
                bgcheckbutton = tk.Checkbutton(data_frame,onvalue=True,offvalue=False,variable=bgbox,bg='grey25',command=lambda:scrollframe.change_json(dataname))
                bgcheckbutton.place(x=40,y=30)
                if jsondict[str(dataname)]['bg'] == True:
                    bgbox.set(True)
                    bgcheckbutton.select()
                else:
                    bgbox.set(False)
                    bgcheckbutton.deselect()

                tk.Label(container,bg='grey25',text='Bg key:',font=('Arial',10),fg='white').place(x=70,y=30)
                bgkeyentry = tk.Entry(data_frame,bg='black',width=15,borderwidth=0,font=('Arial',10),fg='white')
                bgkeyentry.insert(0,str(jsondict[str(dataname)]['bgkey']))
                bgkeyentry.place(x=115,y=30)

                res = tk.OptionMenu(data_frame, scales_res, *RES_LIST,command=lambda:buttoncommands.change_res('var'))
                res.config(width=2,bg='grey25',fg='white',font=('Arial',10))
                res.place(x=235,y=30)

                scales = tk.Scale(data_frame,orient='horizontal',bg="grey25",font=('Arial',10),from_= -0.5, to=1.6,resolution=scales_res.get(),length =90,width=10,sliderlength=20,fg='sky blue')
                scales.set(float(jsondict[str(dataname)]['bgscale']))
                scales.bind("<ButtonRelease-1>",scrollframe.change_json(dataname))
                scales.place(x=220,y=60)


#3. row---------------------------------------------------------
                colopt = tk.OptionMenu(data_frame, col, *coloptions)#,command=lambda:scrollframe.change_json(dataname))
                colopt.config(font=('Arial',10),bg='grey25',fg='white')
                colopt.place(x=60,y=55,width=70)

                lineopt = tk.OptionMenu(data_frame, line, *lineoptions)#,command=lambda:scrollframe.change_json(dataname))
                lineopt["menu"].config(fg="RED")
                lineopt.config(bg="grey25", fg="white",font=('Arial',10))
                lineopt.place(x=140,y=55,width=70)
                
              
#last. row---------------------------------------------------------
                peakbutton = tk.Button(data_frame,text='Peaks',bg="grey80", fg="darkred",font=('Arial',10),borderwidth=0, command=lambda:buttoncommands.findpeaks(dataname)).place(x=250,y=200)


                global ftype,fitname
                fitdata = tk.Button(data_frame,text='FIT',bg="grey80", fg="darkred",font=('Arial',10) ,borderwidth=0, command=lambda:buttoncommands.fit_data(dataname)).place(x=250,y=230)
                ftype = tk.StringVar()
                ftypeoptions = ['Gauss','Lorentz']
                ftype.set(ftypeoptions[0])
                ftypeopt = tk.OptionMenu(data_frame, ftype, *ftypeoptions)
                ftypeopt.config(bg='grey25',fg='white',font=('Arial',10))
                ftypeopt.place(x=165,y=232,width=70)
                fitname = tk.Entry(data_frame,bg="black", fg="white",font=('Arial',10),width = 20)
                fitname.place(x=10,y=230)

                global polyentry, waveentry
                polyfitdata = tk.Button(data_frame,text='polyFIT', bg="grey80", fg="darkred",font=('Arial',10),borderwidth=0, command=lambda:buttoncommands.polyfit_data(dataname)).place(x=250,y=255)
                tk.Label(data_frame,bg="black", fg="white",font=('Arial',10),text='Polyfit deg:').place(x=130,y=259)
                polyentry = tk.Entry(data_frame,bg='black',fg='white',width=3,borderwidth=0,font=('Arial',10))
                polyentry.insert(0, '5')
                polyentry.place(x=190,y=259)

                #polymanfitdata = tk.Button(data_frame,text='pol-man', bg='grey25',borderwidth=0, command=lambda:buttoncommands.polyfit_data(dataname)).place(x=220,y=280)
                waveentry = tk.Entry(data_frame,bg='black',fg='white',width=16,borderwidth=0,font=('Arial',10))
                waveentry.insert(0, '')
                waveentry.place(x=10,y=259)

                exportdata = tk.Button(data_frame,text='export', bg="grey80", fg="darkred",font=('Arial',10),borderwidth=0, command=lambda:buttoncommands.export_data(dataname)).place(x=250,y=100)
                #peakfindbutton = tk.Button(data_frame,text='export', bg='grey25',borderwidth=0, command=lambda:buttoncommands.export_data(dataname)).place(x=220,y=200)

            def change_json(dataname):
                jsondict[dataname]['show']= bool(showbox.get())
                jsondict[dataname]['label']= str(datalabelentry.get())
                jsondict[dataname]['subplot']= str(subplotnum.get())
                jsondict[dataname]['bg']= bool(bgbox.get())
                jsondict[dataname]['bgkey']= str(bgkeyentry.get())
                jsondict[dataname]['bgscale']= float(scales.get())
                jsondict[dataname]['color']= str(col.get())
                jsondict[dataname]['linestyle']= str(line.get())
                print('json up to date')
                #print(jsondict)


                

        
        imageset()
        buttonset()
        inputset()
        scrollframe.__init__()
        
        self.toolframe.pack(side= tk.LEFT, fill=tk.Y, expand=0, anchor= tk.S)
        


#%%Initiation

plotwindow()


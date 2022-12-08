import numpy as np
from scipy import optimize as opt
import tkinter as tk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

def data_red(x,y,xl,xh):
    xvals = []
    yvals = []
    for i in range(len(x)):
        if x[i] <= xh:
            if x[i] >= xl:
                xvals.append(x[i])
                yvals.append(y[i])

    return xvals, yvals


def gaussfit_data(x,y,amp,xpeak,width,height):
    guess=[amp,xpeak,width,height]
    print(guess)
    par,cov = opt.curve_fit(gauss,x,y,guess,maxfev=100000)
    print(par)
    fitx = x
    fity = []
    for i in range(len(fitx)):
        y_val = gauss(x[i],*par)
        fity.append(y_val)
    
    parstring = str('Amp:' + str(round(par[0],3)) + ', xpeak:' + str(round(par[1],3)) +', width:' + str(round(par[2],3)))
    return fitx,fity, parstring, par

def gaussfit_fine(x,y,amp,xpeak,width,height):
    guess=[amp,xpeak,width,height]
    print(guess)
    par,cov = opt.curve_fit(gauss,x,y,guess,maxfev=100000)
    fitx = np.linspace(x[0],x[-1],2000)
    fity = []
    for i in range(len(fitx)):
        y_val = gauss(fitx[i],*par)
        fity.append(y_val)
    
    parstring = str('Amp:' + str(round(par[0],3)) + ', xpeak:' + str(round(par[1],3)) +', width:' + str(round(par[2],3)))
    return fitx,fity, parstring, par

def gauss(x,a,b,c,g):
    return a*np.exp(-(x-b)**2 / c**2)+g

def lorentzfit(x,y,amp,xpeak,width,height):
    guess=[amp,xpeak,width,height]
    print(guess)
    par,cov = opt.curve_fit(lorentz,x,y,guess,maxfev=100000)
    print(par)
    fitx = x
    fity = []
    for i in range(len(x)):
        y_val = lorentz(x[i],*par)
        fity.append(y_val)

    parstring = str('Amp:' + str(round(par[0],5)) + ', x:' + str(round(par[1],3)) +', c:' + str(round(par[2],3)) +', FWHM:' + str(round(FWHM(par[2]),2)))
    return fitx,fity,parstring,par


def lorentz(x,a,b,c,g):
    return ((a*c**2)/((x-b)**2+c**2)) + g

def lorentztest(x,a,b,c,g):
    return ((2*a)/np.pi * c/((x-b)**2+c**2)) + g

def FWHM(c):
    return c*np.pi
    












class polyfit_window():
    def init_widgets(root):
        global polyentry,polywindow
        polywindow = tk.Toplevel(root)
        polywindow.geometry('200x100')
        #polyfit_window.init_widgets(self)
        
        tk.Label(polywindow,bg='grey20',text='Polyfit deg:',font=('Arial',11),fg='white').place(x=10,y=10)
        polyentry = tk.Entry(polywindow,bg='black',width=15,borderwidth=0,font=('Arial',11))
        polyentry.insert(0, '5')
        polyentry.place(x=70,y=10)
        polfit = tk.Button(polywindow,text='Polyfit', bg='grey25',borderwidth=0, command=polyfit_window.polyfit_fit).place(x=70,y=30)
        polywindow.mainloop()

    def polyfit_fit():
        global polydeg
        print('polybutton worked')
        polydeg = int(polyentry.get())
        polywindow.destroy()



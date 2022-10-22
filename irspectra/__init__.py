'''
Funktionen von ir-spectra zu importierung

import_dpt() 
zieht aus dpt datei wavenumber und absorbnumber als 2d array
nimmt nur Wellenzahlen im ausgewählten bereich
INPUTS: low_wav, high_wav, data_path


backgroundwash()
input sind die Wellenzahlen die den gewünschten bereich eingrenzen,
sowie auch die Daten  als 2d-array und background noise data_path
Funktion zieht vom Datensatz den Background ab und gibt neues Datenset
-------------------------------------------
INPUTS: low_wav,high_wav,data_2d_array,background_path,scale
return 2d-array mit subtrahierten Daten


peak_finder()
-startet mit dem iterationsblock [c-iter,val,c+iter]
-Dieser block wird iterativ vergrößert bis die entsprechnde anzahl an Peaks
mit der geforderten Anzahl übereinstimmt.
-Peaks sind definiert als maximum ihres iterationsblockes
-------------------------------------------
INPUTS: d2d_array,peaknumber,iterblocksize
return ist ein 2d-array mit x und y koord aller peaks


mean()
-nimmt als input Liste aus daten in form von Liste mit jeweils 2d-arrays
-berechnet aus allen datensätzen einen mean value und gibt einen mittleren datansatz
-------------------------------------------
INPUTS: low_wav,high_wav,data_list_input,mean_spec
return: Liste mit y mean-werten


correlate()
-skaliert datensatz zwischen 0.8 und 1.2 und berechnet für jede skalierung die
Summe der Residuen zwischen skalierten Datensatz und dem datensatz dem angenähert 
werden soll aus
-gesucht wird die skalierung mit der kleinsten Summe aller y-residuen
- der skalierungs faktor wird auf den Datensatz multipliziert
Dieser Funktion funktioniert unter der annahme , dass die peaks nur ein kleinen Teil des
Spektrums einnehmen. Skaliert wird nach der Differenz des gesamten Spektrums. 
Da die Peaks und deren Werte unterschied nur wenig Gewichtung haben sind bei diesen trotzdem
die Unterschiede zu erkennen
-------------------------------------------
INPUTS: low_wav,high_wav,data_list_input,mean_spec
return ist eine liste mit den skalierten 2d arrays
'''
import numpy as np
from scipy import optimize as opt
def import_dpt_tupel(low_wav,high_wav,data_path_tupel):
    data_list = [] #contains 2d-arrays as list
    for c in range(len(data_path_tupel)):
        if data_path_tupel[c] != '':
            darr = import_dpt(low_wav,high_wav,data_path_tupel[c])
            data_list.append(darr)

    return data_list

#import funktion um dpt einzulesen
def import_dpt(low_wav, high_wav, data_path):
    data = open(data_path,'r')
    data = data.readlines()

    wavenums = []
    absorbnums = []
    for item in data:
        seg = item.index('\t')
        wavestr = item[0:seg]
        wavenum = float(wavestr)       #import aller wavnumbers

        if wavenum >= low_wav:           #Dieser block schränkt den Datensatz ein um nur
            if wavenum <= high_wav:      #den gewollten Bereich zu importieren
                wavenums.append(wavenum)
                absorb = item[seg:int(len(item)-1)] #10->11 wenn ir
                absorbnum = float(absorb) *10**(3) #for milli_OD
                absorbnums.append(absorbnum)

    darray = np.array([wavenums,absorbnums])    #Bildung von 2d-array als datensatz mit Zeile 0 als wavenumber=x

    return darray

def import_data(data_path,delimit):
    data = open(data_path,'r')
    data = data.readlines()
    x = []
    y = []
    for item in data:
        seg = item.index(delimit)
        wavestr = item[0:seg]
        wavenum = float(wavestr)
        x.append(wavenum)
        absorb = item[seg:int(len(item)-1)] #10->11 wenn ir
        absorbnum = float(absorb) 
        y.append(absorbnum)
    return x,y

def substract_bg(x,y,xbg,ybg,scale):
    newx = []
    newy = []
    for c in range(len(x)):
        newxval = x[c]
        newx.append(newxval)
        newyval = y[c]- scale* ybg[c]
        newy.append(newyval)
    
    return newx, newy


#Korrektur des Datensatzes um Hintergrund
def backgroundwash(low_wav,high_wav,data_2d_array,background_path,scale):
    wavenums = data_2d_array[0]
    barray = import_dpt(low_wav,high_wav,background_path)
    #darray = np.array([])
    darray = np.zeros(shape=(2,len(data_2d_array[0])))
    #print(darray)
    for c in range(len(data_2d_array[0])):
        new_abs = data_2d_array[1][c] - scale*barray[1][c] 
        darray[0][c] = data_2d_array[0][c]
        darray[1][c] = new_abs
    
    return darray

def peakfinder(d2d_array,peaknumber,iterblocksize):
    peaknumber = int(peaknumber)
    def peaker(width):
        global peaks
        peaks_x = []
        peaks_y = []
        for c in range(len(d2d_array[1])):
            low = c-width
            if low <0:
                low=0
            high = c+width
            if high > len(d2d_array[1]):
                high = len(d2d_array[1])
            iteration_block = d2d_array[1][low:high]
            #print(iteration_block)
            if max(iteration_block) == d2d_array[1][c]:
                peaks_x.append(d2d_array[0][c])
                peaks_y.append(d2d_array[1][c])
        
        peaks = np.array([peaks_x,peaks_y])

    iter = iterblocksize
    peaker(iter)

    while len(peaks[1]) > peaknumber:
        iter = iter + 1
        peaker(iter)
        
    print(iter)

    return peaks



def mean(low_wav, high_wav,data_list_input):
    array_calc = data_list_input[0]
    data = array_calc[0]
    print(type(data))
    mean_spectra = []
    for i in range(len(data)):
        val = 0
        for a in range(len(data_list_input)):
            val = val + (data_list_input[a])[1][i]

        mean_val = val/len(data_list_input)
        mean_spectra.append(mean_val)
    
    return mean_spectra


def correlate(data_list_input,mean_spec):
    def get_opt_scale(scale_list,data_list):
        residue = []
        print(scale_list)
        for c in range(len(scale_list)):
            diff_list = []
            for i in range(len(data_list)):
                diff = data_list[i]*scale_list[c] - mean_spec[i]
                diff_list.append(np.abs(diff))
            res= sum(diff_list)
            residue.append(res)

        min_val = min(residue)
        #print(residue)
        index = residue.index(min_val)
        scale = scale_list[index]
        
        return scale

    scale_array = np.linspace(0.8,1.2,1000)
    data_scaled_list = []
    for a in range(len(data_list_input)):
        data_list = data_list_input[a][1]
        sc_val = get_opt_scale(scale_array,data_list)
        data_list = data_list*sc_val
        for c in range(len(data_list)):
            data_list_input[a][1][c] = data_list[c]
    
    data_scaled_list = data_list_input

    return data_scaled_list , sc_val


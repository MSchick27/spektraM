def init():
    init_dict = {
        'xlabel': 'wavenumbers [1/cm]',
        'ylabel': r'$\Delta$ abs. [mOD]',
        'xhigh': 4000,
        'xlow' : 1000,
        'yhigh': 1500 ,
        'ylow' : -500,
        'ymulti':1000
        }

    return init_dict

def spectra():
    spectra_dict = {
    'bsp_data': {'xdata': [],
                'ydata': [],
                'bg_xdata':[],
                'bg_ydata':[],
                'show': True,       #default
                'color': 'black',    #default
                'linewidth': 0.9     #default
                },
    'bsp_dat32': '',
    'bsp_data3':''}
    return spectra_dict
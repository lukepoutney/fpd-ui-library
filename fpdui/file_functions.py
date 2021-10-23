from imports import *

#imports either a mib or HDF5 file
def getMerlinOrHDF5():
    filepath = filedialog.askopenfilename(title = "Select MERLIN or HDF5 file", filetypes = (("MERLIN binary files","*.mib"),("MERLIN binary files","*.hdf5"),("all files","*.*")))
    #compares file type to allow for appropriate processing
    if filepath[-1] == "5":
        variables['HDF5f'] = filepath
        getHDF5File()
    elif filepath[-1] == "b":
        variables['MBpath'] = filepath
        getMerlinFile()
    else:
        return

#Processes the input of a mib file
def getMerlinFile():
    print (variables['MBpath'])
    if variables['MBpath'] == '':
        return 0
    bp , fne = os.path.split(variables['MBpath'])
    fn = os.path.splitext(fne)[0]
    variables['MBf'] = os.path.join(bp, fn+'.mib')
    variables['HDRf'] = os.path.join(bp, fn+'.hdr')
    if settings.settings['use_dmi'] == 0:
        getDMIFile()

#imports and processes a dmi file
def getDMIFile():
    #check if a merlin binary file is already present
    if variables.__contains__('MBf'):
        #check if the user wishes to use a dmi file
        if settings.settings["use_dmi"] == 1:
            #get dmi file if there currently isnt one
            if 'DMIf' not in variables or variables['DMIf'] == "":
                variables['DMIf'] = filedialog.askopenfilename(title = "Select *.dm3 file", filetypes = (("Digital Micrograph files","*.dm3"),("all files","*.*")))
                if variables['DMIf'] == '':
                    return 0
            print(variables['DMIf'])
            #combine dmi and merlin binary file
            mb = MerlinBinary(variables['MBf'], variables['HDRf'], variables['DMIf'], row_end_skip=1)
            variables['ds'] = mb.get_memmap()

        else:
            #If a dmi is not defined, get appropriate sizes
            checkNoDMI()
            #combine with merlin binary file
            mb = MerlinBinary(variables['MBf'], variables['HDRf'], [],
                scanYalu=(settings.settings['db_x_size'], 'y', 'na'),
                scanXalu=(settings.settings['db_y_size'], 'x', 'na'), row_end_skip=1)
            variables['ds'] = mb.get_memmap()

    else:
        a=tk.messagebox.askyesno('tip', 'You have not opened a MERLIN file.\nDo you want to open one?')
        if a :
            getMerlinFile()
            getDMIFile()

#Open a DMI file and override the settings if successful
def openDMI():
    variables['DMIf'] = filedialog.askopenfilename(title = "Select *.dm3 file", filetypes = (("Digital Micrograph files","*.dm3"),("all files","*.*")))
    if variables['DMIf'] == '':
        return 0
    mb = MerlinBinary(variables['MBf'], variables['HDRf'], variables['DMIf'], row_end_skip=1)
    variables['ds'] = mb.get_memmap()
    settings.settings["use_dmi"] = 1
        
#get required sizes
def checkNoDMI():
    #if sizes are not defined in settings, from the user
    if settings.settings['db_x_size'] == -1:
        b=tk.messagebox.askyesno('tip', 'No x size defined.\nDefine one now?\nThis can be changed later in the settings menu.')
        if b:
            settings.settings['db_x_size'] = simpledialog.askinteger('tip', 'Enter a value to define x-size')
        else:
            return
    if settings.settings['db_y_size'] == -1:
        b=tk.messagebox.askyesno('tip', 'No y size defined.\nDefine one now?\nThis can be changed later in the settings menu.')
        if b:
            settings.settings['db_y_size'] = simpledialog.askinteger('tip', 'Enter a value to define y-size')
        else:
            return

#Processes the input of a hdf5 file
def getHDF5File():
    print (variables['HDF5f'])
    print("This may take a moment, please be patient")
    with h5py.File(variables['HDF5f'], 'r') as f:
        variables['ds'] = f['fpd_expt/fpd_data/data'][()]
        variables['sum_im'] = f['fpd_expt/fpd_sum_im/data'][()]
        variables['sum_dif'] = f['fpd_expt/fpd_sum_dif/data'][()]
    print("Loading complete")
from ui_functions import *
from browse_functions import *
from dpc_functions import *
from df_functions import *

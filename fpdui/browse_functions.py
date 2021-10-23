from imports import *

def browseData():

    # open databrowser
    variables['browser'] = capture_display(DataBrowser,"Browser",variables['ds_sel'], nav_im=variables["sum_im"])

    # connect the graphs together so they are interactive
    variables['browser'].connect()


def getDataSet():
    real_skip = settings.settings["Down-sampling"]["real_skip"]
    recip_skip = settings.settings["Down-sampling"]["recip_skip"]
    if 'ds' not in variables:
        getMerlinOrHDF5()
        if 'MBf' not in variables and 'HDF5f' not in variables:
            return

        if 'HDF5f' not in variables:
            if settings.settings["use_dmi"] == 0:
                checkNoDMI()
                mb = MerlinBinary(variables['MBf'], variables['HDRf'], [], scanYalu=(settings.settings['db_y_size'], 'y', 'na'), scanXalu=(settings.settings['db_x_size'], 'x', 'na'), row_end_skip=1)
                if settings.settings['db_y_size'] <= 0 or settings.settings['db_x_size'] <= 0:
                    return
                variables['ds'] = mb.get_memmap()
            else:
                getDMIFile()
        if 'ds' not in variables:
            return
    # Calculate ds_sel
    variables['ds_sel'] = variables['ds'][::real_skip, ::real_skip, ::recip_skip, ::recip_skip]
    calculate_sum_im()
    calculate_sum_dif()

def calculate_sum_im():
    variables['sum_im'] = fpdp.sum_im(variables['ds_sel'], 16,16)

def calculate_sum_dif():
    variables['sum_dif'] = fpdp.sum_dif(variables['ds_sel'], 16,16)


from ui_functions import *
from file_functions import *
from dpc_functions import *
from df_functions import *

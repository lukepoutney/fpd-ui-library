from imports import *

# find the matching images
def find_matching_images():
    ap = None

    # user choice to use aperture
    if 'ap' in variables:
        if tk.messagebox.askyesno("Use Aperture?", "Would you like to use the current aperture for this function?"):
            ap = variables['ap']

    try:
        ds_sel = variables['ds_sel']
        if settings.settings["advanced_options"]:
            returns=matching_region_option()
            if returns[0] != None:
                variables['matching' ]= capture_display(fpdp.find_matching_images,"Matching image",ds_sel[returns[0]:returns[1], returns[2]:returns[3]], aperture=ap, plot=TRUE)
        else:
            variables['matching']=capture_display(fpdp.find_matching_images,"Matching image",ds_sel[:10, :10], aperture=ap, plot=TRUE)
    except MemoryError:
        tk.messagebox.showerror("error", "Unable to store image in RAM, reduce size")

# find the disc centre of matching images
def find_disc_centre():
    #image = matching.ims_common.mean(0)
    image = variables['matching'].ims_common * variables['ap']
    variables['image']=image.mean(0)
    #here should show images
    if settings.settings["advanced_options"]:
        returns = disc_centre_option()
        if returns[0] != None:
            variables['cyx_phase'],variables['cr_phase']= capture_display(fpdp.find_circ_centre,'Disc centre',variables['image'], sigma=returns[0], rmms=(returns[1],returns[2], returns[3]))
    else:
        rmms = (5, max(variables['ds'].shape[-2:])/settings.settings["Down-sampling"]["recip_skip"], 1)
        variables['cyx_phase'],variables['cr_phase'] = capture_display(fpdp.find_circ_centre,'Disc centre',variables['image'], sigma=2, rmms=rmms)

# run fpd disc edge sigma function
def find_edge_sigma():
    if settings.settings['advanced_options']:
        returns = edge_sigma_option()
        if returns[0] != None:
            variables['edge_sigma'] = capture_display(fpdp.disc_edge_sigma,'Edge sigma',variables['image'], sigma=returns[0], cyx=variables['cyx_phase'], r=variables['cr_phase'], plot=TRUE)[0]
    else:
        variables['edge_sigma'] = capture_display(fpdp.disc_edge_sigma,'Edge sigma',variables['image'], sigma=2, cyx=variables['cyx_phase'], r=variables['cr_phase'], plot=TRUE)[0]

# run fpd make ref image function
def create_ref_image():
    if settings.settings['advanced_options']:
        returns = ref_image_option()
        if returns[0] != None:
            if returns[1]==0:
                variables['ref_im'] = capture_display(fpdp.make_ref_im,"ref image", variables['image'], edge_sigma=returns[0], aperture=None, bin_opening=returns[2], bin_closing=returns[3], plot=TRUE)
            variables['ref_im'] = capture_display(fpdp.make_ref_im,"ref image", variables['image'], edge_sigma=returns[0], aperture=returns[1], bin_opening=returns[2], bin_closing=returns[3], plot=TRUE)
    else:
        variables['ref_im'] = capture_display(fpdp.make_ref_im,"ref image", variables['image'], edge_sigma=1.2, aperture=None, bin_opening=0, bin_closing=4, plot=True)

# run fpd phase_correlation function
def phase_correlation_basic():
    if settings.settings['advanced_options']:
        returns = phase_correlation_option()
        if returns[0] != None:   
            shift_yx, shift_err, shift_difp, ref = fpdp.phase_correlation(variables['ds_sel'], nc=returns[0], nr=returns[1], spf=returns[2], ref_im=variables['ref_im'],cyx=[returns[3],returns[4]], crop_r=returns[5], sigma=returns[6],parallel=FALSE)
            
    else:
        shift_yx, shift_err, shift_difp, ref = fpdp.phase_correlation(variables['ds_sel'], nc=16, nr=16, spf=100, ref_im=variables['ref_im'],cyx= variables['cyx_phase'], crop_r=variables['cr_phase'], sigma=variables['edge_sigma']*1.5,parallel=FALSE)
    capture_display(plt.matshow,"Phase the correlation",ref)
    variables['shift_yx']=shift_yx
    variables['shift_difp']=shift_difp
    variables['shift_err']=shift_err

# descan correct data
def descan_correction_phase():
    generic_descan_correction("shift_yx","shift_yx_cor","Succesfully corrected : stored as Shift yx corrected")

# magnetic correct data
def magnetic_correction_phase():
    generic_magnetic_correction("shift_yx_cor","shift_yx_beta","Successfully corrected : stored as Shift yx beta")

# image rotate data
def image_rotation_phase():
    generic_image_rotation("shift_yx_beta","shift_yx_rot","Successfully corrected : stored as Shift yx beta rotated")

# use dpc explorer to browse phase cor
def phase_browse_CoM():
    from dpc_explorer_class import DPC_Explorer
    cmap, choice = dpc_options_phase()
    if choice == "Shift yx":
        input_value = "shift_yx"
    elif choice == "Shift yx corrected":
        input_value = "shift_yx_cor"
    elif choice == "Shift yx beta":
        input_value = "shift_yx_beta"
    elif choice == "Shift yx beta rotated":
        input_value = "shift_yx_rot"
        
    global_name=input_value+' DPC'
    
    if input_value == 'shift_yx_beta':
        cyx,vectrot, gaus,pct = DPC_beta('default_list13')
        variables[global_name] = capture_display(DPC_Explorer, input_value+" DPC Explorer", variables[input_value], cmap=cmap,cyx=cyx,vectrot=vectrot,gaus=gaus,pct=pct)
    elif input_value == 'Comparisons':
        cyx,vectrot,gaus,pct = DPC_beta('default_list14')
        variables[global_name] = capture_display(DPC_Explorer, 'Comparisons',variables['pd'],cmap=cmap,cyx=cyx,vectrot=vectrot,gaus=gaus,pct=pct)
    else:
        variables[global_name] = capture_display(DPC_Explorer, input_value+" DPC Explorer", variables[input_value], cmap=cmap)

    DPC_connect(variables[global_name])

# explore 4d data
def DPC_4d():
    if 'shift_yx_beta DPC' in variables:
        # open databrowser
        variables['4D-browser'] = capture_display(DataBrowser,"4D-Browser",variables['ds'], nav_im=variables['shift_yx_beta DPC'].tr_im)

        # connect the graphs together so they are interactive
        variables['4D-browser'].connect()
    else:
        tk.messagebox.showinfo('No shift_yx_beta DPC data','Error, you must visualise shift yx beta using the dpc explorer before running this function.')
from file_functions import *
from browse_functions import *
from dpc_functions import *
from ui_functions import *

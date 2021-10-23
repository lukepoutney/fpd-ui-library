from imports import *

# find the diffraction center of the summed diffractions
def find_diffraction_center():
        
    recip_skip = settings.settings["Down-sampling"]["recip_skip"]
    sigma = 2
    rmms = (5, max(variables['ds'].shape[-2:])/recip_skip, 1)
    if settings.settings["advanced_options"]:
        sigma, rmms = fdc_options(sigma,rmms[0],int(rmms[1]),rmms[2])
        if sigma != None:
            variables['cyx'],variables['cr'] = capture_display(fpdp.find_circ_centre, "Circle center", variables['sum_dif'], sigma = sigma, rmms = rmms)
    else: 
        variables['cyx'],variables['cr'] = capture_display(fpdp.find_circ_centre, "Circle center", variables['sum_dif'], sigma = sigma, rmms = rmms)         

# generate an aperture on the current dataset
def generate_aperture():
    if settings.settings["advanced_options"]:
        params = aperture_options(variables["cyx"], variables["cr"])
        if params[0] != None:
            variables['ap'] = fpdp.synthetic_aperture(variables['ds_sel'].shape[-2:], cyx=params[0], rio=(params[1], params[2]), sigma=params[3], aaf=params[4])[0]
            capture_display(plt.matshow,"Aperture",variables['ap'])
    else:
        variables['ap'] = fpdp.synthetic_aperture(variables['ds_sel'].shape[-2:], cyx=variables['cyx'], rio=(0, variables['cr']+1), sigma=0, aaf=1)[0]
        capture_display(plt.matshow,"Aperture",variables['ap'])

# calculate the centre of mass given dataset
def calculate_CoM():
    ap = None
    if 'ap' in variables and not variables['test']:
        if tk.messagebox.askyesno("Aperture", "Would you like to use the most recently calculated aperture?"):
            ap = variables["ap"]
    if 'ap' in variables and variables['test']:
        ap=variables['ap']
    variables['com_yx'] = fpdp.center_of_mass(variables['ds_sel'], nr=16, nc=16, thr='otsu', aperture=ap, parallel = False)
    if not variables["test"]:
        create_text_tab('Calculate the mass',variables['com_yx'])

# descan correct the centre of mass
def descan_correction():
    generic_descan_correction("com_yx","com_yx_cor","Successfully corrected : stored as Centre of Mass Corrected")

# magnetic correct the centre of mass
def magnetic_correction():
    generic_magnetic_correction("com_yx_cor","com_yx_beta","Successfully corrected : stored as Centre of Mass beta")

# rotate the centre of mass
def image_rotation():
    generic_image_rotation("com_yx_beta","com_yx_rot","Successfully corrected : stored as Centre of Mass beta Rotated")

# perform descan correction on the data in, save to the data out, and display the message when completed successfully
# this is left generic so DPC and phase correlation can use the same functions
def generic_descan_correction(data_in, data_out, message):
    thresh = 0.1
    if settings.settings["advanced_options"]:
        thresh = descan_options()
        if thresh != None:
            fit = capture_display(ransac_im_fit,"Correction",variables[data_in], residual_threshold = thresh, plot = True)[0]
            variables[data_out] = variables[data_in] - fit
            

    else:
        fit = capture_display(ransac_im_fit,"Correction",variables[data_in], residual_threshold = thresh, plot = True)[0]
        variables[data_out] = variables[data_in] - fit
    print(message)

# perform magnetic correction on the data in, save to the data out, and display the message when completed successfully
# this is left generic so DPC and phase correlation can use the same functions
def generic_magnetic_correction(data_in, data_out, message):
    scalar = 1e9
    if variables["test"] is not None:
        scalar = magnet_corr_options()
    variables[data_out] = fpd.mag_tools.beta2bt(variables[data_in])
    print(message)

# perform image rotation on the data in, save to the data out, and display the message when completed successfully
# this is left generic so DPC and phase correlation can use the same functions   
def generic_image_rotation(data_in, data_out, message):
    angle = 0.0
    axes = (-2,-1)
    reshape = False
    order = 3
    mode = "constant"
    cval=0.0
    prefilter=True
    if variables['test'] is not None:
        angle, axes, reshape, order, mode, cval, prefilter = image_rot_options()
    variables[data_out] = sp.ndimage.rotate(variables[data_in], angle=angle, axes=axes, reshape=reshape, order=order, mode=mode, cval=cval, prefilter=prefilter)
    print(message)

# browse the centre of mass using one of the calculated variables
def browse_CoM():
    from dpc_explorer_class import DPC_Explorer
    if not variables['test']:
        cmap, choice = dpc_options()
    else:
        cmap = "viridis"
        choice = "Center of mass"
    if choice == "Center of mass":
        global_name= "com_DPC"
        input_value = "com_yx"
    elif choice == "Center of mass descan corrected":
        global_name= "com_yx_cor_DPC"
        input_value = "com_yx_cor"
    elif choice == 'Center of mass magnetic corrected':
        global_name= "com_yx_beta_DPC"
        input_value = "com_yx_beta"
    else:
        global_name = "com_yx_beta_rot_DPC"
        input_value = "com_yx_beta_rot"
    if input_value not in variables:
        try:
            tk.messagebox.showerror('Input error','You have not calculated : '+choice)
        except:
            tk.messagebox.showerror("Input Error","You have not inputted any data")
    else:
        if input_value == 'com_yx_beta':
            cyx,vectrot, gaus,pct = DPC_beta('default_list12')
            variables[choice] = capture_display(DPC_Explorer, input_value+" DPC Explorer", variables[input_value], cmap=cmap,cyx=cyx,vectrot=vectrot,gaus=gaus,pct=pct)
        else:
            variables[choice] = capture_display(DPC_Explorer, input_value+" DPC Explorer", variables[input_value], cmap=cmap)

    if not variables["test"]:
        DPC_connect(variables[choice])

# connect the DPC graphs together 
def DPC_connect(explorer):
    canvas_xy = variables['recent_canvases'][3]
    canvas_hist = variables['recent_canvases'][2]
    cnct = explorer._rect.figure.canvas.mpl_connect
    cnct_key = canvas_xy.mpl_connect
        
    explorer._cidpress = cnct('button_press_event', explorer._on_press)
    explorer._cidrelease = cnct('button_release_event', explorer._on_release)
    explorer._cidmotion = cnct('motion_notify_event', explorer._on_motion)
    explorer._keypress = cnct_key('key_press_event', explorer._on_keypress)
    explorer._keyrelease = cnct_key('key_release_event', explorer._on_keyrelease)
    explorer._scroll = cnct('scroll_event', explorer._on_scroll)

    # add buttons, selector, and sliders to graphs
    recreate_button(explorer)
    recreate_selector(explorer)
    recreate_sliders(explorer)

# manually recreate DPC selector
def recreate_selector(exp_variable):
    exp = exp_variable
    canvas_xy = variables['recent_canvases'][3]
    canvas_hist = variables['recent_canvases'][2]
    
    exp._xy_selector = RectangleSelector(canvas_xy.figure.get_axes()[0], 
                                             exp._xy_select_callback,
                                             drawtype='box',
                                             useblit=False,
                                             button=[1, 3],
                                             minspanx=5, 
                                             minspany=5,
                                             spancoords='pixels',
                                             interactive=True)      
        
        
    canvas_xy.mpl_connect('key_press_event', exp._on_xy_plot_key)
    canvas_xy.mpl_connect(exp._xy_selector.onmove, exp._update_hist_plot)

# manually recreate DPC sliders
def recreate_sliders(exp_variable):
    exp = exp_variable

    exp._sgaus.ax.remove()
    exp._svectrot.ax.remove()

    canvas_hist = variables['recent_canvases'][2]
    plt.figure(canvas_hist.figure.number)

    exp._axgaus = mplplt.axes([0.1, 0.1, 0.65, 0.03], facecolor = "lightgoldenrodyellow")
    exp._axvectrot = mplplt.axes([0.1, 0.15, 0.65, 0.03], facecolor = "lightgoldenrodyellow")

    exp._sgaus = Slider(exp._axgaus, 'Gaus.', 0.0, exp._gaus_lim,
                        valinit=exp._gaus)
    
    exp._svectrot = Slider(exp._axvectrot, 'Rot.', 0.0, 360.0,
                           valinit=exp._vectrot)
    
    exp._sgaus.on_changed(exp._update_gaus)
    exp._svectrot.on_changed(exp._update_vectrot)

# manually recreate every button for DPC explorer
def recreate_button(exp_variable):
    exp = exp_variable
    
    bGY_ax = exp._bGY.ax
    exp._bGY = matplotlib.widgets.Button(bGY_ax,'Open Y')
    exp._bGY.on_clicked(exp._on_GY)

    bGX_ax = exp._bGX.ax
    exp._bGX = matplotlib.widgets.Button(bGX_ax,'Open X')
    exp._bGX.on_clicked(exp._on_GX)

    bYXr_ax = exp._bYXr.ax
    exp._bYXr = matplotlib.widgets.Button(bYXr_ax,'lim <- r')
    exp._bYXr.on_clicked(exp._on_YXr)
    exp._bYXr.ax.set_facecolor('green')

    bsave_ax = exp._bsave.ax
    exp._bsave = matplotlib.widgets.Button(bsave_ax,'Save')
    exp._bsave.on_clicked(exp._on_save)

    bclose_ax = exp._bclose.ax
    exp._bclose = matplotlib.widgets.Button(bclose_ax,'Close')
    exp._bclose.on_clicked(exp._on_close)

    bdt_ax = exp._bdt.ax
    exp._bdt = matplotlib.widgets.Button(bdt_ax,'R:dt')
    exp._bdt.on_clicked(exp._on_dt)

    bds_ax = exp._bds.ax
    exp._bds = matplotlib.widgets.Button(bds_ax,'R:DS')
    exp._bds.on_clicked(exp._on_ds)

    bsig_ax = exp._bsig.ax
    exp._bsig = matplotlib.widgets.Button(bsig_ax,'R:sig')
    exp._bsig.on_clicked(exp._on_sig)

    bvec_ax = exp._bvec.ax
    exp._bvec = matplotlib.widgets.Button(bvec_ax,'R:rot')
    exp._bvec.on_clicked(exp._on_vec)

    brmin_ax = exp._brmin.ax
    exp._brmin = matplotlib.widgets.Button(brmin_ax,'R:rmin')
    exp._brmin.on_clicked(exp._on_r_min)

    bran_ax = exp._bran.ax
    exp._bran = matplotlib.widgets.Button(bran_ax,'Ran.')
    exp._bran.on_clicked(exp._on_ransac)
    exp._bran.ax.set_facecolor('green')

    bmed_ax = exp._bmed.ax
    exp._bmed = matplotlib.widgets.Button(bmed_ax,'Med.')
    exp._bmed.on_clicked(exp._on_median)
    exp._bmed.ax.set_facecolor('green')

    bprint_ax = exp._bprint.ax
    exp._bprint = matplotlib.widgets.Button(bprint_ax,'Prt')
    exp._bprint.on_clicked(exp._on_print)

    bwxy_ax = exp._bwxy.ax
    exp._bwxy = matplotlib.widgets.Button(bwxy_ax,'xy')
    exp._bwxy.on_clicked(exp._on_wxy)

    bflipy_ax = exp._bflipy.ax
    exp._bflipy = matplotlib.widgets.Button(bflipy_ax,'Flip Y')
    exp._bflipy.on_clicked(exp._on_flipy)
    exp._bflipy.ax.set_facecolor('green')

    bflipx_ax = exp._bflipx.ax
    exp._bflipx = matplotlib.widgets.Button(bflipx_ax,'Flip X')
    exp._bflipx.on_clicked(exp._on_flipx)
    exp._bflipx.ax.set_facecolor('green')
     
#rewriting the output of table function
def _print_shift_stats(shift_yx):
    ''' Prints statistics of 'shift_yx' array'''
    shift_yx_mag = (shift_yx**2).sum(0)**0.5
    shift_yxm = np.concatenate((shift_yx, shift_yx_mag[None, ...]), axis=0)
    
    non_yx_axes = tuple(range(1, len(shift_yxm.shape)))
    yxm_mn, yxm_std = shift_yxm.mean(non_yx_axes), shift_yxm.std(non_yx_axes)
    yxm_min, yxm_max = shift_yxm.min(non_yx_axes), shift_yxm.max(non_yx_axes)
    yxm_ptp = yxm_max - yxm_min
    
    variables['output']='{:10s}{:>8s}{:>11s}{:>11s}'.format('Statistics', 'y', 'x', 'm')+'\r\n'
    
    variables['output']+='{:s}'.format('-'*40)+'\r\n'
    variables['output']+='{:6s}: {:10.3f} {:10.3f} {:10.3f}'.format(*(('Mean',)+tuple(yxm_mn)))+'\r\n'
    variables['output']+='{:6s}: {:10.3f} {:10.3f} {:10.3f}'.format(*(('Min',)+tuple(yxm_min)))+'\r\n'
    variables['output']+='{:6s}: {:10.3f} {:10.3f} {:10.3f}'.format(*(('Max',)+tuple(yxm_max)))+'\r\n'
    variables['output']+='{:6s}: {:10.3f} {:10.3f} {:10.3f}'.format(*(('Std',)+tuple(yxm_std)))+'\r\n'
    variables['output']+='{:6s}: {:10.3f} {:10.3f} {:10.3f}'.format(*(('Range',)+tuple(yxm_ptp)))+'\r\n'
    return variables['output']

# create a text tab to output CoM data
def create_text_tab(tab_name,get):
    table_tab=new_graph_tab(tab_name)
    #mighty = ttk.LabelFrame(table_tab, text=box_text)
    #mighty.grid(column=0, row=0, padx=8, pady=4)
    tk.Label(table_tab,text=_print_shift_stats(get) ).grid(column=1, row=0)
    delete_button = ttk.Button(table_tab,text='quit tab', style='my.TButton', command=lambda: delete_tab(table_tab))
    delete_button.grid(column=1,row=1)


from ui_functions import *
from file_functions import *
from browse_functions import *
from df_functions import *

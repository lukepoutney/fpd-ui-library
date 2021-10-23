from imports import *

# calculate virtual annular darkfield given dataset and diffraction center
def calculateVADF():
    variables['VADF'] = fpdp.VirtualAnnularImages(variables['ds_sel'], nr=16, nc=16, cyx=variables['cyx'],parallel=False)

# save the vadf data (saves to current directory)
def saveVADF():
    variables['VADF'].save_data()

# load an NPZ file in as the VADF data
def loadVADF():
    NPZf= filedialog.askopenfilename(title = "Select NPZ file", filetypes = (("NPZ files","*.NPZ"),("all files","*.*")))
    variables['VADF']= fpdp.VirtualAnnularImages(NPZf)

# plot Virtual annular darkfield using a selected region as the navigation image
def plotVADF():
    choice = vadf_region_option()
    if choice[0] == "D":
        # sum image
        capture_display(variables['VADF'].plot,"VADF",nav_im=variables['sum_dif'])
    elif choice[0] == "M":
        # manual input
        y,x = plotVADF_options()
        capture_display(variables['VADF'].plot,"VADF",nav_im=variables['ds_sel'][y,x])
    else:
        # get from browser
        x = variables['browser'].scanXind
        y = variables['browser'].scanYind
        capture_display(variables['VADF'].plot,"VADF",nav_im=variables['ds_sel'][y,x])
    # connect graphs together
    DF_connect()

# connect the VADF graphs and add a save button
def DF_connect():
    variables['VADF']._f_nav.canvas.mpl_connect('scroll_event', variables['VADF']._onscroll)
    variables['VADF']._f_nav.canvas.mpl_connect('pick_event', variables['VADF']._onpick)

    b_save_ax = plt.axes([0.1,0.9, 0.1,0.075])
    variables['b_save'] = matplotlib.widgets.Button(b_save_ax,'Save')
    variables['b_save'].on_clicked(on_save)

    VADF_recreate_sliders()

# manually recreate sliders
def VADF_recreate_sliders():
    vadf = variables['VADF']

    vadf._sr1.ax.remove()
    vadf._sr2.ax.remove()
    vadf._sr3.ax.remove()
    
    axr1 = mplplt.axes([0.10, 0.05, 0.80, 0.03])
    axr2 = mplplt.axes([0.10, 0.10, 0.80, 0.03])
    axr3 = mplplt.axes([0.10, 0.15, 0.80, 0.03])
    
    val_max = vadf.r_pix.max()
    try:
        vadf._sr1 = Slider(axr1, 'r1', 0, val_max-1, valinit=vadf.r1, valfmt='%0.0f', valstep=1)
        vadf._sr2 = Slider(axr2, 'r2', 1, val_max, valinit=vadf.r2, valfmt='%0.0f', valstep=1)
    except AttributeError:
        vadf._sr1 = Slider(axr1, 'r1', 0, val_max-1, valinit=vadf.r1, valfmt='%0.0f')
        vadf._sr2 = Slider(axr2, 'r2', 1, val_max, valinit=vadf.r2, valfmt='%0.0f')
    vadf._sr3 = Slider(axr3, 'rc', 1, val_max, valinit=vadf.rc, valfmt='%0.1f')

    vadf._sr1.on_changed(vadf._update_r_from_slider)
    vadf._sr2.on_changed(vadf._update_r_from_slider)
    vadf._sr3.on_changed(vadf._update_rc_from_slider)

# save VADF to current directory as a numpy array and a bmp file
def on_save(event):
    # get virtual image
    vadf = variables['VADF']
    
    virtual_image = vadf.annular_slice(vadf.r1,vadf.r2)
    import datetime
    # save virtual image
    time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    if not os.path.exists("VADF"):
        os.mkdir("VADF")
        
    file_name = "VADF/VADF_" + time
    
    mplplt.imsave(file_name + ".bmp",
                  virtual_image)
    np.savetxt(file_name,
               virtual_image)

    tk.messagebox.showinfo("Saved VADF", "Successfully saved to " + file_name + " and " + file_name + ".bmp")
    
from file_functions import *
from browse_functions import *
from dpc_functions import *
from ui_functions import *

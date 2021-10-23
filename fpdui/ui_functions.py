from imports import *

# save settings and close the program
def end():
    matplotlib.pyplot.close('all')
    with open('settings.pickle', 'wb') as f:
        pickle.dump(settings.settings, f)
    quit()

# create the toolbar at the top of the screen
def add_menu(window):
    mainMenu = Menu(window)
    window.config(menu=mainMenu)

    fileMenu= Menu(mainMenu)
    mainMenu.add_cascade(label="File", menu = fileMenu)
    fileMenu.add_command(label="Open .mib or hdf5 file" , command = getMerlinOrHDF5)
    fileMenu.add_command(label="Open .dm3 file" , command = openDMI)
    fileMenu.add_command(label="Save/Load variables" , command = save_page.show_save_page)

    toolsMenu= Menu(mainMenu)
    mainMenu.add_cascade(label="Tools", menu = toolsMenu)
    toolsMenu.add_command(label="Options" , command = settings.show_settings)


# captures any matplotlib figures created by a function
# returns a 2d list with following structure
# [list of figures, list of returns of function]
def capture_mpl_fig(function, *args, **kwargs):
    curFigs = len(plt.get_fignums())
    returns = function(*args,**kwargs)
    newFigs = len(plt.get_fignums())
    figList = []
    for i in range(newFigs,curFigs,-1):
        figList.append(plt.figure(i))
    return [figList, returns]

# takes a function, a label, and arguments
# runs the function with the arguments passed
# returns the returns of that function
# captures all MPL figures and embeds them in a new tab
def capture_display(function, label, *args, **kwargs):

    # get the returns and the figure
    figList, returns = capture_mpl_fig(function, *args, **kwargs)
    # bypass graphics for tests

    if variables["test"] or settings.settings["plot_in_window"]:
        return returns
    
    # get the new tab
    from scrollable import ScrollableFrame
    tab = new_graph_tab(label)

    # get the size available to fit graphs in
    size_of_tab = variables['tabGraphs'].winfo_width()

    # create the (scrollable) frame to fit graphs in
    scroll_frame = ScrollableFrame(tab)
    scroll = scroll_frame.scrollable_frame
    scroll_frame.pack(fill="both", expand=1)
    
    from math import floor
    canvases = []

    rows = []

    
    for i in range(len(figList)):

        # two plots per row
        if i % 2 == 0:
            row_frame = Frame(master=scroll)
            row_frame.grid(row=floor(i/2),column=0)
            row_graphs = []
            rows.append(row_graphs)


        plot = figList[i]
        row_graphs.append(plot)
        
        # add a new frame for the toolbar
        plot_frame = Frame(master=row_frame,width = 300, height = 100)
        
        plot_frame.grid(row=1,column=0+(i%2))
        
                
        # embed the plot
        plot_canvas = FigureCanvasTkAgg(plot, master=plot_frame)
        plot_canvas.draw()
        canvases.append(plot_canvas)
        plot_canvas.get_tk_widget().pack()

        
        # add the toolbar
        plot_toolbar = NavigationToolbar2Tk(plot_canvas,plot_frame)
        plot_toolbar.update()

        # downsize the graphs to fit in the screen
        if len(row_graphs)==2:

            # get combined width of graphs in row
            graph_one = last_canvas.figure
            graph_two = plot_canvas.figure
            g1_size = graph_one.get_size_inches()
            g2_size = graph_two.get_size_inches()
            total_width = g1_size[0] * graph_one.get_dpi() + g2_size[0] * graph_two.get_dpi()

            # if the graphs are too wide, shrink them
            if total_width > size_of_tab:

                # shrink each graph by this scaling factor
                scaling_factor = ((size_of_tab / total_width) * graph_one.get_dpi()) - 6

                graph_one.set_dpi(scaling_factor)
                last_canvas.draw()
                one_canvas_width = g1_size[0] * scaling_factor
                one_canvas_height = g1_size[1] * scaling_factor
                last_canvas.get_tk_widget().config(width=one_canvas_width,height=one_canvas_height)
                
                graph_two.set_dpi(scaling_factor)
                plot_canvas.draw()
                two_canvas_width = g2_size[0] * scaling_factor
                two_canvas_height = g2_size[1] * scaling_factor
                plot_canvas.get_tk_widget().config(width=two_canvas_width,height=two_canvas_height)
                

        last_canvas = plot_canvas
    
        
    variables['recent_canvases'] = canvases

    # add quit tab button
    delete_button = ttk.Button(tab,text='quit tab', style='my.TButton', command=lambda: delete_tab(tab))
    delete_button.pack()

    # get the function that will be used to connect the graphs
    # if they are opened as a new window
    connect = None
    if isinstance(returns, DataBrowser):
        connect = returns.connect
    elif isinstance(returns, DPC_Explorer):
        connect = partial(DPC_connect,returns)
    elif label == "VADF":
        connect = DF_connect

    # add the open graphs as new window button
    new_window_button = ttk.Button(tab,text='Open window', style='my.TButton', command=lambda: new_window(canvases, tab, connect))
    new_window_button.pack()

    
    return returns

#Opens graphs into new window
def new_window(canvases, tab, connect):
    for canvas in canvases:
        #get figure
        figure = canvas.figure

        # make new window
        new_win = tk.Tk()
        
        # embed the plot
        plot_canvas = FigureCanvasTkAgg(figure, master=new_win)
        plot_canvas.draw()
        plot_canvas.get_tk_widget().pack()

    # close the old tab
    delete_tab(tab)

    # connect the graphs
    if connect is not None:
        connect()


    

# returns a new tab in the tab graphs tab controller with text 
def new_graph_tab(text):
    tabGraphs = variables['tabGraphs']
    tab = ttk.Frame(tabGraphs)
    tabGraphs.add(tab, text=text)
    tabGraphs.select(tab)
    return tab

# close given tab
def delete_tab(select_tab):
    tabGraphs=variables['tabGraphs']
    tabGraphs.forget(select_tab)

# create the tabs that will be used to run functions
def create_initial_tab(tabControl):
    tabs = {"Basic Data":
            {"Browse Data": browseData,
            "Find Diffraction Pattern Center": find_diffraction_center,
            "Generate an Aperture": generate_aperture,
             },
            "DPC Explorer":
            {"Calculate Center of Mass": calculate_CoM,
            "Descan Correction": descan_correction,
            "Magnetic Correction": magnetic_correction,
            "Image Rotation": image_rotation,
            "Browse Center of Mass": browse_CoM,
             },
             "Phase Correlation":
             {"Find similar images":find_matching_images,
             "Find disc centre":find_disc_centre,
             "Estimate the width":find_edge_sigma,
             "Create ref image":create_ref_image,
             "Basic phase correlation":phase_correlation_basic,
             },
             "DPC data view":
             {"Descan Correction": descan_correction_phase,
            "Magnetic Correction": magnetic_correction_phase,
            "Image Rotation": image_rotation_phase,
            "DPC Explorer":phase_browse_CoM,
            "Visualisation with the 4-D data":DPC_4d,
             },
            "VADF":
             {
            "Find Diffraction Pattern Center": find_diffraction_center,
            "Calculate VADF":calculateVADF,
            "Load VADF": loadVADF,
            "Save VADF": saveVADF,
            "Plot VADF": plotVADF,
            }
                }

    for tab in list(tabs.keys()):
        create_new_tab(tabControl, tab, tabs[tab])
    tabControl.grid(column=0, row=0, sticky="N")

# create a new tab in the given tabcontroller with the given name
# containing the given buttons
def create_new_tab(tabControl, tab_name, button_dict):

    tab = ttk.Frame(tabControl)
    tabControl.add(tab, text=tab_name)
    create_buttons(tab, button_dict)

# create a button for each function
def create_buttons(tab, button_dict):

    i = 3
    j = 0
    for b_name, func in button_dict.items():
        if b_name == "checkbox":
            button = Checkbutton(tab, text=func["text"], variable=func["var"])
        else:
            # run each function through the button runner function that checks its requirements are being met
            button = ttk.Button(tab, text=b_name, style='my.TButton', command=partial(button_runner,func))
        button.pack(side=TOP, pady=20)

        i += 1

    quit_button = ttk.Button(tab, text="Quit", style='my.TButton',
                                command=end)
    quit_button.pack(side=TOP, pady=20)

# given a command, ensure its requirements are met before it is run
def button_runner(command):
    # find all the sub requirements of command
    requirements = find_requirements(function_dict[command])
    # if the requirements are not being met, meet them
    for requirement in requirements:        
        if requirement not in variables:
            requirements_dict[requirement]()
        if requirement not in variables:
            tk.messagebox.showerror("Error",error_dict[requirement])
            return
    command()

# given a list of requirements, recursively find all of its subrequirments
# i.e. which variables must be calculated before it can be calculated
def find_requirements(req):
    new_reqs_found = False
    return_req = req[:]
    for requirement in req:
        try:
            subrequirements = function_dict[requirements_dict[requirement]]

            #iterate backwards to preserve correct requirement order
            for subreq in reversed(subrequirements):
                if subreq not in return_req:
                    return_req.insert(0, subreq)
                    new_reqs_found = True

        except:
            pass

    if new_reqs_found:
        return_req = find_requirements(return_req)
    
    return return_req
    
from file_functions import *
from browse_functions import *
from dpc_functions import *
from df_functions import *
from Phase_correlation_processing import *

# a map of functions to their requirement variables
function_dict = {
    browseData: ["ds_sel","sum_im","sum_dif"],
    generate_aperture: ["ds_sel","cyx"],
    calculate_CoM: ["ds","ds_sel"],
    descan_correction: ["com_yx"],
    magnetic_correction: ["com_yx_cor"],
    image_rotation: ["com_yx_beta"],
    browse_CoM: ["com_yx"],
    find_matching_images: ["ds_sel"],
    find_disc_centre: ["ap","matching"],
    find_edge_sigma: ["cyx_phase"],
    create_ref_image: ["edge_sigma"],
    phase_correlation_basic: ["ref_im"],
    descan_correction_phase: ["shift_yx"],
    magnetic_correction_phase: ["shift_yx_cor"],
    image_rotation_phase: ["shift_yx_beta"],
    phase_browse_CoM: ["shift_yx"],
    DPC_4d: [],
    find_diffraction_center: ["ds","sum_dif"],
    calculateVADF: ["ds_sel","cyx"],
    loadVADF: [],
    saveVADF: ["VADF"],
    plotVADF: ["sum_dif","VADF"]
    }


# map of keywords (variables) to the function that defines them
requirements_dict = {
    "ds":getDataSet,
    "ds_sel":getDataSet,
    "sum_im":calculate_sum_im,
    "sum_dif":calculate_sum_dif,
    "cyx":find_diffraction_center,
    "ap":generate_aperture,
    "com_yx":calculate_CoM,
    "com_yx_cor":descan_correction,
    "com_yx_beta":magnetic_correction,
    "matching":find_matching_images,
    "cyx_phase":find_disc_centre,
    "image":find_disc_centre,
    "edge_sigma":find_edge_sigma,
    "ref_im":create_ref_image,
    "shift_yx":phase_correlation_basic,
    "shift_yx_cor":descan_correction_phase,
    "shift_yx_beta":magnetic_correction_phase,
    "VADF":calculateVADF,
    }

# map of keywords to error messages if they are not defined
error_dict = {
    "ds":"A data set must be opened before functions can be run",
    "ds_sel":"A data set must be opened before functions can be run",
    "sum_im":"The summed images of the dataset are required for this function.",
    "sum_dif":"The summed diffractions of the dataset are required for this fucntion.",
    "cyx":"The centre of diffractions must be found before this function can be run",
    "com_yx":"The centre of mass must be found before this function can be run",
    "com_yx_cor":"The descan corrected centre of mass must be found before this function can be run",
    "com_yx_beta":"The magnetically corrected centre of mass must be found before this function can be run",
    "matching":"Matching images must be found before this function can be run",
    "cyx_phase":"The centre of the disc must be found before this function can be run",
    "ref_im":"A reference image must be created before this function can be run",
    "shift_yx":"Phase correlation must be run before this function can be run",
    "shift_yx_cor":"The descan corrected phase correlation must be found before this function can be run",
    "shift_yx_beta":"The magnetic corrected phase correlation must be found before this function can be run",
    "VADF":"Virtual Annular Darkfield must be found before this function can be run",
    }


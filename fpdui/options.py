from imports import *

class Options:

    def __init__(self):
        self.menu = Toplevel()
        self.entries = []
        self.current_row = 0
        self.outputs = []
        self.current_output = 0
        
    def add_int_field(self, label, default = None, info = None, maxi=None, mini=None, t=int):
        ttk.Label(self.menu, text=label, font=("Helvetica",18)).grid(row=self.current_row,column=0)
        self.outputs.append(None)
        newEntry = tk.Entry(self.menu)
        self.current_output+=1
        newEntry.grid(row=self.current_row, column=1)
        newEntry.insert(END,default)
        self.entries.append({"entry":newEntry,"max":maxi,"min":mini,"type":t})
        self.current_row+=1
        if(info != None):
            ttk.l=Label(self.menu, text=info, font=("Helvetica",12)).grid(row=self.current_row, column=0, columnspan=2)
            self.current_row += 1
            
    def add_choice(self, label, choices, info = None):
        ttk.Label(self.menu, text=label, font=("Helvetica",18)).grid(row=self.current_row,column=0)
        self.outputs.append(StringVar(self.menu))
        self.outputs[-1].set(choices[0])
        newOption = tk.OptionMenu(self.menu, self.outputs[self.current_output], *choices)
        self.current_output += 1
        newOption.grid(row = self.current_row, column=1)
        self.entries.append({"entry":newOption})
        self.current_row += 1
        if(info != None):
            ttk.Label(self.menu, text=info, font=("Helvetica",12)).grid(row=self.current_row, column=0, columnspan=2)
            self.current_row += 1
        
    def get(self):
        ttk.Button(self.menu,text="Ok", command=self.end).grid(row=self.current_row,column=1)
        self.menu.wait_window(self.menu)
        return self.outputs

    def end(self):
        for i in range(len(self.entries)):
            entry = self.entries[i]
            try:
                self.outputs[i] = entry["entry"].get()
            except:
                self.outputs[i] = self.outputs[i].get()
            if "type" in entry:
                try:
                    self.outputs[i] = entry["type"](self.outputs[i])
                except:
                    self.entries[i]["entry"].config(bg="red")
                    self.menu.focus_force()
                    tk.messagebox.showerror("Invalid Input", "One of the values you have entered is not a valid " + entry["type"].__name__, parent=self.menu)
                    return
            if "min" in entry:
                if entry["min"] is None:
                    continue
                if self.outputs[i] < entry["min"] or self.outputs[i] > entry["max"]:
                    entry["entry"].config(bg="red")
                    tk.messagebox.showerror("Invalid Input", "A value you have entered was outside the possible bounds [" + str(entry["min"]) + "," + str(entry["max"]) + "]", parent=self.menu)
                    return
        self.menu.destroy()

def aperture_options(cyx,r):
    options = Options()
    if 'default_list1' not in variables:
        variables['default_list1']=[cyx[0],cyx[1],0,r+8,0,1]
    options.add_int_field("Centre y", default = variables['default_list1'][0])
    options.add_int_field("Centre x", default = variables['default_list1'][1])
    options.add_int_field("Inner radius", default = variables['default_list1'][2])
    options.add_int_field("Outer radius", default = variables['default_list1'][3], info = "This field is usually slightly larger than the diffraction center radius which in this case is " + str(r))
    options.add_int_field("Sigma", default = variables['default_list1'][4])
    options.add_int_field("Anti-aliasing factor", default = variables['default_list1'][5])
    returns = options.get()
    if returns[0] != None:
        variables['default_list1']=returns
    else:
        tk.messagebox.showerror('Error','You have not input any data.')
    return [returns[0],returns[1]], returns[2], returns[3], returns[4], returns[5]

def plotVADF_options():
    options = Options()
    if 'default_list2' not in variables:
        variables['default_list2']=[0,0]
    options.add_int_field("y coord", default=variables['default_list2'][0], maxi = np.size(variables['ds_sel'],1) - 1, mini=0)
    options.add_int_field("x coord", default=variables['default_list2'][1], maxi = np.size(variables['ds_sel'],0) - 1, mini=0)
    returns = options.get()
    if returns[0] != None:
        variables['default_list2']=returns
    else:
        tk.messagebox.showerror('Error','You have not input any data.')
    return returns[0],returns[1]

def descan_options():
    options = Options()
    if 'default_list3' not in variables:
        variables['default_list3']=[0.1]
    options.add_int_field("Residual threshold", default = variables['default_list3'], info = "Maximum distance for a data point to be classified as an inlier", t=float)
    returns = options.get()
    if returns[0] != None:
        variables['default_list3']=returns
    else:
        tk.messagebox.showerror('Error','You have not input any data.')    
    return returns[0]

def vadf_region_option():
    options = Options()
    choices = ["Diffraction Sum", "Manually input Region"]
    if 'default_list_vadf' not in variables:
        variables['default_list_vadf'] = ["Diffraction Sum"]
    if 'browser' in variables:
        choices.append("Use data browser selection")
    options.add_choice("Nav Image Region", choices)
    returns = options.get()
    if returns[0] != None:
        variables['default_list_vadf'] = returns
    else:
        tk.messagebox.showerror('Error','You have not input any data.')    
    return returns[0]

def fdc_options(s,hmin,hmax,hradius):
    options = Options()
    if 'default_list4' not in variables:
        variables['default_list4']=[s,hmin,hmax,hradius]
    options.add_int_field("Sigma",default=variables['default_list4'][0])
    options.add_int_field("Hough minimum",default=variables['default_list4'][1])
    options.add_int_field("Hough maximum",default=variables['default_list4'][2])
    options.add_int_field("Hough radius",default=variables['default_list4'][3])
    returns = options.get()
    if returns[0] != None:
        variables['default_list4']=returns
    else:
        tk.messagebox.showerror('Error','You have not input any data.')
    return [returns[0],(returns[1],returns[2],returns[3])]

def dpc_options():
    options = Options()
    choices = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn','binary',
            'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink', 'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia','hot',
            'afmhot', 'gist_heat', 'copper', 'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu', 'RdYlGn', 'Spectral',
            'coolwarm', 'bwr', 'seismic', 'twilight', 'twilight_shifted', 'hsv', 'Pastel1', 'Pastel2', 'Paired', 'Accent',
            'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c', 'flag', 'prism', 'ocean', 'gist_earth',
            'terrain', 'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet',
            'nipy_spectral', 'gist_ncar']
    options.add_choice("Matplotlib cmap", choices)
    input_choices = ["Center of mass"]
    if 'com_yx_cor' in variables:
        input_choices.append("Center of mass descan corrected")
    if 'com_yx_beta' in variables:
        input_choices.append("Center of mass magnetic corrected")
    if 'com_yx_beta_rot' in variables:
        input_choices.append("Center of mass magnetic corrected and rotated")
    options.add_choice('Input value',input_choices)
    returns = options.get()
    return returns[0], returns[1]


def matching_region_option():
    options = Options()
    if 'default_list5' not in variables:
        variables['default_list5']=[0,variables['ds_sel'].shape[0],0,variables['ds_sel'].shape[1]]
    options.add_int_field('X-axis start',default=variables['default_list5'][0],info='Matching image range end point in x-axis',maxi=variables['ds_sel'].shape[0],mini=0)
    options.add_int_field('X-axis end',default=variables['default_list5'][1],info='Matching image range end point in x-axis',maxi=variables['ds_sel'].shape[0],mini=0)
    options.add_int_field('Y-axis start',default=variables['default_list5'][2],info='Matching image range end point in y-axis',maxi=variables['ds_sel'].shape[1],mini=0)
    options.add_int_field('Y-axis end',default=variables['default_list5'][3],info='Matching image range end point in y-axis',maxi=variables['ds_sel'].shape[1],mini=0)
    returns = options.get()
    if returns[0] != None:
        variables['default_list5']=returns
    else:
        tk.messagebox.showerror('Error','You have not input any data.')
    return returns

def disc_centre_option():
    options = Options()
    if 'default_list6' not in variables:
        variables['default_list6']=[2,14,int(max(variables['ds'].shape[-2:])/settings.settings["Down-sampling"]["recip_skip"]),1]
    options.add_int_field('Sigma',default=variables['default_list6'][0],t=float)
    options.add_int_field('Inner radius',default=variables['default_list6'][1])
    options.add_int_field("Outer radius",default=variables['default_list6'][2])
    options.add_int_field('Step radius',default=variables['default_list6'][3])
    returns = options.get()
    if returns[0] != None:
        variables['default_list6']=returns
    else:
        tk.messagebox.showerror('Error','You have not input any data.')
    return returns

def edge_sigma_option():
    options = Options()
    if 'default_list7' not in variables:
        variables['default_list7']=[2]
    options.add_int_field('Sigma',default=variables['default_list7'][0],t=float)
    returns = options.get()
    if returns[0] != None:
        variables['default_list7']=returns
    else:
        tk.messagebox.showerror('Error','You have not input any data.')
    return returns

def ref_image_option():
    options = Options()
    if 'default_list8' not in variables:
        variables['default_list8']=[1.2,1,0,4]
    options.add_int_field('Edge Sigma',default=variables['default_list8'][0],t=float)
    options.add_int_field('Aperture',default=variables['default_list8'][1])
    options.add_int_field('Bin opening',default=variables['default_list8'][2])
    options.add_int_field('Bing closing',default=variables['default_list8'][3])
    returns = options.get()
    if returns[0] != None:
        variables['default_list8']=returns
    else:
        tk.messagebox.showerror('Error','You have not input any data.')
    return returns

def phase_correlation_option():
    options = Options()
    if 'default_list9' not in variables:
        variables['default_list9']=[16,16,100,variables['cyx_phase'][0],variables['cyx_phase'][1],variables['cr_phase'],round(variables['edge_sigma']*1.5,2)]
    options.add_int_field('Nc',default=variables['default_list9'][0])
    options.add_int_field('Nr',default=variables['default_list9'][1])
    options.add_int_field('Spf',default=variables['default_list9'][2])
    options.add_int_field('Cyx start',default=variables['default_list9'][3])
    options.add_int_field('Cyx end',default=variables['default_list9'][4],info='Default value comes from last cyx')
    options.add_int_field('Crop_r',default=variables['default_list9'][5],info='Default value comes from last cr')
    options.add_int_field('Sigma',default=variables['default_list9'][6],t=float,info='Default value is 1.5*edge width')
    returns = options.get()
    if returns[0] != None:
        variables['default_list9']=returns
    else:
        tk.messagebox.showerror('Error','You have not input any data.')
    return returns

def magnet_corr_options():
    options = Options()
    if 'default_list10' not in variables:
        variables['default_list10'] = [1e9]
    options.add_int_field("Scalar", default=variables['default_list10'][0], t=float)
    returns = options.get()
    if returns[0] != None:
        variables['default_list10'] = returns
    else:
        tk.messagebox.showerror("Error","You have not input any data.")
    return returns[0]

def image_rot_options():
    options = Options()
    if 'default_list11' not in variables:
        variables['default_list11'] = [0.0,-2,-1,False,3,"constant",0.0,True]
    options.add_int_field("Angle", default=variables['default_list11'][0], t=float)
    options.add_int_field("Axis 1", default=variables['default_list11'][1])
    options.add_int_field("Axis 2", default=variables['default_list11'][2])
    options.add_choice("Reshape",["True","False"])
    options.add_int_field("Order", default=variables['default_list11'][4])
    options.add_choice("Mode", ["reflect","constant","nearest","mirror","wrap"])
    options.add_int_field("cval",default=variables['default_list11'][6],t=float)
    options.add_choice("Prefilter",["True","False"])
    returns = options.get()
    if returns[0] != None:
        variables['default_list11'] = returns
    else:
        tk.messagebox.showerror("Error","You have not input any data.")
    return [returns[0],[returns[1],returns[2]],returns[3],returns[4],returns[5],returns[6],returns[7]]

def DPC_beta(value_name):
    options=Options()
    if value_name not in variables:
        variables[value_name] = [0,0,125,0.0,0.5]
    options.add_int_field('cyx start',default=variables[value_name][0])
    options.add_int_field('cyx end',default=variables[value_name][1])
    options.add_int_field('vectrot',default=variables[value_name][2])
    options.add_int_field('gaus',default=variables[value_name][3],t=float)
    options.add_int_field('pct',default=variables[value_name][4],t=float)
    returns = options.get()
    if returns[0] != None:
        variables[value_name] = returns
    else:
        tk.messagebox.showerror("Error","You have not input any data.")
    return [[returns[0],returns[1]],returns[2],returns[3],returns[4]]

def dpc_options_phase():
    options = Options()
    choices = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn','binary',
            'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink', 'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia','hot',
            'afmhot', 'gist_heat', 'copper', 'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu', 'RdYlGn', 'Spectral',
            'coolwarm', 'bwr', 'seismic', 'twilight', 'twilight_shifted', 'hsv', 'Pastel1', 'Pastel2', 'Paired', 'Accent',
            'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c', 'flag', 'prism', 'ocean', 'gist_earth',
            'terrain', 'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet',
            'nipy_spectral', 'gist_ncar']
    options.add_choice("Matplotlib cmap", choices)
    input_choices = []
    if 'shift_yx' in variables:
        input_choices.append("Shift yx")
    if 'shift_yx_cor' in variables:
        input_choices.append("Shift yx corrected")
        if 'com_yx_cor' in variables:
            variables['pd']=np.array([variables['com_yx_cor'],variables['shift_yx_cor']])
            input_choices.append('Comparisons')
    if 'shift_yx_beta' in variables:
        input_choices.append("Shift yx beta")
    if 'shift_yx_beta_rot' in variables:
        input_choices.append("Shift yx beta rotated")
    options.add_choice('Input value',input_choices)
    returns = options.get()
    return returns[0], returns[1]

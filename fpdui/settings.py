from imports import *

class Settings:

    changed_sampling = False
    
    settings = {"Down-sampling":{"real_skip":1,"recip_skip" : 1},
                "db_x_size": -1,
                "db_y_size": -1,
                "plot_in_window": 0,
                "use_dmi": 1,
                "advanced_options": 1}
    
    def __init__(self, test=False):
        # Load settings from pickle file
        if not test:
            try:
                with open('settings.pickle', 'rb') as f:
                    self.settings = pickle.load(f)
            except:
                print("couldn't load settings")


    # Sets all options to a default value
    def reset_to_defaults(self):
        matplotlib.rcdefaults()
        plt.ioff()
        self.settings = {"Down-sampling":{"real_skip":1,"recip_skip" : 1},
                "db_x_size": -1,
                "db_y_size": -1,
                "plot_in_window": 0,
                "use_dmi": 1,
                "advanced_options": 1}
                
    
    # Each function here updates the associated variable in main as well as within
    # this class (so that they can be saved to file)

    def set_real_ds(self,x):
        if self.settings["Down-sampling"]["real_skip"] != x:
            self.changed_sampling = True
        self.settings["Down-sampling"]["real_skip"]=x
        
    def set_recip_ds(self,x):
        if self.settings["Down-sampling"]["recip_skip"] != x:
            self.changed_sampling = True
        self.settings["Down-sampling"]["recip_skip"]=x

    def set_x_size(self, x):
        self.settings["db_x_size"]=x

    def set_y_size(self, x):
        self.settings["db_y_size"]=x

    def set_plot_in_window(self, x):
        self.settings["plot_in_window"]=x
        variables["plot_in_window"] = x
        if x == 1:
            # Plots graphs in a separate window
            plt.ion()
        else:
            # Plots graphs in a tab
            plt.ioff()

    def set_use_dmi(self, x):
        self.settings["use_dmi"]= x
        variables["use_dmi"] = x

    def set_options(self, x):
        self.settings["advanced_options"]=x
        variables["advanced_options"] = x


    # Updates all settings variables and saves them to a file
    def saveSettings(self,window):
        # Get user's input from the textboxes/checkboxes
        self.set_real_ds(int(self.text1.get()))
        self.set_recip_ds(int(self.text2.get()))
        changedXY = False
        if int(self.text3.get()) != self.settings['db_x_size'] or int(self.text4.get()) != self.settings['db_y_size']:
            changedXY = True
        self.set_x_size(int(self.text3.get()))
        self.set_y_size(int(self.text4.get()))
        self.set_plot_in_window(checkboxes["plot_in_window"].get())
        self.set_use_dmi(checkboxes["use_dmi"].get())
        self.set_options(checkboxes["advanced_options"].get())

        # Save settings to file
        with open('settings.pickle', 'wb') as f:
            pickle.dump(self.settings, f)

        # Function call to update certain variables if the down sampling or data size
        # has been changed
        if self.changed_sampling:
            from browse_functions import getDataSet
            getDataSet()
            self.changed_sampling = False
        if changedXY:
            from file_functions import getDMIFile
            getDMIFile()

        # Close settings window
        window.destroy()

    # Display the settings menu
    def show_settings(self, test=False):
        top = Toplevel()
        top.title("Settings")

        # Tkinter IntVar variables must be initialised in a tkinter root
        checkboxes["use_dmi"] = IntVar(master=top)
        checkboxes["plot_in_window"] = IntVar(master=top)
        checkboxes["advanced_options"] = IntVar(master=top)


        # Don't run UI based code in tests
        if not test:
            # Load the settings file
            try:
                with open('settings.pickle', 'rb') as f:
                    self.settings = pickle.load(f)
            except:
                print("couldn't load settings")

            
            # Setup the checkboxes and associated variables
            try:
                checkboxes["use_dmi"].set(self.settings["use_dmi"])
                variables["use_dmi"] = self.settings["use_dmi"]
        
            except:
                checkboxes["use_dmi"].set(0)
            
            try:
                checkboxes["plot_in_window"].set(self.settings["plot_in_window"])
                variables["plot_in_window"] = self.settings["plot_in_window"]
            except:
                checkboxes["plot_in_window"].set(0)

            try:
                checkboxes["advanced_options"].set(self.settings["advanced_options"])
                variables["advanced_options"] = self.settings["advanced_options"]
            except:
                checkboxes["advanced_options"].set(0)


        # Create the labels and buttons/checkboxes
        self.label1 = Label(top,text="Real space downsampling:")
        self.text1 = Entry(top)
        self.text1.insert(END, self.settings["Down-sampling"]["real_skip"])
        self.label2 = Label(top,text="Reciprocal space downsampling:")
        self.text2 = Entry(top)
        self.text2.insert(END, self.settings["Down-sampling"]["recip_skip"])
        self.label3 = Label(top,text="DataBrowser x size:")
        self.text3 = Entry(top)
        self.text3.insert(END, self.settings["db_x_size"])
        self.label4 = Label(top,text="DataBrowser y size:")
        self.text4 = Entry(top)
        self.text4.insert(END, self.settings["db_y_size"])
        self.check1 = Checkbutton(top, text="Use DMI file?", variable=checkboxes["use_dmi"])
        self.check2 = Checkbutton(top, text="Plot graphs in a window?", variable=checkboxes["plot_in_window"])
        self.check3 = Checkbutton(top, text="Advanced options", variable=checkboxes["advanced_options"])

        self.button1 = Button(top,text="Save", command=lambda: self.saveSettings(top))

        # Display the labels and buttons/checkboxes in the window
        self.label1.grid(row=0, column=0, sticky=W)
        self.text1.grid(row=0, column=1)
        self.label2.grid(row=1, column=0, sticky=W)
        self.text2.grid(row=1, column=1)
        self.label3.grid(row=2, column=0, sticky=W)
        self.text3.grid(row=2, column=1)
        self.label4.grid(row=3, column=0, sticky=W)
        self.text4.grid(row=3, column=1)
        self.check1.grid(row=5, column=0, sticky=W)
        self.check2.grid(row=6, column=0, sticky=W)
        self.check3.grid(row=7, column=0, sticky=W)
        self.button1.grid(row=8, column=1)

settings = Settings()

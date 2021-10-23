from sys import platform

# Check requirements/dependencies are installed
try:
    from imports import *
except ImportError:
    import subprocess
    # If they're not, install for the given platform
    if platform == "darwin" or platform == "linux" or platform == "linux2":
        subprocess.run(["conda", "install", "--user", "-c", "numba", "llvmlite"])
        subprocess.run(["pip", "install", "--user", "-r", "requirements.txt"])
    elif platform == "win32":
        subprocess.call([r'installer.bat'])
    from imports import *



# Create subclass inheriting from tkinter root to allow for further customisation
class AppRoot(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "FPD GUI")
        try:
            self.state("zoomed")
        except:
            pass
        if platform == "linux" or platform == "linux2":
            w, h = self.winfo_screenwidth(), self.winfo_screenheight()
            self.geometry("%dx%d+0+0" % (w,h))
        
        if platform == "darwin":
            self.attributes("-fullscreen", True)
            self.attributes("-fullscreen", False)


        container = tk.Frame(self)
        #container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Allow for mutliple 'pages' to be setup.
        # This version contains only one page, however this remains to allow for future expansion
        self.frames= {}
        frame = StartPage(container, self)
        self.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        # Show the first page
        self.show_frame(StartPage)
        
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# Allows graphs to be plotted in-app instead of popping out in a window by default
plt.ioff()

if platform == "win32":
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

# Initialise the root window
app = AppRoot()

# Setup tabs to control each workflow (e.g. Browse Data, DPC Exploere, VADF etc.)
tabControl = ttk.Notebook(app)
create_initial_tab(tabControl)

# Setup tabs to control new graphs
tabGraphs = ttk.Notebook(app)
Grid.columnconfigure(app,1,weight=1)
tabGraphs.grid(row=0, rowspan = 2, column=1 ,columnspan=2, sticky="NEWS")

tabControl.update()
app.update()

# Setup in-app console view
console_height = app.winfo_height() - tabControl.winfo_height() - 40

consoleSpace = tk.Frame(app, width=tabControl.winfo_width(), height=console_height)
consoleSpace.pack_propagate(False)
consoleSpace.grid(row=1,column=0, sticky="NEWS")

scroll = ttk.Scrollbar(consoleSpace)
scroll.pack(side=RIGHT, fill=Y)

console = tk.Text(consoleSpace, yscrollcommand=scroll.set)
console.pack(fill=Y, expand=True)

scroll.config(command=console.yview)

sys.stdout = ConsoleDirector(console)
sys.stderr = ConsoleDirector(console)


variables['tabGraphs'] = tabGraphs

# Global variable for checking test features
variables['test'] = False

# Create options menu
add_menu(app)

# Start GUI
app.mainloop()

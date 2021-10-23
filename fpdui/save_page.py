from imports import *

class Save_page:
    def __init__(self):
        pass
            
    def show_save_page(self):
        top = Toplevel()
        top.title("Save or restore")
        nb = ttk.Notebook(top)
        nb.pack()
        
        savePage = ttk.Frame(nb)
        nb.add(savePage, text='Save')

        self.label1 = Label(savePage, text="Variables list:")
        self.listbox1 = Listbox(savePage)
        self.button1 = Button(savePage, text="Save", command= self.save, width = 8)
        
        self.label1.grid(row=0, column=0, sticky=W)
        self.listbox1.grid(row=1, column=0, sticky=W)
        self.button1.grid(row=2, column=0, sticky='NEW', padx=5, pady=5)

        loadPage = ttk.Frame(nb)
        nb.add(loadPage, text='Load')
        
        self.label2 = Label(loadPage, text="Variables list:")
        self.listbox2 = Listbox(loadPage)
        self.button2 = Button(loadPage, text="Load", command= self.load, width = 8)
        
        self.label2.grid(row=0, column=0, sticky=W)
        self.listbox2.grid(row=1, column=0, sticky=W)
        self.button2.grid(row=2, column=0, sticky='NEW', padx=5, pady=5)

        sessionPage = ttk.Frame(nb)
        nb.add(sessionPage, text='Sessions')

        self.label3 = Label(sessionPage, text="Save session as:")
        self.text1 = tk.Entry(sessionPage)
        self.button3 = Button(sessionPage, text="Save", command= self.saveSession, width = 8)
        self.label4 = Label(sessionPage, text="Load previous sessions:")
        self.listbox3 = Listbox(sessionPage)
        self.button4 = Button(sessionPage, text="Load", command= self.loadSession, width = 8)
        
        
        self.label3.grid(row=0, column=0, sticky=W)
        self.text1.grid(row=1, column=0, sticky=W)
        self.button3.grid(row=2, column=0, sticky='NEW', padx=5, pady=5)
        self.label4.grid(row=3, column=0, sticky=W)
        self.listbox3.grid(row=4, column=0, sticky=W)
        self.button4.grid(row=5, column=0, sticky='NEW', padx=5, pady=5)
        self.refresh()
        
    def saveToFile(self, vName, fName=""):
        if fName=="":
            fName=vName+".pkl"
        pickle.dump(variables[vName], open(fName, "wb"))
        self.refresh()

    def loadFromFile(self, vName, fName=""):
        if fName=="":
            fName=vName+".pkl"
        if os.path.exists(fName):
            try:
                variables[vName] = pickle.load(open(fName, "rb"))
            except Exception as e:
                tk.messagebox.showerror(title='Error', message=e)
        else:
            fName = filedialog.askopenfilename(title = "Select file")
            if fName != "":
                if vName == "":
                    path , name = os.path.split(fName)
                    vName = name.split(".")[0]
                self.loadFromFile(vName, fName)
        self.refresh()

    def save(self):
        try:
            self.saveToFile(self.listbox1.get(self.listbox1.curselection()),self.text1.get())
        except Exception as e:
            tk.messagebox.showerror(title='Error', message=e)

    def load(self):
        try:
            vName = self.listbox2.get(self.listbox2.curselection()).replace('.pkl','')
            self.loadFromFile(vName)
        except Exception as e:
            tk.messagebox.showerror(title='Error', message=e)

    def saveSession(self):
        if self.text1.get() != "":
            try:
                valids = []
                for variable in variables:
                    if variable not in ['tabGraphs','ds']:
                        try:
                            self.saveToFile(variable)
                            valids.append(variable)
                        except Exception as e:
                            print("Ecountered error while trying to save "+variable)
                            tk.messagebox.showerror(title='Error', message=e)
                pickle.dump(valids, open(self.text1.get()+'.session.pkl', "wb"))     
            except Exception as e:
                tk.messagebox.showerror(title='Error', message=e)
        else:
            tk.messagebox.showwarning(title='Warning', message='Please enter a session name!')
        self.refresh()

    def loadSession(self):
        if self.listbox3.curselection():
            try:
                valids = pickle.load(open(self.listbox3.get(self.listbox3.curselection()), "rb"))
                for variable in valids:
                    self.loadFromFile(variable)
                tk.messagebox.showinfo(title='Success', message='Session was loaded successfully!')
            except Exception as e:
                tk.messagebox.showerror(title='Error', message=e)
        else:
            tk.messagebox.showwarning(title='Warning', message='Please select a session!')
        self.refresh()

    def refresh(self):
        try:
            self.listbox1.selection_clear(0, END)
            self.refresh_variables_list()
        except Exception as e:
            tk.messagebox.showerror(title='Error', message=e)
        try:
            self.listbox2.selection_clear(0, END)
            self.find_saved_variables()
        except Exception as e:
            tk.messagebox.showerror(title='Error', message=e)
        try:
            self.listbox3.selection_clear(0, END)
            self.find_saved_sessions()
        except Exception as e:
            tk.messagebox.showerror(title='Error', message=e)

    def refresh_variables_list(self):
        self.listbox1.delete(0, tk.END)
        for variable in variables:
            if variable not in ['tabGraphs']:
                self.listbox1.insert(END, variable)

    def find_saved_variables(self):
        self.listbox2.delete(0, tk.END)
        files = [file for file in os.listdir(os.curdir) if '.pkl' in file and '.session' not in file]
        for file in files:
            self.listbox2.insert(END, file)

    def find_saved_sessions(self):
        self.listbox3.delete(0, tk.END)
        files = [file for file in os.listdir(os.curdir) if '.session.pkl' in file]
        for file in files:
            self.listbox3.insert(END, file)

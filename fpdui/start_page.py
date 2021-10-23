from imports import *  

class StartPage(tk.Frame):

    variables = {}
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Browse STEM Data", font=("Helvetica", 18))
        label.grid(pady=10, padx=10, row=0, column=0)
        
        s = ttk.Style()
        s.configure('my.TButton', font=('Helvetica', 14))


        



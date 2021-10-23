from imports import *

class ConsoleDirector(object):

    def __init__(self, widget):
        self.output = widget
        self.lastLineReturn = False
        self.lastLineLength = 0
        
    def write(self, s):

        if "\r" in s:
            if self.lastLineReturn:
                self.output.delete("insert-" + str(self.lastLineLength) + "c", END)
                self.output.update()
            self.lastLineReturn = True
        else:
            self.lastLineReturn = False
        self.output.insert(tk.INSERT, s)
        self.lastLineLength = len(s)
        self.output.update()

    def flush(self):
        pass

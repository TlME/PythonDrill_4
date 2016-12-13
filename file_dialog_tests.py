import os
import shutil
import time
from tkinter import *
from tkinter import ttk

class FileTransferGUI:
    def __init__(self, master):
        #Create a paned window to handle the file browsers
        self.fileBrowser = ttk.Frame(master)
        self.fileBrowser.pack()

        self.frame_source = ttk.Frame(self.fileBrowser)
        self.fileBrowser.add(self.frame_source)
        self.src_treeview = ttk.Treeview(self.frame_source)
        self.src_treeview.pack()
        
        #Destination file viewer
        self.frame_destination = ttk.Frame(self.fileBrowser)
        self.fileBrowser.add(self.frame_destination, weight = 2)
        self.dst_treeview = ttk.Treeview(self.frame_destination)
        self.dst_treeview.pack()

        
def main():
    root = Tk()
    fileGUI = FileTransferGUI(root)
    root.mainloop()

# module handling
if __name__ == "__main__": main()

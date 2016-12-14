#=================================
## Python Drill 4
# A file-handling GUI
# By Nick Henegar
#==============================================================================================
# Kind of messy implementation here. If I was to be producing this for some goal,
# I would have spent more time tidying up my code and applying better classical OO principles
# to the code design. However, this was an exercise to help gain a deeper understanding of
# the tkinter GUI creating functionality, and I feel like that was accomplished. I would have
# liked to make the GUI update the trees once a file tranfer occurred, but that would have
# required the creation of a compound function with rather finicky rules on operation.
# (Unless of course, I created a stand-alone 'refresh' button, but that seemed icky.)

# tl;dr - I don't want to spend more time on this to make it better.
#==============================================================================================

#imports
import os
import shutil
import time
from tkinter import *
from tkinter import ttk

#GUI Class
class FileTransferGUI:
    def __init__(self, master):
        self.currentTime = time.time()
        self.src = StringVar('')
        self.dst = StringVar('')
        self.selected = []
    #Styling the master window and the two slave frames
        master.title('File Transfer GUI')
       # master.resizable(True,True)
        master.configure(height = 1000, width = 1000, background = 'light blue')
        
        self.style = ttk.Style()
        self.style.configure('Header.TLabel', font = ('Arial', 20))
        #self.style.configure('recent.Treeview', foreground = "dark green")

        self.frame_header = ttk.Frame(master)
        self.frame_header.pack(fill = BOTH, expand = 1)
        # Adding pretty pictures (stored in same folder)
        self.header_img = PhotoImage(file = 'fileTransfer.gif')
        self.folder_img = PhotoImage(file = 'folder.gif')
        self.file_img = PhotoImage(file = 'file.gif')
        self.src_img = PhotoImage(file = 'src.gif')
        self.dst_img = PhotoImage(file = 'dst.gif')
        # Header
        ttk.Label(self.frame_header, image = self.header_img).grid(row = 0, column = 0, rowspan = 2)
        ttk.Label(self.frame_header, text = 'Basic File Transfer GUI', style = 'Header.TLabel').grid(row = 0, column = 1)
        ttk.Label(self.frame_header, wraplength = 300,
                  text = ("""Click on the source and destination buttons below to set directories for file transfer. Recently modified items will show up highlighted in green.
You can also manually choose which files to export by ctrl-clicking them before selecting the 'transfer' button at the bottom.""")).grid(row = 1, column = 1)
        #Content
        self.frame_content = ttk.Frame(master)
        self.frame_content.pack(fill = BOTH, expand = 1) 
        
        #Create a paned window to handle the file browsers
        self.fileBrowser = ttk.Frame(self.frame_content)
        self.fileBrowser.grid(row = 1, column = 0, columnspan = 2, sticky = E + W + N + S)
        self.fileBrowser.grid_rowconfigure(0, weight=1)
        self.fileBrowser.grid_columnconfigure(0, weight=1)
        #Source file viewer
        self.frame_source = ttk.Frame(self.fileBrowser, relief = SUNKEN)
        self.frame_source.grid(row = 0, column = 0, sticky = E + W + N + S)
        self.frame_source.grid_rowconfigure(0, weight=1)
        self.frame_source.grid_columnconfigure(0, weight=1)
        self.src_treeview = ttk.Treeview(self.frame_source, selectmode = 'extended')
        self.src_treeview.grid(row = 0, column = 0, sticky = E + W + N + S)
        self.src_treeview.grid_rowconfigure(0, weight=1)
        self.src_treeview.grid_columnconfigure(0, weight=1)
        #This scrollbar exists, but does nothing.
        self.scrollbar = ttk.Scrollbar(self.frame_source, orient = HORIZONTAL)
        self.scrollbar.grid(row = 1, column = 0, sticky = S)
        self.src_treeview.config(xscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.src_treeview.xview)
            # The genTrees function will tag appended tree widgets with the tag 'recent' if their associated file has been
            #   modified in the past 24 hours, this makes the treeview display their text in green.
        self.src_treeview.tag_configure('recent', foreground = 'dark green')

        #Destination file viewer
        self.frame_destination = ttk.Frame(self.fileBrowser, relief = SUNKEN)
        self.frame_destination.grid(row = 0, column = 1, sticky = E + W + N + S)
        self.dst_treeview = ttk.Treeview(self.frame_destination, selectmode = 'none')
        self.dst_treeview.grid(row = 0, column = 1, sticky = E + W + N + S)

         # Directory choice buttons
        self.srcButton = ttk.Button(self.frame_content, image = self.src_img, text = 'Source Directory',
                                    compound = LEFT, command = lambda: self.src.set(choose(self.src_treeview, self.file_img, self.folder_img, self.currentTime)))
        self.srcButton.grid(row = 0, column = 0)
        self.dstButton = ttk.Button(self.frame_content, image = self.dst_img, text = 'Destination Directory',
                                    compound = LEFT, command = lambda: self.dst.set(choose(self.dst_treeview, self.file_img, self.folder_img, self.currentTime)))
        self.dstButton.grid(row = 0, column = 1)
        self.transferButton  = ttk.Button(self.frame_content, text = 'Transfer',
                                    command = lambda: transfer(self.src.get(), self.dst.get(), self.currentTime))
        self.transferButton.grid(row = 2, column = 0, columnspan = 2)
        self.refreshButton = ttk.Button(self.frame_content, text = 'Refresh',
                                    command = lambda: transfer(self.src.get(), self.dst.get(), self.currentTime))
        
#====== Choose ============================================================================================
# @args -
    # src_treeview - the treeview widget that is to have elements appended
    # file_img, folder_img - two .gifs which distinguish files from folders (Must be in same folder as main)
    # currentTime - a time.time() object, used to track how recently something was modified
# @returns - src : a string that represents the filepath used to reach the chosen directory
#
# Usage - allows user to choose a directory to be indexed, drops the current treeview, then populates a new
#           treeview based off the files and folders contained within the target directory.
# !!! Will ignore the .git folder !!!
#===========================================================================================================
def choose(src_treeview, file_img, folder_img, currentTime):
    src = filedialog.askdirectory()
    src_treeview.delete(*src_treeview.get_children())
    #File Viewing utility:
    def genTrees(src_treeview, src, parent, file_img, folder_img, currentTime):
        i = 0
        children = os.listdir(src)
        for child in children:
            if child.endswith(".git"):
                continue
            try:
                test = os.listdir(src + "/" + child)
                src_treeview.insert(parent, 'end', parent + str(i), image = folder_img, text = child)
                genTrees(src_treeview, src + "/" + child,  parent + str(i), file_img, folder_img, currentTime)
            except (NotADirectoryError):
                recently_modified = ((currentTime - os.stat(src + "/" + child).st_mtime) <= 86400)
                if recently_modified:
                    src_treeview.insert(parent, 'end', parent + str(i), image = file_img, text = child, tags = 'recent')
                else:
                    src_treeview.insert(parent, 'end', parent + str(i), image = file_img, text = child)
            i += 1
    genTrees(src_treeview, src, '', file_img, folder_img, currentTime)
    return src

#==== Transfer Utility:=====================================================================================================
# @args -
    # src, dst - strings which represent the filepath where the directory is located.
    # currentTime - a time.time() object, used to track how recently something was modified
# @return - None
#
# Usage - Moves recently modified(past 24 hours) files from a src directory to a destination directory.
#
# Notes - This could probably have been merged with the "Choose" function, but due to subtle differences in application,
#   I opted to instead have them as two separate functions. I could probably have included a boolean "move" flag to dictate
#   whether one behavior was intended or the other. However, that did not occur, and probably will never occur.
#============================================================================================================================
def transfer(src, dst, currentTime):
        children = os.listdir(src)
        for child in children:
            if child.endswith(".git"):
                continue
            try:
                test = os.listdir(src + "/" + child)
                transfer(src + "/" + child, dst, currentTime)
            except (NotADirectoryError):
                recently_modified = ((currentTime - os.stat(src + "/" + child).st_mtime) <= 86400)
                if recently_modified:
                    shutil.copy2(src + "/" + child, dst) #move normally, copy for now
                else:
                    pass
            
# main function execution            
def main():
    root = Tk()
    fileGUI = FileTransferGUI(root)
    root.mainloop()

# module handling
if __name__ == "__main__": main()

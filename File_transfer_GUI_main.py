## Python Drill 4
# A file-handling GUI
# By Nick Henegar

#imports
import os
import shutil
import time
from tkinter import *
from tkinter import ttk

#allow user to browse and choose folders to be checked with d.3
#Allow user to choose destination folder
#Allow user to manually activate file-check
#tkinter file dialog

#GUI Class
class FileTransferGUI:
    def __init__(self, master):
        self.currentTime = time.time()
        self.src = ''
        self.dst = ''
    #Styling the master window and the two slave frames
        master.title('File Transfer GUI')
       # master.resizable(True,True)
        master.configure(background = 'light blue')

        self.style = ttk.Style()
        self.style.configure('Header.TLabel', font = ('Arial', 20))

        self.frame_header = ttk.Frame(master)
        self.frame_header.pack()
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
                  text = ("Click on the source and destination buttons below to set directories for file transfer")).grid(row = 1, column = 1)
        #Content
        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()
        # Directory choice buttons
        self.srcButton = ttk.Button(self.frame_content, image = self.src_img, text = 'Source Directory',
                                    compound = LEFT, command = lambda: cdir(self.src))
        self.srcButton.grid(row = 0, column = 0)
        self.dstButton = ttk.Button(self.frame_content, image = self.dst_img, text = 'Destination Directory',
                                    compound = LEFT, command = lambda: cdir(self.dst))
        self.dstButton.grid(row = 0, column = 1)

        self.testButton = self.dstButton = ttk.Button(self.frame_content, text = 'Test',
                                    command = lambda: test(self.src,self.dst))
        self.testButton.grid(row = 2, column = 0, columnspan = 2)
        
        #Create a paned window to handle the file browsers
        self.fileBrowser = ttk.Panedwindow(self.frame_content, orient = HORIZONTAL)
        self.fileBrowser.grid(row = 1, column = 0, columnspan = 2)
        #Source file viewer
        self.frame_source = ttk.Frame(self.fileBrowser, height = 800, width = 600, relief = SUNKEN)
        self.fileBrowser.add(self.frame_source)
        self.src_treeview = ttk.Treeview(self.frame_source)
        self.src_treeview.pack()
        #Destination file viewer
        self.frame_destination = ttk.Frame(self.fileBrowser, height = 800, width = 600, relief = SUNKEN)
        self.fileBrowser.add(self.frame_destination, weight = 2)
        self.dst_treeview = ttk.Treeview(self.frame_destination)
        self.dst_treeview.pack()
        

     #This loop creates labels for the content frame based on whether or not the business is open at the time of program run.   
       # for i in range(0,3):
        #     ttk.Label(self.frame_content, text = (locations[i].name + ":"),  font = ('Helvetica', 14,'bold') ).grid(row = 0,column = i, padx = 20, sticky = 's')
         #    if (locations[i].open):
          #       ttk.Label(self.frame_content, text = "Open", foreground = 'green', font = ('Impact', 20,'bold')).grid(row = 3,column = (i), padx = 20, sticky = 's')
           #  else:
            #     ttk.Label(self.frame_content, text = "Closed", foreground = 'red', font = ('Impact', 20,'bold')).grid(row = 3,column = (i), padx = 20, sticky = 's')
        #ttk.Label(self.frame_content, image = self.portland_img).grid(row = 1, column = 0)
        #ttk.Label(self.frame_content, image = self.london_img).grid(row = 1, column = 1)
        #ttk.Label(self.frame_content, image = self.nyc_img).grid(row = 1, column = 2)
            
#File checking utility:
def traverse(src, dst, currentTime):
    children = os.listdir(src)
    for child in children:
        recently_modified = ((currentTime - os.stat(src + child).st_mtime) <= 86400) 
        if child.endswith(".txt") and recently_modified:
            shutil.move(src + child, dst)
        elif child[-4:] == '.txt'and not recently_modified:
            pass
        else:
            traverse(src + child + "\\", dst, currentTime)
            
# File Dialog functionality
def cdir(directoryName):
    directoryName = filedialog.askdirectory()
    return directoryName

def test(src,dst):
    print(src)
    print(dst)

# main function execution            
def main():
    root = Tk()
    fileGUI = FileTransferGUI(root)
    root.mainloop()
    
    traverse(src, dst, currentTime)
    print("File transfer operation complete.")

# module handling
if __name__ == "__main__": main()

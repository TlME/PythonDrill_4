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
        self.src = StringVar('')
        self.dst = StringVar('')
    #Styling the master window and the two slave frames
        master.title('File Transfer GUI')
       # master.resizable(True,True)
        master.configure(background = 'light blue')

        self.style = ttk.Style()
        self.style.configure('Header.TLabel', font = ('Arial', 20))

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
                  text = ("Click on the source and destination buttons below to set directories for file transfer")).grid(row = 1, column = 1)
        #Content
        self.frame_content = ttk.Frame(master)
        self.frame_content.pack(fill = BOTH, expand = 1) 
        
        #Create a paned window to handle the file browsers
        self.fileBrowser = ttk.Frame(self.frame_content)
        self.fileBrowser.grid(row = 1, column = 0, columnspan = 2, sticky = E + W + N + S)
        #Source file viewer
        self.frame_source = ttk.Frame(self.fileBrowser, relief = SUNKEN)
        self.frame_source.grid(row = 0, column = 0, sticky = E + W + N + S)
        self.src_treeview = ttk.Treeview(self.frame_source)
        self.src_treeview.pack(fill = BOTH, expand = 1)

        #Destination file viewer
        self.frame_destination = ttk.Frame(self.fileBrowser, relief = SUNKEN)
        self.frame_destination.grid(row = 0, column = 1, sticky = E + W + N + S)
        self.dst_treeview = ttk.Treeview(self.frame_destination)
        self.dst_treeview.pack(fill = BOTH, expand = 1)

         # Directory choice buttons
        self.srcButton = ttk.Button(self.frame_content, image = self.src_img, text = 'Source Directory',
                                    compound = LEFT, command = lambda: self.src.set(choose(self.src_treeview, self.file_img, self.folder_img)))
        self.srcButton.grid(row = 0, column = 0)
        self.dstButton = ttk.Button(self.frame_content, image = self.dst_img, text = 'Destination Directory',
                                    compound = LEFT, command = lambda: self.dst.set(choose(self.dst_treeview, self.file_img, self.folder_img)))
        self.dstButton.grid(row = 0, column = 1)
        self.testButton = self.dstButton = ttk.Button(self.frame_content, text = 'Test',
                                    command = lambda: genTrees(self.src_treeview, self.src.get(), '', self.file_img, self.folder_img))
        self.testButton.grid(row = 2, column = 0, columnspan = 2)
        
#source chooser
def choose(src_treeview, file_img, folder_img):
    src = filedialog.askdirectory()
    #File Viewing utility:
    def genTrees(src_treeview, src, parent, file_img, folder_img):
        i = 0
        children = os.listdir(src)
        for child in children:
            if child.endswith(".git"):
                continue
            try:
                test = os.listdir(src + "/" + child)
                src_treeview.insert(parent, 'end', parent + str(i), image = folder_img, text = child)
                genTrees(src_treeview, src + "/" + child,  parent + str(i), file_img, folder_img)
            except (NotADirectoryError):
                src_treeview.insert(parent, 'end', parent + str(i), image = file_img, text = child)
            i += 1
    genTrees(src_treeview, src, '', file_img, folder_img)
    return src

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
            
# main function execution            
def main():
    root = Tk()
    fileGUI = FileTransferGUI(root)
    root.mainloop()

# module handling
if __name__ == "__main__": main()

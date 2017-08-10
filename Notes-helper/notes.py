import os
from Tkinter import *
from ttk import *
import tkFileDialog
import tkMessageBox
note=Tk()
note.title("SSN")
homedir=os.environ['HOME']
homedir+=r"/SSN"
currentdoc=r''

if not os.path.isdir(homedir):
    os.mkdir(homedir,0755)
text=Text(note,state=NORMAL,wrap=WORD)
text.pack()
scroll=Scrollbar(orient=VERTICAL,command=text.yview)
text['yscrollcommand']=scroll.set

def newproject():
    top=note.top=Toplevel(note)
    Label(top,text="Enter project name:").pack()
    note.e=Entry(top)
    note.e.pack(padx=5)
    def create():
        global homedir
        path=homedir
        path+='/'
        path+=str(note.e.get())
        if os.path.isdir(path):
	    tkMessageBox.showinfo("","Project exsists")
        else:
            os.mkdir(path,0755)
        note.top.destroy()
    done=Button(top,text="CREATE",command=create).pack(pady=5)

def newdocument():
    text.delete(1.0,END)
    
def opendocument():
    path=homedir
    filename=tkFileDialog.askopenfilename(parent=note)
    f=open(filename)
    text.delete(1.0,END)
    text.insert(INSERT,f.read())
    f.close()
    global currentdoc
    currentdoc=r''
    currentdoc+=str(filename)
    
def save():
    global currentdoc
    if len(currentdoc)==0:
        saveas()
    else:
        with open(currentdoc,mode="w") as filetosave:
            filetosave.seek(0)
            filetosave.truncate()
            filetosave.write(text.get("1.0","end-1c"))
        
def saveas():
    name=tkFileDialog.asksaveasfile(mode="w",defaultextension=".txt")
    text2save=str(text.get(1.0,END))
    name.write(text2save)
    name.close()
    
menubar=Menu(note)
filemenu=Menu(menubar,tearoff=0)
filemenu.add_command(label="New Project",command=newproject)
filemenu.add_command(label="New Document",command=newdocument)
filemenu.add_command(label="Open Document",command=opendocument)
filemenu.add_command(label="Save",command=save)
filemenu.add_command(label="Save as",command=saveas)
filemenu.add_separator()
filemenu.add_command(label="Exit",command=note.quit)
menubar.add_cascade(label="File",menu=filemenu)
note.config(menu=menubar)
mainloop()

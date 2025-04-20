
import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from tkinter import font as tkfont
from PIL import Image, ImageTk
from tkinter import filedialog
import requests
from io import BytesIO
import csv
import sys
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import messagebox
def Window(): 
    root = tk.Tk()
    return root

def Title(root, title = "New Window"):
    a = root.title(title)
    return a
def Dropdown(parent, textvariable, values):
    dropdown = ttk.Combobox(parent, textvariable=textvariable, values=values)
    return dropdown


def ScrollBar(root, widget, side="right", fill="y"):
    a = widget
    scrollbar = tk.Scrollbar(root, command=a.yview)
    scrollbar.pack(side=side, fill=fill)
    a.config(yscrollcommand=scrollbar.set)



def DragDropArea(parent, text="Drag and Drop here!", width=40, height=10, padx=20, pady=20):
    label = tk.Label(parent, text=text, width=width, height=height, relief="solid")
    label.pack(padx=padx, pady=pady)

    def on_drop(event):
        dropped_file = event.data
        messagebox.showinfo("File Dropped", f"You dropped the file: {dropped_file}")

    label.drop_target_register(DND_FILES)
    label.dnd_bind('<<Drop>>', on_drop)
    
    return label


def Label(parent, textvariabl, text=None, font="Helvetica", size=12, color="black", wraplenght=2, width=50):
    label = ttk.Label(parent, text=text,  font = (font, size), foreground = color, wraplength=wraplenght, textvariable=textvariabl, width=width)
    return label

    

def Place(widget, x, y):
    widget.place(x=x, y=y)

def Font(name = 'arial', size = 20, weight = "bold"):
    font = tkfont.Font(name = name, size = size, weight = weight)
    return font
def StrVar(master, string):
    v = tk.StringVar(master, string)
    return v
def OpenFile(title):
    file_path = filedialog.askopenfilename(title="Select a file")
    return file_path

def SaveFile(title):
    file_save = filedialog.asksaveasfilename(
    title=title,
    defaultextension=".txt",
    filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
)
    return file_save


def ChexBox(parent, text = 'check me', variable=None, command = None):
    checkbutton = ttk.Checkbutton(parent, text=text, variable=variable, command=command)

def CTBox(parent, width = 120, height = 25, corner_radius=10, fg = "red", text = "Custom Button"):
    CTkEntry(master=parent, width=width, height=height, corner_radius=corner_radius, fg = fg, text = text )

def add(widget, padx = 10, pady = 10, side="left", fill = "y", expand=True):
    widget.pack(padx = padx, pady = pady, side=side, fill=fill, expand=expand)

def BGImage(parent, bg_image_path = '', width=400 , height=300):
    # Load and set the background image
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((width, height), Image.ANTIALIAS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    background_label = tk.Label(parent, image=bg_photo)
    background_label.image = bg_photo  # Keep a reference to avoid garbage collection
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

def Button(parent, text="Button", command=None, font="Helvetica", size=12, bg="black", fg="black", width=20, height=20):
    button = tk.Button(parent, text=text, command=command, font=(font, size), bg=bg, fg=fg, width=width, height=height)
    return button

def Entry(parent, width=20, font="Helvetica", size=12, bg="white", fg="black"):
    entry = ttk.Entry(parent, width=width, font=(font, size), background=bg, foreground=fg)
    return entry
def CVSREAD(filename):
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        return reader
    
def CVSWRITE(filename, data):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)
        
def Image(parent, path_or_url, width=None, height=None):
    try:
        # Load image from URL or file
        if path_or_url.startswith('http'):
            response = requests.get(path_or_url)
            img_data = BytesIO(response.content)
        else:
            img_data = path_or_url

        img = Image.open(img_data)

        # Resize if needed
        if width and height:
            img = img.resize((width, height))

        tk_img = ImageTk.PhotoImage(img)

        label = tk.Label(parent, image=tk_img)
        label.image = tk_img  # Keep a reference to prevent garbage collection
        label.pack()        
        return label
    except Exception as e:
        print("Error loading image:", e)
        return None

def GetEntry(entry):
    d = entry.get()
    return d 

def Design(theme):
    style = Style(theme=theme)
    return style

def BulleanVar():
    Variable = tk.BooleanVar()
    return Variable

def Run(window):
    window.mainloop()

def BGImage(parent, bg_image_path = '', width=400 , height=300):
    # Load and set the background image
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((width, height), Image.ANTIALIAS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    background_label = tk.Label(parent, image=bg_photo)
    background_label.image = bg_photo  # Keep a reference to avoid garbage collection
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

def Button(parent, text="Button", command=None, font="Helvetica", size=12, bg="black", fg="black", width=20, height=20, padx = 10, pady = 10):
    button = tk.Button(parent, text=text, command=command, font=(font, size), bg=bg, fg=fg, width=width, height=height)
    return button

def Entry(parent, width=20, font="Helvetica", size=12, bg="white", fg="black", padx = 10, pady = 10):
    entry = ttk.Entry(parent, width=width, font=(font, size), background=bg, foreground=fg)
    return entry
def Close(window):
    window.destroy()
def Exit():
        sys.exit()
def Run(window):
    window.mainloop()
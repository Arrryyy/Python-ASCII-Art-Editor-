"""
Developer's Name: Aryan Jain
Matriculation Number: 22107593

Libraries used:
import tkinter
import threading
from tkinter import *
from PIL import ImageTk, Image
from PIL import ImageDraw
from tkinter import filedialog as fd
from tkinter import ttk
import PIL
import PIL.Image
import numpy as np
from tkinter import messagebox

ASCII Art Editor GUI:
- This program can convert an RGB Image to Grayscale and show it on Canvas
- This Program, then can convert the grayscale image to ASCII Image and show it on Canvas
- This Program also allows user to save the ASCII Image into File. 
- The GUI allows the user to select an image, specify the ASCII Character Image parameters for ASCII conversion, and generate the ASCII art.
- The ASCII art is displayed in the GUI with scroll bars. 
- The generated text can be saved to a .txt file.

Rules:
- All rules from the slide set 00_exercise_performance_general.pdf apply.
- The main file is called ascii_art.py.
- Deadline is 2023-06-05 (Monday), 23.59 o’clock.
- There are 10 points to achieve:
    - 1 point for sticking to the general rules.
    - 2 points for a GUI layout that contains all the required elements and options.
    - 2 points for all options being read correctly from the GUI for the conversion and proper default values.
    - 3 points for a working conversion of an image to ASCII.
    - 2 points for having the conversion done with a thread, which is meaningfully joined to the main thread at some point.

The conversion process:
- The input image is converted to grayscale.
- A set of characters is provided as input.
- These characters are rendered to little images with specified width, height, and font size.
- For each position in the input image, a distance metric (e.g. Euclidean distance) is computed between the original image crop and all the character images.
- The character with the lowest distance is selected for the final ASCII text.

GUI parameters:
- Image path: an entry and a file selection dialogue button to choose the image.
- Character image width, height, and font size: entries with proper labels.
- Grayscale conversion method: a button or label to select the method (e.g. RGB channels).
- Character set: an entry to type in the characters for conversion.

Main GUI elements:
- Generate button: starts the conversion with the selected options.
- Save Text button: opens a file selection dialogue to save the generated text to a .txt file.
- Generated ASCII text: displayed as the main element of the GUI with scroll bars if necessary.

Threads:
- The conversion process is done in a separate thread.
- The thread is joined with the main thread at some point.

Voluntary additions:
- Use a more advanced distance measure for the conversion.

Implementation help:
- Use monospaced fonts for ASCII art conversion.
- Required libraries: tkinter, Pillow, and NumPy.
- Good resources for learning: lecture slides.
- Think about meaningful events to join the conversion thread and avoid creating multiple threads rapidly by pressing the Generate button.

""" 


import tkinter
from tkinter import *
from PIL import ImageTk, Image
from PIL import ImageDraw
from tkinter import filedialog as fd
from tkinter import ttk
import PIL
import PIL.Image
import numpy as np
from tkinter import messagebox

class ASCIIart:
    IsImageGray = False
    ascii = []
    # Select image to print on Canvas
    def select_image(self):
        filetypes= [("Image files", "*.png;*.jpg;*.jpeg;*.gif")] #Opt-on:Image Files Only!
        filename = fd.askopenfilename(title="Select an Image", filetypes=filetypes)
        if filename:
            self.SelectPath.delete(0, END)
            self.SelectPath.insert(0, filename)
            #Display the Selected Image:
            img = Image.open(filename) 
            # self.canvas.delete("all")
            self.photo = ImageTk.PhotoImage(img)
            self.image_label.configure(image=self.photo)
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            self.canvas.pack()

    # Convert the selected image to Grayscale
    def Convert_to_grayscale(self):
        if self.photo:
            if self.is_grayscale:
                # Convert grayscale image to color
                img_rgb = Image.open(self.SelectPath.get())
                self.photo = ImageTk.PhotoImage(img_rgb)
                self.image_label.configure(image=self.photo)
                Grayscale=u"\U00002611"
                self.GenerateGray.configure(text=Grayscale+" |"+" Convert to Gray-Scale")
                self.IsImageGray = False
                self.is_grayscale = False
            else:
                # Convert color image to grayscale
                img_rgb = Image.open(self.SelectPath.get())
                self.img_gray = img_rgb.convert('L')
                self.photo = ImageTk.PhotoImage(self.img_gray)
                self.image_label.configure(image=self.photo)
                colorPalate=u"\U0001F3A8"
                self.GenerateGray.configure(text=colorPalate+" |"+ " Convert to Color")
                self.IsImageGray = True
                self.is_grayscale = True
    def resized_image(self):
        # Open the original image
            img = Image.open(self.SelectPath.get())
            # Resize the original image to match the character image size
            des_width = int(self.Charwidth_entry.get())
            des_height = int(self.Charheight_entry.get())
            img_resized = img.resize((des_width,des_height))
            # img_resized.show()
            # self.photo = ImageTk.PhotoImage(img_resized)
            # self.image_label.configure(image=self.photo)
            # self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            return img_resized

    
    def pixels_to_ascii(self):
        ASCII_CHARS = []
        char_data = self.Character_entry.get()
        for char in char_data:
            ASCII_CHARS.append(char)
        # path = self.SelectPath.get()

        # # resize the image as given by the user
        # img1 = Image.open(path)
        # dw = int(self.Charwidth_entry.get())
        # dh = int(self.Charheight_entry.get())
        # img2=img1.resize(dw,dh)

        img2=self.resized_image()
        # Get Gray Image if it's already converted, or convert it to gray      
        imgGray = img2.convert('L')
        

        # Get width and Height of Original Image
        W,H = imgGray.size[0], imgGray.size[1]

        # Count number of Colomns
        rem = W%int(self.fontsize_entry.get())
        if(rem!=0):
            c = int(W/int(self.fontsize_entry.get()))+1
        else: 
            c= int(W/int(self.fontsize_entry.get()))

        # Width of the tile
        w = W/c

        # Count number of Rows
        rem = H%int(self.fontsize_entry.get())
        if(rem!=0):
            r = int(H/int(self.fontsize_entry.get()))+1
        else: 
            r= int(H/int(self.fontsize_entry.get()))
        
        # Height of the Tile 
        h = H/r
        
        # Define ASCII Image Array in NumPy
        # ascii = []

        # generate list of dimensions
        for j in range(r):
            y1 = int(j*h)
            y2 = int((j+1)*h)
 
            # correct Euclidian Distance
            if j == r-1:
                y2 = H
 
            # append an empty string for this row
            self.ascii.append("")
 
            for i in range(c):
                # crop image to tile
                x1 = int(i*w)
                x2 = int((i+1)*w)
 
                # correct Euclidian Distance:
                if i == c-1:
                    x2 = W

 
                # crop image to extract tile
                img = imgGray.crop((x1, y1, x2, y2))

                # Get Average Luminisence of this tile:
                Limage = np.array(img)
                w1,h1 = Limage.shape

                Al = np.average(Limage.reshape(w1*h1))

                self.ascii[j] += ASCII_CHARS[int((Al*len(ASCII_CHARS))/255)]

        #Create Text Widget
        self.canvas.delete("all")
        h = Scrollbar(self.canvas, orient = 'horizontal')
        h.pack(side = BOTTOM, fill = X)
        v = Scrollbar(self.canvas)
        v.pack(side = RIGHT, fill = Y)
        T = Text(self.canvas, bg="white", fg="black",width=self.Charwidth_entry.get(), height= self.Charheight_entry.get(),xscrollcommand= h.set, yscrollcommand = v.set)
        for row in self.ascii:
            T.insert(END, str(row + '\n'))
        print("hello")
        T.pack()

    
    def save_to_ASCII(self):
        ftypes= [("Text file", ".txt")] #Opt-on:Text Files Only!
        fname = fd.askopenfilename(title="Select a Text File", filetypes=ftypes)
        if not fname:
            fname = "myascii.txt"
        f = open(fname, 'w')
        # write to file
        for row in self.ascii:
            f.write(row + '\n')
        # cleanup
        f.close()
        messagebox.showinfo("ASCII Dump", f"File written into {fname}")

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")
    
    # Inititator-Method
    def __init__(self):
        self.root=Tk()
        self.root.title("ASCII Art Editor")
        self.root.geometry("950x700")
        
        #The Header Frame
        self.header_frame = Frame(self.root, height=80, background="light blue")
        self.header_frame.pack(side="top",fill="x")
        
        #The Footer Frame
        self.footer_frame = Frame(self.root,height=80, background="light blue")
        self.footer_frame.pack(side="bottom",fill="x")

        # Calculate available height for the Text widget
        window_height = int(self.root.winfo_height())
        header_height = int(self.header_frame.winfo_height())
        footer_height = int(self.footer_frame.winfo_height())
        text_widget_height = window_height - header_height - footer_height

        # Create the text widget
        self.text_widget = Text(self.root, font="Arial 12", wrap=WORD)
        self.text_widget.pack(fill=BOTH, expand=True)
        self.text_widget.place(x=0, y=header_height, relwidth=1, relheight=text_widget_height / window_height)

        #The "ASCII Art GUI"label
        self.label = Label(self.root, text="ASCII Art GUI",font="Calibri 25",bg="white")
        self.label.place(x=55, y=25)
        self.label.config(fg="blue")

        #The font-Size Entry
        self.fontsize_entry = Entry(self.footer_frame,width=3,font=('Arial',14),background="light gray")
        self.fontsize_entry.insert(0, "9")
        self.fontsize_entry.place(x=30,y=20)
        self.fontsizelabel = Label(self.footer_frame,text="Font Size",background="white")
        self.fontsizelabel.place(x=25, y=45)

        #The Image Width Entry
        self.Charwidth_entry = Entry(self.footer_frame,width=3,font=('Arial',14) ,background="light gray")
        self.Charwidth_entry.insert(0, "300")
        self.Charwidth_entry.place(x=110,y=20)
        self.Charwidthlabel = Label(self.footer_frame,text="Image Width",background="white")
        self.Charwidthlabel.place(x=95,y=45)

        #The Image Height Entry
        self.Charheight_entry = Entry(self.footer_frame, width=3,font=('Arial',14),background="light gray")
        self.Charheight_entry.insert(0, "200")
        self.Charheight_entry.place(x=190,y=20)
        self.Charheightlabel = Label(self.footer_frame, text="Image Height", background="white")
        self.Charheightlabel.place(x=175,y=45)

        #Take Users Character for grayscale
        self.Character_entry = Entry(self.footer_frame, width=15,font=('Arial',14), background="light gray")
        self.Character_entry.insert(0, "@%#*+=-:.")
        self.Character_entry.place(x=300,y=20)
        self.CharacterLabel = Label(self.footer_frame, text="Characters", background="white")
        self.CharacterLabel.place(x=350,y=45)

        #Render ASCII Image Button
        arrow_symbol = u"\U000021BA" 
        Regeneratebutton = Button(self.footer_frame, text=arrow_symbol+" Generate ASCII", width=15, height=2, font="Arial 12 bold",command=self.pixels_to_ascii)
        Regeneratebutton.place(x=750,y=15)

        #The Select-Path Entry
        self.SelectPath= Entry(self.root,width=30, background="light gray")
        self.SelectPath.place(x=450,y=40, height=25)
        # The image label
        self.canvas = Canvas(self.root, width=950, height=620)
        self.canvas.pack(side="top", pady=10)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.scrollbar_y = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        # self.scrollbar_y.grid(row=0,column=1,sticky=NS)
        self.scrollbar_y.pack(side="right", fill="y")
        self.scrollbar_x = ttk.Scrollbar(self.root, orient="horizontal", command=self.canvas.xview)
        self.scrollbar_x.pack(side="bottom", fill="x")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas_frame = Frame(self.canvas)  # Create a frame to hold the image label
        self.canvas.create_window((0, 0), window=self.canvas_frame, anchor="nw")  # Add frame to the canvas
        self.image_label = Label(self.canvas_frame)  # Use canvas frame as the parent of the image label
        self.image_label.pack()

        #Save-File Button
        floppy_disk = u"\U0001F4BE"
        Savefile = Button(self.root,text=floppy_disk+" |"+" Save ASCII File", command = self.save_to_ASCII)
        Savefile.place(x=800,y=38)

        #Select-Image Button
        Search = u"\U0001F50D"
        Selectfile = Button(self.root,text=Search+" |"+" Select Image",command=self.select_image)
        Selectfile.place(x=680,y=38)

        self.is_grayscale = False  # Initialize is_grayscale attribute

        #The Generate GrayScale-Button
        Grayscale=u"\U00002611"
        self.GenerateGray= Button(self.root, text=Grayscale+" |"+" Convert to Gray-Scale",command=self.Convert_to_grayscale)
        self.GenerateGray.place(x=270,y=38)
        self.root.mainloop()

# Main
a= ASCIIart()
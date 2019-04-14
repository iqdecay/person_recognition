from tkinter import Tk
from PIL import ImageTk, Image
import tkinter as tk
from functools import partial
import os
from tkinter.filedialog import askopenfilename, askdirectory
import cv2

# TODO : Make interface explain that the choice is for the face_database directory location
#  Provide the location of the database of pictures
# directory = askdirectory() + '/'
directory = "/home/lulwat/Documents/IMT/S4/face-database/"

# TODO : Make interface explain that the choice is for the list of directories

# Provide the location of the file containing the preselected folders under CSV form
# preselection_file = askopenfilename()
preselection_file = "/home/lulwat/Documents/IMT/S4/test-set.csv"

# Make a dictionary with all the preselected directories as keys and their content as values
directories = dict()
with open(preselection_file) as fp:
    issues = []
    lines = fp.readlines()
    for line in lines:
        name = line.split(",")[0].strip() + '/'
        try:
            file_list = os.listdir(directory + name)
            print(file_list)
            directories[name] = list()
            for file in file_list:
                directories[name].append(directory + name + file)

        except FileNotFoundError:
            issues.append(name)
#  TODO : fix the encoding issue (optional)
#  TODO : add the possibility to fix the name in the file and the directory (optional)
print("There were issues with theses files :", issues)


class MyApp:
    def validate(self, i):
        print(i)

    def __init__(self, parent):
        self.results = []
        self.parent = parent  # The parent Tk application
        # We give all the rows the same non-zero weight so that they scale with the window
        self.parent.rowconfigure(0, weight=1)
        self.parent.rowconfigure(1, weight=1)  # We add an empty row for design purposes
        self.parent.rowconfigure(2, weight=1)

        filename = "/home/lulwat/Documents/IMT/S4/face-database/a.j. hinch/newsml.afp.com.20180221.PH.GTY.922314274.png"
        image = Image.open(filename)
        image = image.resize((800,800))
        photo = ImageTk.PhotoImage(image)

        self.label = tk.Label(image=photo)
        self.label.image = photo
        self.label.grid(row=0, column=0, columnspan=2)
        # self.display = tk.Canvas(self.parent, width=w, height=h)
        # self.display.pack()
        # self.display.create_image(0, 0, image=photo)

        # self.display.grid(row=0, column=0)
        true = tk.Button(self.parent, text="True", command=partial(self.validate, True))
        false = tk.Button(self.parent, text="False", command=partial(self.validate, False))
        self.parent.columnconfigure(0, weight=1)
        self.parent.columnconfigure(1, weight=1)
        true.grid(row=2, column=0, columnspan=1, sticky="nswe")
        false.grid(row=2, column=1, columnspan=1, sticky="nswe")


root = Tk()
root.title('Test UI')
myapp = MyApp(root)
root.mainloop()

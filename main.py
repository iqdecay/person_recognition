from tkinter import Tk, Image
import tkinter as tk
from functools import partial
import os
from tkinter.filedialog import askopenfilename, askdirectory

Tk().withdraw()
# TODO : Make interface explain that the choice is for the face_database directory location
# Provide the location of the database of pictures
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
        name = line.split(",")[0].strip()
        try:
            directories[name] = os.listdir(directory + name)
        except FileNotFoundError:
            issues.append(name)
#  TODO : fix the encoding issue (optional)
#  TODO : add the possibility to fix the name in the file and the directory (optional)
print("There were issues with theses files :", issues)



class MyApp :
    def validate(self, i):
        print(i)
    def __init__(self, parent):
        self.results = []
        self.parent = parent  # The parent Tk application
        # self.experiences = experiences  # The experience set
        # self.tickets = tickets  # The ticket dictionary
        # self.number_of_tickets = number_of_tickets
        # self.current_ticket_couple = -1
        # self.ticket_a = None  # Contains ticket id
        # self.ticket_b = None  # Contains ticket id
        # self.similarity = None
        # self.text_a = None
        # self.text_b = None
        # We give all the rows the same non-zero weight so that they scale with the window
        self.parent.rowconfigure(0, weight=1)
        self.parent.rowconfigure(1, weight=1)  # We add an empty row for design purposes
        self.parent.rowconfigure(2, weight=1)
        self.text_top = tk.Text(self.parent, wrap=tk.WORD)  # The wrap=WORD option avoids newline in the middle of words
        self.text_top.grid(row=0, column=0, columnspan=11, sticky="nswe")
        button_values = [(str(i), i) for i in range(11)]
        for text, integer in button_values:
            b = tk.Button(self.parent, text=text, command=partial(self.validate, integer))
            self.parent.columnconfigure(integer, weight=1)
            b.grid(row=2, column=integer, columnspan=1, sticky="nswe")


root = Tk()
root.title('Test UI')
# root.state('zoomed')
myapp = MyApp(root)
root.mainloop()


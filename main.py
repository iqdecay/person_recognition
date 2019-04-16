from tkinter import Tk
from PIL import ImageTk, Image
import tkinter as tk
from functools import partial
import os
import pickle
from tkinter.filedialog import askopenfilename, askdirectory, asksaveasfile
import cv2

# TODO : Make interface explain that the choice is for the face_database directory location
# TODO : take back the location of the face_database is already defined and ask for confirmation
#  Provide the location of the database of pictures
# directory = askdirectory() + '/'
directory = "/home/lulwat/Documents/IMT/S4/face-database/"

# TODO : Make interface explain that the choice is for the list of directories

# Provide the location of the file containing the preselected folders under CSV form
# preselection_file = askopenfilename()
preselection_file = "/home/lulwat/Documents/IMT/S4/test-set.csv"

# Make a dictionary with all the preselected directories as keys and their content as values
list_of_pictures = list()
with open(preselection_file) as fp:
    issues = []
    lines = fp.readlines()
    for line in lines:
        name = line.split(",")[0].strip()
        try:
            file_list = os.listdir(directory + name)
            for file in file_list:
                list_of_pictures.append((name, directory + name + '/' + file))

        except FileNotFoundError:
            issues.append(name)


#  TODO : fix the encoding issue (optional)
#  TODO : add the possibility to fix the name in the file and the directory (optional)
#  TODO : log the issues in a text file instead


class MyApp:
    def validate(self, button_value):
        self.update_photo()
        self.results[self.current_filepath] = button_value

    def update_photo(self, quit_and_save=False):
        """
        Update the picture displayed
        :quit : boolean, True if the quit button was pressed
        :return: None
        """
        if self.current_picture_number < self.max_picture_number and not quit_and_save:
            self.current_picture_number += 1
            self.current_name, self.current_filepath = list_of_pictures[self.current_picture_number]
            image = Image.open(self.current_filepath)
            h, w = image.height, image.width
            ratio = w / h
            image = image.resize((int(round(800 * ratio)), 800))
            photo = ImageTk.PhotoImage(image)
            self.image.configure(image=photo)
            self.image.image = photo
            self.update_text()

        elif quit_and_save:
            # TODO : make the GUI announce quitting and saving
            self.results["last_picture_treated"] = self.current_picture_number
            file_save(self.results)
            print("Results saved")
            self.parent.quit()

        else:
            #  TODO : make the GUI announce the completion
            print("All files were explored")

    def update_text(self):
        """
        Update the text displayed, to show the next ticket pair
        :return: None
        """
        self.text.config(text="Est-ce que cette photo représente bien {}".format(self.current_name))

    def __init__(self, parent):
        # Initialize the variables about the image displayed
        self.parent = parent  # The parent Tk application
        self.current_name = ""
        self.current_filepath = ""
        self.max_picture_number = len(list_of_pictures) - 1
        self.current_picture_number = -1

        # Initialize login
        self.results = dict()

        # Give all the rows the same non-zero weight so that they scale with the window
        self.parent.rowconfigure(0, weight=1)
        self.parent.rowconfigure(1, weight=1)  # We add an empty row for design purposes
        self.parent.rowconfigure(2, weight=1)

        # Add a quit and save button
        quit_and_save = tk.Button(self.parent, text="Quit and save", command=partial(self.update_photo, True))
        quit_and_save.grid(row=2, column=1)

        #  Configure image and buttons widgets
        self.image = tk.Label()
        self.image.grid(row=0, column=0, columnspan=3)
        true = tk.Button(self.parent, text="Oui", command=partial(self.validate, True))
        false = tk.Button(self.parent, text="Non", command=partial(self.validate, False))
        true.grid(row=2, column=0, columnspan=1, sticky="nswe")
        false.grid(row=2, column=2, columnspan=1, sticky="nswe")
        self.parent.columnconfigure(0, weight=1)
        self.parent.columnconfigure(1, weight=1)
        self.parent.columnconfigure(2, weight=1)

        # Configure text widget
        self.text = tk.Label(parent, text="Est-ce que cette photo représente bien {}".format(self.current_name))
        self.text.grid(row=1, column=0, columnspan=2)

        # Load previous results to resume where we stopped
        try:
            print("Loading previous results")
            with open("results.pkl", "rb") as f:
                self.results = pickle.load(f)
                self.current_picture_number = self.results["last_picture_treated"]
        except FileNotFoundError:
            print("No previous results found, starting from 0")


def file_save(content):
    new_file = asksaveasfile(mode='wb', defaultextension=".pkl")
    if file is None:
        return
    pickle.dump(content, new_file, -1)
    new_file.close()


root = Tk()
root.title('Test UI')
root.attributes("-zoomed", True)

myapp = MyApp(root)

root.mainloop()

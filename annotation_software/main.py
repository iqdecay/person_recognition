from tkinter import Tk
from PIL import ImageTk, Image
import tkinter as tk
from functools import partial
import os
import pickle
from tkinter.filedialog import askopenfilename, askdirectory, asksaveasfile
from tkinter.messagebox import showinfo, showerror
import cv2

root = Tk()
root.title("Application d'annotation")
root.attributes("-zoomed", True)
# TODO : take back the location of the face_database if already defined and ask for confirmation
#  Provide the location of the database of pictures
directory = askdirectory(title="Locate the folder containing 'face-database'")
while "face-database" not in os.listdir(directory):
    showerror("Wrong location", "Make sure the selected folder contains 'face-database'")
    directory = askdirectory(title="Locate the folder containing 'face-database'")
directory = os.path.join(directory, "face-database")
print("face-database folder found in {}".format(directory))

preselection_file = "test-set.csv"

# Make a dictionary with all the preselected directories as keys and their content as values
list_of_pictures = list()
try:
    with open(preselection_file) as fp:
        issues = []
        lines = fp.readlines()
        number_of_pictures = 0
        for line in lines:
            # The line is under in the format "name, n" where n is the number of picture in the corresponding folder
            name = line.split(",")[0].strip()
            try:
                person_directory = os.path.join(directory, name)
                file_list = os.listdir(person_directory)
                for file in file_list:
                    number_of_pictures += 1
                    file_path = os.path.join(person_directory, file)
                    list_of_pictures.append((name, file_path))

            except FileNotFoundError:
                issues.append(name)
    print("{} preselected picture were found, and there was {} issues".format(number_of_pictures, len(issues)))
except FileNotFoundError:
    print("The preselection file was not found !")


#  TODO : fix the encoding issue (optional)
#  TODO : add the possibility to fix the name in the file and the directory (optional)
#  TODO : log the issues in a text file instead


class MyApp:
    def validate(self, button_value):
        self.update_photo()
        # Remove absolute path
        current_picture = os.path.normpath(self.current_filepath.replace(directory, ""))
        print(button_value)
        self.results[current_picture] = button_value

    # Alias of the above function to ignore the event argument
    def validate_keyboard(self, button_value, event):
        self.validate(button_value)

    def go_back(self):
        self.current_picture_number -= 1
        self.current_name, self.current_filepath = list_of_pictures[self.current_picture_number]
        image = Image.open(self.current_filepath)
        h, w = image.height, image.width
        ratio = w / h
        image = image.resize((int(round(800 * ratio)), 800))
        photo = ImageTk.PhotoImage(image)
        self.image.configure(image=photo)
        self.image.image = photo
        self.update_text()

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
            showinfo("Save and quit", "Saving the results under results.pkl and quitting")
            self.results["last_picture_treated"] = self.current_picture_number
            file_save(self.results)
            for k,v in self.results.items() :
                print(k, v)
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

        # Add "return" button
        go_back = tk.Button(self.parent, text="Retour à la photo précédente", command=self.go_back)
        go_back.grid(row=2, column=2)

        #  Configure image and buttons widgets
        self.image = tk.Label()
        self.image.grid(row=0, column=0, columnspan=4)
        true = tk.Button(self.parent, text="Oui \n (Flèche gauche)", command=partial(self.validate, True))
        false = tk.Button(self.parent, text="Non \n (Flèche droite)", command=partial(self.validate, False))
        true.grid(row=2, column=0, columnspan=1, sticky="nswe")
        false.grid(row=2, column=3, columnspan=1, sticky="nswe")
        self.parent.columnconfigure(0, weight=1)
        self.parent.columnconfigure(1, weight=1)
        self.parent.columnconfigure(2, weight=1)
        self.parent.columnconfigure(3, weight=1)

        # Add arrow keys binding
        self.parent.bind("<Left>", partial(self.validate_keyboard, True))
        self.parent.bind("<Right>", partial(self.validate_keyboard, False))

        # Configure text widget
        self.text = tk.Label(parent, text="Merci de cliquer sur un des deux boutons pour commencer")
        self.text.configure(anchor="center")
        self.text.grid(row=1, column=1, columnspan=2)

        # Load previous results to resume where we stopped
        try:
            print("Loading previous results")
            with open("results.pkl", "rb") as f:
                self.results = pickle.load(f)
                self.current_picture_number = self.results["last_picture_treated"]
        except FileNotFoundError:
            print("No previous results found, starting from 0")


def file_save(content):
    filename = "results.pkl"
    with open(filename, "wb") as file:
        pickle.dump(content, file, -1)


myapp = MyApp(root)

root.mainloop()

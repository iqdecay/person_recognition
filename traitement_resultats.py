import pickle
from tkinter import Tk
import os.path
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror, showinfo

with open("results.pkl", "rb") as file:
    results = pickle.load(file)

root = Tk()
root.title("Provide location of face_database directory")
showinfo("Information", "This program will help you use the annotations results, whatever your operating system")
#  Provide the location of the database of pictures
directory = askdirectory(title="Locate the folder containing 'face-database'")
while "face-database" not in os.listdir(directory):
    showerror("Wrong location", "Make sure the location is correct and the name is 'face-database'")
    directory = askdirectory(parent=root, title="Select location of the face_database directory")
directory = os.path.abspath(directory)

local_results = dict()
for key in results.keys():
    local_path = os.path.normpath(directory + key)
    local_results[local_path] = results[key]
with open("local_results.pkl", "wb") as file:
    pickle.dump(local_results, file, -1)

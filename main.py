from tkinter import Tk
import os
from tkinter.filedialog import askopenfilename, askdirectory

Tk().withdraw()
# TODO : Make interface explain that the choice is for the face_database directory location
# directory = askdirectory() + '/'
directory = "/home/lulwat/Documents/IMT/S4/face-database/"
print(directory)
dirList = os.listdir(directory)
sort = sorted(dirList)

# TODO : Make interface explain that the choice is for the list of directories

# preselection_file = askopenfilename()
preselection_file = "/home/lulwat/Documents/IMT/S4/test-set.csv"
directory_list = []
with open(preselection_file) as fp:
    issues = []
    lines = fp.readlines()
    for line in lines:
        name = line.split(",")[0].strip()
        try:
            listDir = os.listdir(directory + name)
            print(listDir)
        except FileNotFoundError:
            issues.append(name)
#  TODO : fix the encoding issue (optional)
print("There were issues with theses files :", issues)

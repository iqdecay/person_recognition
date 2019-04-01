# This app is used to select tickets that would be suitable to be sent to client relations employees (thanks to the
# final_app.
import tkinter as tk
from tkinter.constants import *
from functools import partial  # Used instead of lambda functions in the buttons

import document_io

tickets_dict = document_io.load("csv_file_as_pickle",
                                "")  # Loading the set of tickets so that we can choose some
ticket_index_list = list(tickets_dict.keys())

previous_name = 'tickets_selected_03'
save_name = 'tickets_selected_04'
begin_index, _ = document_io.load(previous_name, "results")


class MyApp:

    def validate(self, i, quitting=False, saving=False):
        if i:
            self.correct_tickets += 1
            self.results.append(self.current_ticket_id)
        self.current_index += 1
        if self.current_index == self.number_of_tickets or self.correct_tickets == self.goal or quitting:
            results_tuple = (self.current_index, self.results)
            if saving:
                document_io.save(save_name, results_tuple, "results", overwrite=True)
            else:
                print("Quitting without saving !")
            self.parent.destroy()
            return None
        index = self.current_index
        self.current_ticket_id = self.key_list[index]
        self.current_text = self.tickets[self.current_ticket_id]["text"]
        self.update_text()

    def update_text(self):
        self.text_top.configure(state='normal')
        self.text_top.delete(1.0, END)
        self.text_top.insert(INSERT, self.current_text)
        self.text_top.configure(state='disabled')  # Prevent user input in the text zone
        self.text_middle.configure(state='normal')
        self.text_middle.delete(1.0, END)
        self.text_middle.insert(INSERT, "{} right tickets were selected so far".format(self.correct_tickets))
        self.text_middle.configure(state='disabled')

    def __init__(self, parent, tickets, key_list, goal, begin):
        self.results = []
        self.goal = goal
        self.parent = parent
        self.tickets = tickets
        self.key_list = key_list
        self.number_of_tickets = 1000
        self.current_index = begin
        self.current_ticket_id = None
        self.current_text = None
        self.correct_tickets = 0
        # We give all the rows the same non-zero weight so that they scale with the window
        self.parent.rowconfigure(0, weight=1)
        self.parent.rowconfigure(1, weight=1)  # We add an empty row for design purposes
        self.parent.rowconfigure(2, weight=1)
        self.text_middle = tk.Text(self.parent, wrap=WORD)
        self.text_top = tk.Text(self.parent, wrap=WORD)  # The wrap=WORD option avoids newline in the middle of words
        self.text_top.grid(row=0, column=0, columnspan=16, sticky=N + S + E + W)
        self.text_middle.grid(row=1, column=0, columnspan=16, sticky=N + S + E + W)
        self.button_false = tk.Button(self.parent, text="Ce ticket est inutile", command=partial(self.validate, False))
        self.button_true = tk.Button(self.parent, text="Ce ticket est utile", command=partial(self.validate, True))
        self.button_quit = tk.Button(self.parent, text="Quitter sans sauvegarder",
                                     command=partial(self.validate, True, quitting=True, saving=False))
        self.button_save = tk.Button(self.parent, text="Quitter et sauvegarder",
                                     command=partial(self.validate, True, quitting=True, saving=True))
        for i in range(16):
            self.parent.columnconfigure(i, weight=1)
        self.button_false.grid(row=2, column=0, columnspan=4, sticky=N + S + W + E)
        self.button_true.grid(row=2, column=4, columnspan=4, sticky=N + S + W + E)
        self.button_quit.grid(row=2, column=8, columnspan=4, sticky=N + S + W + E)
        self.button_save.grid(row=2, column=12, columnspan=4, sticky=N + S + W + E)
        self.validate(False)


root = tk.Tk()
root.title('Test UI')
root.state('zoomed')
myapp = MyApp(root, tickets_dict, ticket_index_list, 300, begin_index)
root.mainloop()
# aggregate = document_io.load("aggregate", "others")
# _, last_ticket_list = document_io.load(save_name, "others")
# aggregate = aggregate + last_ticket_list
# document_io.save("aggregate", aggregate, "others", overwrite=True)

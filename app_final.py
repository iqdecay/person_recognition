# This app's purpose is to gather notation from relation client employees. Using this app, we ask them to
# assess, on a scale from 0 to 10, how similar are the two tickets we present them with.
# The tickets presented are supposed to already have been processed using the text comparison algorithms, and the
# objective is to evaluate the difference between user opinion and machine decision. If applied at a large enough
# scale, can be a first step towards supervised learning approaches

import tkinter as tk
from tkinter.constants import *
from functools import partial  # Used instead of lambda functions in the buttons

import document_io

# We prepare the experiment
# The experience set is a list of dictionary. Each dictionary is under the form
#  { 'ticket_a': ticket_id,
#    'ticket_b': ticket_id,
#    'similarity': similarity }

experience_list = document_io.load("handpicked", "others")  # Loading the prepared experience set
number_tickets = len(experience_list)
tickets_dict = document_io.load("csv_file_as_pickle", "")


class MyApp:

    def validate(self, i):
        """
        Logs the rating given by the user to the pair of tickets, and then proceed to the next ticket pair
        :param i: the button that initiated the call, hence the user's rating
        :return: None
        """
        result = {
            "ticket_a": self.ticket_a,
            "ticket_b": self.ticket_b,
            "similarity": self.similarity,
            "user_rating": i,
        }
        if i is not None:
            self.results.append(result)
        self.current_ticket_couple += 1
        if self.current_ticket_couple == self.number_of_tickets:
            for result in self.results:
                print(result)
            document_io.save("user_results", self.results, "results", overwrite=True)
            self.parent.destroy()
            return None
        current = self.current_ticket_couple
        current_experience = self.experiences[current]
        self.ticket_a = current_experience['ticket_a']
        self.ticket_b = current_experience['ticket_b']
        self.similarity = current_experience['similarity']
        self.text_a = self.tickets[self.ticket_a]["text"]
        self.text_b = self.tickets[self.ticket_b]["text"]
        self.update_text()
        return None

    def update_text(self):
        """
        Update the text displayed, to show the next ticket pair
        :return: None
        """
        self.text_top.configure(state='normal')
        self.text_top.delete(1.0, END)
        self.text_top.insert(INSERT, self.text_a)
        self.text_top.insert(INSERT, "\n==========================================================================")
        self.text_top.insert(INSERT, '\n' + self.text_b)
        self.text_top.configure(state='disabled')  # Prevent user input in the text zone
        return None

    def __init__(self, parent, number_of_tickets, experiences, tickets):
        self.results = []
        self.parent = parent  # The parent Tk application
        self.experiences = experiences  # The experience set
        self.tickets = tickets  # The ticket dictionary
        self.number_of_tickets = number_of_tickets
        self.current_ticket_couple = -1
        self.ticket_a = None  # Contains ticket id
        self.ticket_b = None  # Contains ticket id
        self.similarity = None
        self.text_a = None
        self.text_b = None
        # We give all the rows the same non-zero weight so that they scale with the window
        self.parent.rowconfigure(0, weight=1)
        self.parent.rowconfigure(1, weight=1)  # We add an empty row for design purposes
        self.parent.rowconfigure(2, weight=1)
        self.text_top = tk.Text(self.parent, wrap=WORD)  # The wrap=WORD option avoids newline in the middle of words
        self.text_top.grid(row=0, column=0, columnspan=11, sticky=N + S + E + W)
        button_values = [(str(i), i) for i in range(11)]
        for text, integer in button_values:
            b = tk.Button(self.parent, text=text, command=partial(self.validate, integer))
            self.parent.columnconfigure(integer, weight=1)
            b.grid(row=2, column=integer, columnspan=1, sticky=N + S + W + E)
        self.validate(None)


root = tk.Tk()
root.title('Test UI')
root.state('zoomed')
myapp = MyApp(root, number_tickets, experience_list, tickets_dict)
root.mainloop()

import tkinter as tk
from tkinter import ttk

class FlightSearchGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Cheapest Flights Finder")

        # Departure label and entry
        self.departure_label = tk.Label(self.window, text="Departure:")
        self.departure_label.grid(column=0, row=0, padx=10, pady=10, sticky=tk.W)
        self.departure_var = tk.StringVar()
        self.departure_entry = ttk.Entry(self.window, textvariable=self.departure_var, width=40)
        self.departure_entry.grid(column=1, row=0, padx=10, pady=10)

        # Destination label and entry
        self.destination_label = tk.Label(self.window, text="Destination:")
        self.destination_label.grid(column=0, row=1, padx=10, pady=10, sticky=tk.W)
        self.destination_var = tk.StringVar()
        self.destination_entry = ttk.Entry(self.window, textvariable=self.destination_var, width=40)
        self.destination_entry.grid(column=1, row=1, padx=10, pady=10)

        # Number of nights label and spinbox
        self.nights_label = tk.Label(self.window, text="Nights:")
        self.nights_label.grid(column=0, row=2, padx=10, pady=10, sticky=tk.W)
        self.nights_var = tk.IntVar(value=1)
        self.nights_spinbox = ttk.Spinbox(self.window, from_=1, to=30, textvariable=self.nights_var, width=5)
        self.nights_spinbox.grid(column=1, row=2, padx=10, pady=10, sticky=tk.W)

        # Number of adults label and spinbox
        self.adults_label = tk.Label(self.window, text="Adults:")
        self.adults_label.grid(column=0, row=3, padx=10, pady=10, sticky=tk.W)
        self.adults_var = tk.IntVar(value=1)
        self.adults_spinbox = ttk.Spinbox(self.window, from_=1, to=10, textvariable=self.adults_var, width=5)
        self.adults_spinbox.grid(column=1, row=3, padx=10, pady=10, sticky=tk.W)

        # Search button
        self.search_button = ttk.Button(self.window, text="Search Flights", command=self.search_flights)
        self.search_button.grid(column=1, row=4, padx=10, pady=10)

    def run(self):
        self.window.mainloop()

    def search_flights(self):
        # Call FlightSearch.search() and display results
        pass

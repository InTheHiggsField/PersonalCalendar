import datetime
import json
import tkinter as tk
from tkcalendar import Calendar, DateEntry
from tkinter import ttk, Event


def add_event():
    top = tk.Toplevel(root)
    field_names = ["Insert Date in MM/DD/YYYY format", "Event Name", "Event Details"]
    entries = {}
    for i, name in enumerate(field_names):
        tk.Label(top, text=f"{name}:").pack(padx=10, pady=10)

        entry = tk.Entry(top)
        entry.pack(padx=5, pady=5)
        entries[name] = entry
        if i == len(field_names) - 1:
            tk.Button(top, text="Submit", command=lambda: store_event_data(entries)).pack(padx=10, pady=10)
def store_event_data(entries):
    entries = {key: entry.get() for key, entry in entries.items()}
    print(entries)
    try:
        with open('event_data.json', 'r') as file:
            event_data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        event_data = {}
    if len(event_data) == 0:
        event_data = {"Event #1" : entries}
    if len(event_data) != 0:
        length = len(event_data) + 1 #This will present issues if I ever want to add a delete option
        #Currently this only tracks the number of events by the length of the dictionary
        #This will cause issues of overwriting events once I start deleting data.
        event_data[f"Event #{length}"] = entries
    with open('event_data.json', 'w') as file:
        json.dump(event_data, file, indent=4, sort_keys=True)

def detailed_calendar():

    top = tk.Toplevel(root)
    top.focus_force()
    cal = Calendar(top, tooltipbackground = 'black', tooltipforeground = 'white', tooltipalpha = 0.9, tooltipdelay = 200)
    try:
        with open('event_data.json', 'r') as file:
            event_data = json.load(file)

    except (FileNotFoundError, json.decoder.JSONDecodeError):
        event_data = {}
    if len(event_data) != 0:
        for events, details in event_data.items():
            date = details["Insert Date in MM/DD/YYYY format"]
            split_date = date.split('/')
            month = int(split_date[0])
            day = int(split_date[1])
            year = int(split_date[2])
            pass_date = datetime.date(year=year, month=month, day=day)
            cal.calevent_create(pass_date, text =f"Name: {details['Event Name']}, Details: {details['Event Details']} ", tags = 'reminder')
            tk.Label(top, text=f"Date: {details["Insert Date in MM/DD/YYYY format"]} {details['Event Details']}").pack(padx=10, pady=10)
            top.update_idletasks()
    cal.tag_config('reminder', background='red', foreground='yellow')
    cal.pack(padx=10, pady=10)
    ttk.Label(top, text=f"You have {len(event_data)} events soon").pack(padx=10, pady=10)

root = tk.Tk()
ttk.Button(root, text="Add Event", command=add_event).pack(padx = 10, pady = 10)
ttk.Button(root, text="Event Calendar", command=detailed_calendar).pack(padx = 10, pady = 10)
root.mainloop()
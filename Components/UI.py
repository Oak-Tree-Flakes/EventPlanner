from tkinter import *
from tkinter import filedialog, messagebox
from Components.Calendar import CalendarCore
from tkcalendar import DateEntry


class Interface:

    def __init__(self):
        self.location = ""
        self.bg_color = "#10ac84"
        self.root = Tk()
        self.root.title("Event Planner")
        self.core = None
        self.details = None
        self.new = True
        self.root.minsize(width=800, height=600)
        self.background = Frame(self.root, bg=self.bg_color)
        self.background.place(relwidth=1, relheight=1)

        self.openFile = Button(self.background, padx=6, pady=2, command=self.get_file, text="Load File")
        self.newEvent = Button(self.background, padx=2, pady=2, command=self.add_window, text="New Event")
        self.openFile.grid(row=0, column=0)
        self.newEvent.grid(row=1, column=0)

        self.root.mainloop()

    def get_file(self):
        self.location = filedialog.askopenfilename(initialdir="./", title="Select Calendar File",
                                                   filetypes=(("Calendar File", "*.ics"), ("All Files", "*.*")))
        if self.location == "":
            return
        try:
            self.core = CalendarCore(self.location)
        except TypeError:
            return messagebox.showerror("Unknown File Type", "Only .ics files are supported")
        self.root.title(f"Event Planner - {self.location}")
        self.new = False

        self.reload_display()

    def reload_display(self):
        temp = str(self.core)
        if self.details:
            self.details.destroy()

        self.details = Label(self.background, text=temp, fg="white", bg=self.bg_color)
        self.details.grid(row=2, column=1)

    def add_window(self):
        # Build looks
        top = Toplevel(self.root)
        top.title("Add New Event")
        top.grab_set()
        top.minsize(width=800, height=600)

        bg2 = Frame(top, bg="#2bcbba")
        bg2.place(relwidth=1, relheight=1)

        Label(bg2, text='Choose date', background="#00b894").grid(row=0, column=0)
        cal1 = DateEntry(bg2, width=12, borderwidth=2)
        cal1.grid(row=0, column=1)

import pytz
import datetime
from tkinter import *
from tkcalendar import DateEntry
from Components.Calendar import CalendarCore, VEvent
from tkinter import filedialog, messagebox, font


core = None


def to_datetime(arr: iter):
    """
    Function to generate a UTC datetime from list of user input options

    Parameters
    ----------
    arr: iter
        list of inputs from user (tk)

    Returns
    -------
    datetime
        UTC datetime from the user
    """
    ret = datetime.datetime.combine(arr[0].get_date(),
                                    datetime.time(int(arr[1].get()), int(arr[2].get()), int(arr[3].get())))
    # https://stackoverflow.com/questions/2720319/python-figure-out-local-timezone
    local_zone = datetime.datetime.now().astimezone().tzinfo
    ret = ret.replace(tzinfo=local_zone)
    return ret.astimezone(pytz.utc)


class Interface:
    """
    Interface class responsible for interactive GUI
    """

    def __init__(self):
        """
        Constructor for the Interface class
        """
        self.location = ""
        self.bg_color = "#10ac84"
        self.root = Tk()
        self.root.title("Event Planner")
        self.details = None
        self.new = True
        self.root.minsize(width=800, height=600)
        self.background = Frame(self.root, bg=self.bg_color)
        self.background.place(relwidth=1, relheight=1)

        # build main window looks
        menu_bar = Menu(self.root, tearoff=0)

        def save_as():
            return self.save_file(True)

        def new_data():
            global core
            core = None
            self.location = ""
            self.reload_display()

        file_sub_menu = Menu(menu_bar, tearoff=0)
        file_sub_menu.add_command(label="New", command=new_data)
        file_sub_menu.add_command(label="Open", command=self.get_file)
        file_sub_menu.add_command(label="Save", command=self.save_file)
        file_sub_menu.add_command(label="Save As...", command=save_as)
        file_sub_menu.add_separator()
        file_sub_menu.add_command(label="Exit", command=self.root.quit)

        menu_bar.add_cascade(label="File", menu=file_sub_menu)

        edit_sub_menu = Menu(menu_bar, tearoff=0)
        edit_sub_menu.add_command(label="New Event", command=EventUI(self.root, self.reload_display).generate)

        menu_bar.add_cascade(label="Edit", menu=edit_sub_menu)

        self.root.config(menu=menu_bar)
        self.root.mainloop()

    def save_file(self, force: bool = False):
        """
        Method for saving the ICS file

        Parameters
        ----------
        force: bool
            whether or not to force ask for save location

        Returns
        -------
        messagebox
            if there is any error
        """
        global core
        if not isinstance(core, CalendarCore):
            return messagebox.showerror("No Data Error", "There is no event in the system to save")

        if self.location == "" or force:
            temp = filedialog.asksaveasfilename(initialdir="./", title="Select Save Location",
                                                filetypes=(("Calendar File", "*.ics"), ("All Files", "*.*")))
            if temp == "":
                return
            else:
                self.location = temp

            if not self.location.endswith(".ics"):
                self.location += ".ics"
        if self.location != "":
            core.write_file(self.location)

        messagebox.showinfo("Success!", f"Calendar data has been saved to:\n{self.location}")
        self.reload_display()

    def get_file(self):
        """
        Method to fetch the location of an existing ICS file

        Returns
        -------
        messagebox
            if there is any error
        """
        self.location = filedialog.askopenfilename(initialdir="./", title="Select Calendar File",
                                                   filetypes=(("Calendar File", "*.ics"), ("All Files", "*.*")))
        if self.location == "":
            return
        try:
            global core
            core = CalendarCore(self.location)
        except TypeError:
            return messagebox.showerror("Unknown File Type", "Only .ics files are supported")
        self.new = False

        self.reload_display()

    def reload_display(self):
        # reloading temporary data view of the CalendarCore, may be removed in the future
        global core
        temp = str(core)
        if self.details:
            self.details.destroy()

        self.details = Label(self.background, text=temp, fg="white", bg="black", justify=LEFT)
        self.details.grid(row=0, column=0) if core else self.details.destroy()
        self.root.title(f"Event Planner - {self.location}") if self.location != "" else self.root.title("Event Planner")


class EventUI:
    def __init__(self, previous: Tk, reload: classmethod, exist_data: VEvent = None, key: int = None):
        self.key = key
        self.font_family = "Open Sans"
        self.data = {} if not exist_data else exist_data
        self.root = None
        self.previous = previous
        self.reload = reload
        self.bg = "#2bcbba"

    def build_datetime_selector(self, root, row: int, title: str, start: int = 6):
        """
        Generate label containing datetime input detectors base on passed information from the parameter

        Parameters
        ----------
        root
            previous "node" for the system to append itself to
        row: int
            row number for the grid position of the root
        title: str
            text for the label
        start: int
            start value for the "hour" part of the input, default 6

        Returns
        -------
        list
            returns list of TK input in the format of [DateEntry, Spinbox...]
        """
        # responsible for creating time selector sections
        hold = LabelFrame(root, text=title, background=self.bg,
                          font=font.Font(family=self.font_family, size=12, weight=font.BOLD))
        hold.grid(row=row, column=0, padx=10, pady=5)
        Label(hold, text='Date', background="#f1c40f").grid(row=0, column=0)
        ret = [DateEntry(hold, width=8, borderwidth=2, background="#f1c40f")]
        ret[0].grid(row=0, column=1, pady=6)

        Label(hold, text='Hour', background="#00cec9").grid(row=0, column=2)
        default = IntVar(hold)
        default.set(start)
        temp = Spinbox(hold, from_=0, to=23, width=6, textvariable=default)
        ret.append(temp)
        ret[1].grid(row=0, column=3)

        Label(hold, text='Minutes', background="#00cec9").grid(row=0, column=4)
        temp = Spinbox(hold, from_=0, to=59, width=6)
        ret.append(temp)
        ret[2].grid(row=0, column=5)

        Label(hold, text='Seconds', background="#00cec9").grid(row=0, column=6)
        temp = Spinbox(hold, from_=0, to=59, width=6)
        ret.append(temp)
        ret[3].grid(row=0, column=7)

        return ret

    def try_create(self):
        """
        Method that will try generate a new VEvent data from user inputs

        Returns
        -------
        messagebox
            if there is error
        """
        if isinstance(self.data, VEvent):
            return

        global core
        feed = {}

        try:
            for k, v in self.data.items():
                if k.startswith("DT"):
                    feed[k] = to_datetime(v)
                elif k == "DESCRIPTION":
                    feed[k] = v.get("1.0", END)
                else:
                    feed[k] = v.get()
        except ValueError:
            return messagebox.showerror("Failed to Create Event",
                                        "Please check your input, it's beyond acceptable number range")

        try:
            temp = VEvent(feed)
        except TypeError:
            return \
                messagebox.showerror("Failed to Create Event", "Please check your input, it's missing key details")
        except AssertionError:
            return messagebox.showerror("Failed to Create Event", "Event Start time is later than event end time")

        if core:
            core.data.append(temp)
        else:
            core = CalendarCore([temp])

        if self.root:
            self.root.destroy()
        messagebox.showinfo("Successfully Created Event", f"{feed['SUMMARY']} has been successfully created")
        self.reload()

    def generate(self):
        # Build window appearance
        self.root = Toplevel(self.previous)
        self.root.title("Add New Event" if not isinstance(self.data, VEvent) else "Edit Event")
        self.root.grab_set()
        self.root.minsize(width=415, height=600)
        bg2 = Frame(self.root, bg=self.bg)
        bg2.place(relwidth=1, relheight=1)
        # ------------------------------------------------------------------------------------------------
        name_label = LabelFrame(bg2, text="Event Name *", background=self.bg,
                                font=font.Font(family=self.font_family, size=12, weight=font.BOLD))
        name_label.grid(row=0, column=0, sticky=W, padx=10)
        self.data["SUMMARY"] = Entry(name_label, width=64)
        self.data["SUMMARY"].grid(row=0, column=1)
        # ------------------------------------------------------------------------------------------------
        self.data["DTSTART"] = self.build_datetime_selector(bg2, 1, "Start Date and Time *", 8)
        self.data["DTEND"] = self.build_datetime_selector(bg2, 2, "End Data and Time *", 10)
        # ------------------------------------------------------------------------------------------------
        class_label = LabelFrame(bg2, text="Event Type", background=self.bg,
                                 font=font.Font(family=self.font_family, size=12, weight=font.BOLD))
        class_label.grid(row=3, column=0, sticky=W, padx=10)
        self.data["CLASS"] = StringVar()
        self.data["CLASS"].set("PRIVATE")
        i = 0
        for a, b in [("Private", "PRIVATE"), ("Confidential", "CONFIDENTIAL"), ("Public", "PUBLIC")]:
            Radiobutton(class_label, text=a, value=b, variable=self.data["CLASS"], bg=self.bg,
                        activebackground=self.bg).grid(column=i, row=0, padx=28)
            i += 1
        # ------------------------------------------------------------------------------------------------
        priority_label = LabelFrame(bg2, text="Event Priority", background=self.bg,
                                    font=font.Font(family=self.font_family, size=12, weight=font.BOLD))
        priority_label.grid(row=4, column=0, sticky=W, padx=10)
        self.data["PRIORITY"] = IntVar()
        self.data["PRIORITY"].set(0)
        i = 0
        for a, b in [("Low", 0), ("Normal", 1), ("High", 2)]:
            Radiobutton(priority_label, text=a, value=b, variable=self.data["PRIORITY"], bg=self.bg,
                        activebackground=self.bg).grid(column=i, row=0, padx=35)
            i += 1
        # ------------------------------------------------------------------------------------------------
        self.data["STATUS"] = StringVar()
        self.data["STATUS"].set("CONFIRMED")
        status_label = LabelFrame(bg2, text="Event Status", background=self.bg,
                                  font=font.Font(family=self.font_family, size=12, weight=font.BOLD))
        status_label.grid(row=5, column=0, sticky=W, padx=10)
        i = 0
        for a, b in [("Confirmed", "CONFIRMED"), ("Tentative", "TENTATIVE"), ("Cancelled", "CANCELLED")]:
            Radiobutton(status_label, text=a, value=b, variable=self.data["STATUS"], bg=self.bg,
                        activebackground=self.bg).grid(column=i, row=0, padx=24, pady=2)
            i += 1
        # ------------------------------------------------------------------------------------------------
        location_label = LabelFrame(bg2, text="Location", background=self.bg,
                                    font=font.Font(family=self.font_family, size=12, weight=font.BOLD))
        location_label.grid(row=6, column=0, sticky=W, padx=10)
        self.data["LOCATION"] = Entry(location_label, width=64)
        self.data["LOCATION"].grid(row=0, column=1)
        # ------------------------------------------------------------------------------------------------
        info_label = LabelFrame(bg2, text="Description", background=self.bg,
                                font=font.Font(family=self.font_family, size=12, weight=font.BOLD))
        info_label.grid(row=7, column=0, sticky=W, padx=10)
        self.data["DESCRIPTION"] = Text(info_label, width=48, height=10)
        self.data["DESCRIPTION"].grid(row=0, column=1)
        # ------------------------------------------------------------------------------------------------
        if not isinstance(self.data, VEvent):
            Button(bg2, padx=10, pady=0, command=self.try_create, text="Create").grid(row=8, column=0)
        # TODO: update button

    # TODO: when implementing edit event, change values within the user input boxes (there is a lot)

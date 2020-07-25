import datetime
from tkinter import *
from tkcalendar import DateEntry
from Components.Calendar import CalendarCore, VEvent
from tkinter import filedialog, messagebox, font
from tzlocal import get_localzone


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
        local datetime from the user
    """
    ret = datetime.datetime.combine(arr[0].get_date(),
                                    datetime.time(int(arr[1].get()), int(arr[2].get()), int(arr[3].get())))
    return get_localzone().localize(ret)


def date_and_time_inputs(frame: LabelFrame, row: int, hour: int):
    Label(frame, text='Date', background="#f1c40f").grid(row=row, column=0)
    ret = [DateEntry(frame, width=10, borderwidth=2, background="#f1c40f")]
    ret[0].grid(row=row, column=1, pady=6)

    Label(frame, text='Hour', background="#00cec9").grid(row=row, column=2)
    ret.append(IntVar(frame, value=hour))
    Spinbox(frame, from_=0, to=23, width=6, textvariable=ret[1]).grid(row=row, column=3)

    Label(frame, text='Minutes', background="#00cec9").grid(row=row, column=4)
    ret.append(IntVar(frame))
    Spinbox(frame, from_=0, to=59, width=6, textvariable=ret[2]).grid(row=row, column=5)

    Label(frame, text='Seconds', background="#00cec9").grid(row=row, column=6)
    ret.append(IntVar(frame))
    Spinbox(frame, from_=0, to=59, width=6, textvariable=ret[3]).grid(row=row, column=7)

    return ret


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
        self.event_ref = exist_data
        self.inputs = {}
        self.rrule = {}
        self.rrule_end_mode = IntVar(value=0)
        self.root = None
        self.previous = previous
        self.reload = reload
        self.bg = "#2bcbba"
        self.rec_label = None
        self.bgf = None

    def build_datetime_selector(self, row: int, title: str, start: int = 6):
        """
        Generate label containing datetime input detectors base on passed information from the parameter

        Parameters
        ----------
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
        hold = LabelFrame(self.bgf, text=title, background=self.bg,
                          font=font.Font(family=self.font_family, size=12, weight=font.BOLD))
        hold.grid(row=row, column=0, padx=10, pady=5)
        ret = date_and_time_inputs(hold, 0, start)

        return ret

    def try_create(self):
        """
        Method that will try generate a new VEvent data from user inputs

        Returns
        -------
        messagebox
            if there is error
        """
        if isinstance(self.inputs, VEvent):
            return

        global core
        feed = {}

        try:
            for k, v in self.inputs.items():
                if k.startswith("DT"):
                    feed[k] = to_datetime(v)
                elif k == "DESCRIPTION":
                    feed[k] = v.get("1.0", END)
                else:
                    feed[k] = v.get()
        except ValueError:
            return messagebox.showerror("Failed to Create Event",
                                        "Please check your input, it's beyond acceptable number range")

        if self.rrule["FREQ"].get() != "NEVER":
            check = self.rrule["FREQ"].get()
            append = [f"FREQ={check}"]
            if self.rrule["INTERVAL"].get() > 1:
                append.append(f"INTERVAL={self.rrule['INTERVAL'].get()}")

            if check == "WEEKLY":
                temporary = []
                for k, v in self.rrule["BYDAY"].items():
                    if v.get() == 1:
                        temporary.append(k)
                if len(temporary) == 0:
                    return messagebox.showerror("Failed to Create Event", "For recurring weekly type event, "
                                                                          "make sure at least one weekday is selected")
                part = ",".join(temporary)
                append.append(f"BYDAY={part}")
            if check in ["MONTHLY, YEARLY"]:
                append.append(f"BYMONTHDAY={self.rrule['BYMONTHDAY']}")
                if check == "YEARLY":
                    append.append(f"BYMONTH={self.rrule['BYMONTH']}")

            check2 = self.rrule_end_mode.get()
            if check2 == 1:
                append.append(f"COUNT={self.rrule['COUNT'].get()}")
            if check2 == 2:
                temp = self.rrule["UNTIL"].get().replace("/", "")
                append.append(f"UNTIL={temp}")

            feed["RRULE"] = ";".join(append)

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

    def preset(self):
        # TODO process VEvent file
        self.inputs["SUMMARY"] = StringVar(value="New Event")
        self.inputs["CLASS"] = StringVar(value="PRIVATE")
        self.inputs["PRIORITY"] = IntVar(value=0)
        self.inputs["STATUS"] = StringVar(value="CONFIRMED")
        self.inputs["LOCATION"] = StringVar()

        self.rrule["FREQ"] = StringVar(value="NEVER")
        self.rrule["INTERVAL"] = IntVar(value=1)
        self.rrule["BYDAY"] = {}
        for i in ["SU", "MO", "TU", "WE", "TH", "FR", "SA"]:
            self.rrule["BYDAY"][i] = IntVar()
        self.rrule["COUNT"] = IntVar(value=1)
        self.rrule["BYMONTHDAY"] = datetime.datetime.now().day
        self.rrule["BYMONTH"] = datetime.datetime.now().month
        self.rrule["UNTIL"] = StringVar(value=datetime.datetime.now().strftime("%Y/%m/%d"))

    def generate(self):
        self.preset()
        # Build window appearance
        self.root = Toplevel(self.previous)
        self.root.title("Add New Event" if not isinstance(self.inputs, VEvent) else "Edit Event")
        self.root.grab_set()
        self.root.minsize(width=430, height=730)
        self.bgf = Frame(self.root, bg=self.bg)
        self.bgf.place(relwidth=1, relheight=1)
        # ------------------------------------------------------------------------------------------------
        name_label = LabelFrame(self.bgf, text="Event Name *", background=self.bg,
                                font=font.Font(family=self.font_family, size=12, weight=font.BOLD))
        name_label.grid(row=0, column=0, sticky=W, padx=10)
        Entry(name_label, width=66, textvariable=self.inputs["SUMMARY"]).grid(row=0, column=1)
        # ------------------------------------------------------------------------------------------------
        self.inputs["DTSTART"] = self.build_datetime_selector(1, "Start Date and Time *", 8)
        self.inputs["DTEND"] = self.build_datetime_selector(2, "End Data and Time *", 10)
        # ------------------------------------------------------------------------------------------------
        ref_frame = LabelFrame(self.bgf, text="Recurrence", background=self.bg, font=font.Font(
            family="Open Sans", size=12, weight=font.BOLD))
        ref_frame.grid(row=3, column=0, sticky=W, padx=10)
        select_frame = Frame(ref_frame, bg=self.bg)
        select_frame.grid(row=0, column=0)
        i = 0
        for a, b in [("Never", "NEVER"), ("Hourly", "HOURLY"), ("Daily", "DAILY"), ("Weekly", "WEEKLY"),
                     ("Monthly", "MONTHLY"), ("Yearly", "YEARLY")]:
            Radiobutton(select_frame, text=a, value=b, variable=self.rrule["FREQ"], bg=self.bg,
                        activebackground=self.bg, command=self.update_recur_display).grid(column=i, row=0, padx=2)
            i += 1
        self.rec_label = Frame(ref_frame, bg=self.bg)
        self.rec_label.grid(row=1, column=0)
        # ------------------------------------------------------------------------------------------------
        class_label = LabelFrame(self.bgf, text="Event Type", background=self.bg,
                                 font=font.Font(family=self.font_family, size=12, weight=font.BOLD))
        class_label.grid(row=4, column=0, sticky=W, padx=10)
        i = 0
        for a, b in [("Private", "PRIVATE"), ("Confidential", "CONFIDENTIAL"), ("Public", "PUBLIC")]:
            Radiobutton(class_label, text=a, value=b, variable=self.inputs["CLASS"], bg=self.bg,
                        activebackground=self.bg).grid(column=i, row=0, padx=30)
            i += 1
        # ------------------------------------------------------------------------------------------------
        priority_label = LabelFrame(self.bgf, text="Event Priority", background=self.bg,
                                    font=font.Font(family=self.font_family, size=12, weight=font.BOLD))
        priority_label.grid(row=5, column=0, sticky=W, padx=12)
        i = 0
        for a, b in [("Low", 0), ("Normal", 1), ("High", 2)]:
            Radiobutton(priority_label, text=a, value=b, variable=self.inputs["PRIORITY"], bg=self.bg,
                        activebackground=self.bg).grid(column=i, row=0, padx=37)
            i += 1
        # ------------------------------------------------------------------------------------------------
        status_label = LabelFrame(self.bgf, text="Event Status", background=self.bg,
                                  font=font.Font(family=self.font_family, size=12, weight=font.BOLD))
        status_label.grid(row=6, column=0, sticky=W, padx=10)
        i = 0
        for a, b in [("Confirmed", "CONFIRMED"), ("Tentative", "TENTATIVE"), ("Cancelled", "CANCELLED")]:
            Radiobutton(status_label, text=a, value=b, variable=self.inputs["STATUS"], bg=self.bg,
                        activebackground=self.bg).grid(column=i, row=0, padx=26, pady=2)
            i += 1
        # ------------------------------------------------------------------------------------------------
        location_label = LabelFrame(self.bgf, text="Location", background=self.bg,
                                    font=font.Font(family=self.font_family, size=12, weight=font.BOLD))
        location_label.grid(row=7, column=0, sticky=W, padx=10)
        Entry(location_label, width=66, textvariable=self.inputs["LOCATION"]).grid(row=0, column=1)
        # ------------------------------------------------------------------------------------------------
        info_label = LabelFrame(self.bgf, text="Description", background=self.bg,
                                font=font.Font(family=self.font_family, size=12, weight=font.BOLD))
        info_label.grid(row=8, column=0, sticky=W, padx=10)
        self.inputs["DESCRIPTION"] = Text(info_label, width=50, height=10)
        self.inputs["DESCRIPTION"].grid(row=0, column=1)
        # ------------------------------------------------------------------------------------------------
        if not isinstance(self.inputs, VEvent):
            Button(self.bgf, padx=10, pady=0, command=self.try_create, text="Create").grid(row=9, column=0)
        # TODO: when implementing edit event, change values within the user input boxes (there is a lot)

    def update_recur_display(self):
        if not self.rec_label:
            return

        guide = self.rrule["FREQ"].get()

        temp = self.rec_label.master
        self.rec_label.destroy()
        self.rec_label = Frame(temp, bg=self.bg)
        self.rec_label.grid(row=1, column=0)

        if guide == "NEVER":
            return

        grid1 = Frame(self.rec_label, bg=self.bg)
        grid1.grid(row=0, column=0)
        Label(grid1, text='Repeat Every ', background=self.bg).grid(row=0, column=0)
        Spinbox(grid1, from_=1, to=2000000000, width=6,
                textvariable=self.rrule["INTERVAL"]).grid(row=0, column=1)
        translate = str(guide).lower()[:-2] + "(s)" if guide != "DAILY" else "day(s)"
        Label(grid1, text=f" {translate}", background=self.bg).grid(row=0, column=2)

        if guide == "WEEKLY":
            grid2 = Frame(self.rec_label, bg=self.bg)
            grid2.grid(row=1, column=0)
            i = 1
            Label(grid2, text='*Repeat on:', background=self.bg).grid(row=1, column=0)
            for a, b in [("Sun", "SU"), ("Mon", "MO"), ("Tue", "TU"), ("Wed", "WE"), ("Thu", "TH"), ("Fri", "FR"),
                         ("Sat", "SA")]:
                Checkbutton(grid2, text=a, variable=self.rrule["BYDAY"][b],
                            bg=self.bg, activebackground=self.bg).grid(row=1, column=i)
                i += 1

        grid3 = Frame(self.rec_label, bg=self.bg)
        grid3.grid(row=2, column=0)
        Label(grid3, text='Ends:', background=self.bg).grid(row=0, column=0)
        note = []

        def change():
            for item in note:
                item.destroy()
            note.clear()

            if self.rrule_end_mode.get() == 1:
                note.append(Spinbox(grid3, from_=1, to=2000000000, width=6, textvariable=self.rrule["COUNT"]))
                note[0].grid(row=0, column=i)
                note.append(Label(grid3, background=self.bg, text=" Time(s)"))
                note[1].grid(column=i + 1, row=0)
            if self.rrule_end_mode.get() == 2:
                note.append(DateEntry(grid3, width=10, borderwidth=2, background="#f1c40f",
                                      date_pattern='y/mm/dd', textvariable=self.rrule["UNTIL"]))
                note[0].grid(row=0, column=i)

        i = 1
        for a, b in [("Never", 0), ("After", 1), ("On", 2)]:
            Radiobutton(grid3, text=a, value=b, variable=self.rrule_end_mode, bg=self.bg, command=change,
                        activebackground=self.bg).grid(column=i, row=0)
            i += 1
        change()

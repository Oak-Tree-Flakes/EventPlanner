import pytz
import datetime
from tkinter import *
from tkcalendar import DateEntry
from Components.Calendar import CalendarCore, VEvent
from tkinter import filedialog, messagebox, font


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
        self.font_family = "Open Sans"
        self.root = Tk()
        self.root.title("Event Planner")
        self.core = None
        self.details = None
        self.new = True
        self.root.minsize(width=800, height=600)
        self.background = Frame(self.root, bg=self.bg_color)
        self.background.place(relwidth=1, relheight=1)

        # build main window looks
        self.menu_bar = Menu(self.root, tearoff=0)

        def save_as():
            return self.save_file(True)

        def new_data():
            self.core = None
            self.location = ""
            self.reload_display()

        file_sub_menu = Menu(self.menu_bar, tearoff=0)
        file_sub_menu.add_command(label="New", command=new_data)
        file_sub_menu.add_command(label="Open", command=self.get_file)
        file_sub_menu.add_command(label="Save", command=self.save_file)
        file_sub_menu.add_command(label="Save As...", command=save_as)
        file_sub_menu.add_separator()
        file_sub_menu.add_command(label="Exit", command=self.root.quit)
        Button(self.background, padx=2, pady=2, command=self.event_window, text="New Event").\
            grid(row=0, column=0, pady=10, padx=5)

        self.menu_bar.add_cascade(label="File", menu=file_sub_menu)

        self.root.config(menu=self.menu_bar)
        self.root.mainloop()

    def event_window(self, exist: VEvent = None):
        """
        Method for generating new window

        Parameters
        ----------
        exist: VEvent
            if VEvent is provided, information will be filled through VEvent class.
        """

        # TODO: when implementing edit event, change values within the user input boxes (there is a lot)

        def build_datetime_selector(root, row: int, title: str, start: int = 6):
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
            hold = LabelFrame(root, text=title, background="#2bcbba",
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
            # ------------------------------------------------------------

        # Build window appearance
        top = Toplevel(self.root)
        top.title("Add New Event")
        top.grab_set()
        top.minsize(width=415, height=600)
        bg2 = Frame(top, bg="#2bcbba")
        bg2.place(relwidth=1, relheight=1)

        name_label = LabelFrame(bg2, text="Event Name *", background="#2bcbba",
                                font=font.Font(family=self.font_family, size=12, weight=font.BOLD))
        name_label.grid(row=0, column=0, sticky=W, padx=10)
        name_data = Entry(name_label, width=64)
        name_data.grid(row=0, column=1)

        before_data = build_datetime_selector(bg2, 1, "Start Date and Time *")
        after_data = build_datetime_selector(bg2, 2, "End Data and Time *", 9)

        info_label = LabelFrame(bg2, text="Event Information", background="#2bcbba",
                                font=font.Font(family=self.font_family, size=12, weight=font.BOLD))
        info_label.grid(row=3, column=0, sticky=W, padx=10)
        info_data = Text(info_label, width=48, height=10)
        info_data.grid(row=0, column=1)

        location_label = LabelFrame(bg2, text="Event Location", background="#2bcbba",
                                    font=font.Font(family=self.font_family, size=12, weight=font.BOLD))
        location_label.grid(row=4, column=0, sticky=W, padx=10)
        location_data = Entry(location_label, width=64)
        location_data.grid(row=0, column=1)

        def to_datetime(arr: iter):
            """
            Method to generate a UTC datetime from list of user input options

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
            ret = ret.astimezone(local_zone)
            return ret.astimezone(pytz.utc)

        def try_create():
            """
            Method that will try generate a new VEvent data from user inputs

            Returns
            -------
            messagebox
                if there is error
            """
            try:
                feed = {"SUMMARY": name_data.get(), "LOCATION": location_data.get(),
                        "DTSTART": to_datetime(before_data), "DTEND": to_datetime(after_data),
                        "DESCRIPTION": info_data.get("1.0", END)}
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

            if self.core:
                self.core.data.append(temp)
            else:
                self.core = CalendarCore([temp])

            top.destroy()
            messagebox.showinfo("Successfully Created Event", f"{feed['SUMMARY']} has been successfully created")
            self.reload_display()

            # TODO: when implementing edit event, make sure command isn't linked to try_create

        Button(bg2, padx=10, pady=0, command=try_create, text="Create").grid(row=5, column=0)

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
        if not self.core:
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
            self.core.write_file(self.location)

        messagebox.showinfo("Success!", f"Calendar data has been saved to:\n{self.location}")

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
            self.core = CalendarCore(self.location)
        except TypeError:
            return messagebox.showerror("Unknown File Type", "Only .ics files are supported")
        self.new = False

        self.reload_display()

    def reload_display(self):
        # reloading temporary data view of the CalendarCore, may be removed in the future
        temp = str(self.core)
        if self.details:
            self.details.destroy()

        self.details = Label(self.background, text=temp, fg="white", bg="black", justify=LEFT)
        self.details.grid(row=1, column=1) if self.core else self.details.destroy()
        self.root.title(f"Event Planner - {self.location}") if self.location != "" else self.root.title("Event Planner")

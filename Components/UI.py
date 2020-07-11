import pytz
import datetime
from tkinter import *
from tkcalendar import DateEntry
from Components.Calendar import CalendarCore, VEvent
from tkinter import filedialog, messagebox, font


class Interface:

    def __init__(self):
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

        self.details = Label(self.background, text=temp, fg="white", bg="black", justify=LEFT)
        self.details.grid(row=2, column=1)

    def add_window(self):
        # Build looks
        top = Toplevel(self.root)
        top.title("Add New Event")
        top.grab_set()
        top.minsize(width=800, height=600)
        bg2 = Frame(top, bg="#2bcbba")
        bg2.place(relwidth=1, relheight=1)

        def build_datetime_selector(root, row: int, title: str, start: int = 6):
            hold = LabelFrame(root, text=title, background="#2bcbba",
                              font=font.Font(family=self.font_family, size=12, weight=font.BOLD))
            hold.grid(row=row, column=0, padx=10, pady=5)
            Label(hold, text='Date', background="#f1c40f").grid(row=0, column=0)
            ret = [DateEntry(hold, width=8, borderwidth=2, background="#f1c40f")]

            twenty_four = []
            for i in range(0, 24):
                twenty_four.append(i)
            ret[0].grid(row=0, column=1, pady=6)
            temp = IntVar(hold)
            temp.set(start)
            ret.append(temp)
            Label(hold, text='Hour', background="#00cec9").grid(row=0, column=2)
            OptionMenu(hold, temp, *twenty_four).grid(row=0, column=3)

            sixty = []
            for i in range(0, 61):
                sixty.append(i)
            temp = IntVar(hold)
            temp.set(0)
            ret.append(temp)
            Label(hold, text='Minutes', background="#00cec9").grid(row=0, column=4)
            OptionMenu(hold, temp, *sixty).grid(row=0, column=5)

            temp = IntVar(hold)
            temp.set(0)
            ret.append(temp)
            Label(hold, text='Seconds', background="#00cec9").grid(row=0, column=6)
            OptionMenu(hold, temp, *sixty).grid(row=0, column=7)

            return ret

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

        def to_datetime(arr: list):
            ret = datetime.datetime.combine(arr[0].get_date(), datetime.time(arr[1].get(), arr[2].get(), arr[3].get()))
            # https://stackoverflow.com/questions/2720319/python-figure-out-local-timezone
            local_zone = datetime.datetime.now().astimezone().tzinfo
            ret = ret.astimezone(local_zone)
            return ret.astimezone(pytz.utc)

        def try_create():
            feed = {"SUMMARY": name_data.get(), "LOCATION": location_data.get(),
                    "DTSTART": to_datetime(before_data), "DTEND": to_datetime(after_data),
                    "DESCRIPTION": info_data.get("1.0", END)}
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

        Button(bg2, padx=10, pady=0, command=try_create, text="Create").grid(row=5, column=0)

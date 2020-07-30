import pytz
import typing
import datetime
from tzlocal import get_localzone

file_tz = get_localzone()


class VEvent:
    """
    VEvent class aim to represent VEVENT within ICS files

    Attributes
    ----------
    data: dict
        dictionary storing data for an VEvent Object
    recur: bool
        whether or not the Event is a recurrence one
    """

    def __init__(self, pack: dict):
        """
        Constructor of VEvent class

        Parameters
        ----------
        pack: dict
            pass in dictionary data for initialization

        Raises
        ------
        TypeError
            if dictionary from parameter don't contain enough data
        """
        self.data = {}
        self.recur = False
        self.update(pack)

    def update(self, data: dict):
        """
        Method to update self.data within VEvent

        Parameters
        ----------
        data: dict
            pass in dictionary data for updating self.data

        Raises
        ------
        TypeError
            if dictionary from parameter don't contain enough data
        """
        self.data.clear()

        for key, value in data.items():
            if isinstance(value, str):
                if key.startswith("DT"):
                    if value.endswith("Z"):
                        self.data[key] = pytz.UTC.localize(datetime.datetime.strptime(value, "%Y%m%dT%H%M%SZ"))
                    else:
                        global file_tz
                        self.data[key] = file_tz.localize(datetime.datetime.strptime(value, "%Y%m%dT%H%M%S"))
                elif key == "LOCATION":
                    self.data[key] = value.replace("\,", ",")
                else:
                    self.data[key] = value
            else:
                if key == "RRULE":
                    self.recur = True
                self.data[key] = value

        if not self.check():
            raise TypeError("Illegal VEvent: Missing required entry")

        if self.data["DTSTART"] > self.data["DTEND"]:
            raise AssertionError("Event end time can not be before the event start time")

        if "UID" not in self.data:
            temp = f'{datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")}>{self.data["SUMMARY"]}'
            self.data["UID"] = f"{temp}@oaktreeEPlanner.com"

    def check(self):
        """
        Method that checks whether or not the current data is a valid form of VEvent

        Returns
        -------
        bool
            whether or not the class data is legal
        """
        for i in ["DTSTART", "DTEND", "SUMMARY"]:
            try:
                temp = self.data[i]
                if not temp or temp == "":
                    return False
            except KeyError:
                return False
        return True

    def __str__(self):
        """
        Overrides the default "to string" of python object

        Returns
        -------
        str
            String conversion of the class
        """
        return self.stringify()

    def __repr__(self):
        # TODO: here only for temporary visualization within console, remove when done
        return self.stringify(datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ"))

    def stringify(self, stamp: str = None):
        ret = "BEGIN:VEVENT\n"

        if stamp and "DTSTAMP" not in self.data:
            ret += f"DTSTAMP:{stamp}\n"

        for k, v in self.data.items():
            if k.startswith("DT"):
                v = v.strftime("%Y%m%dT%H%M%SZ" if v.tzinfo == pytz.UTC else "%Y%m%dT%H%M%S")
            elif k == "LOCATION":
                v = v.replace(",", "\,")

            if v not in ["", "\n"]:
                ret += f"{k}:{v}\n"
        ret += "END:VEVENT\n"

        return ret

    def __lt__(self, other):
        return self.data["DTSTART"] < other.data["DTSTART"]

    def __eq__(self, other):
        return self.data["DTSTART"] == other.data["DTSTART"]


class CalendarCore:
    """
    CalendarCore class that simulates data from an ICS file

    Attributes
    ----------
    file: File
        the file object if class data is gathered through opening an ICS file else nothing
    data: list
        list containing VEvents
    fail: int
        how many objects failed to load (won't check if initialization is a list)
    location: str
        location of the file being read if applicable
    """

    def __init__(self, package: typing.Union[str, list]):
        """
        Constructor for CalendarCore class

        Parameters
        ----------
        package: typing.Union[str, list]
            if package is string, class will attempt to open the string as a file specification and scan it
            if package is list, it will be appended to data

        Raises
        ------
        TypeError
            if the passed in package string for the file location isn't supported
        """
        if isinstance(package, str):
            if not package.endswith(".ics"):
                raise TypeError("Unsupported file format")

        global file_tz
        self.timezone = get_localzone()
        file_tz = self.timezone

        self.file = None
        self.fail = 0
        self.location = ""
        if isinstance(package, list):
            self.data = package
        else:
            self.data = []
            self.read_file(package)
            self.location = package

    def __del__(self):
        """
        Destructor of the CalendarCore class to close any lingering file the class have opened
        """
        try:
            if self.file:
                self.file.close()
        except AttributeError:
            pass

    def __str__(self):
        """
        Overrides the default "to string" of python object

        Returns
        -------
        str
            String conversion of the class
        """
        ret = "BEGIN:VCALENDAR\nPRODID:-//Team Oak Tree Flakes//Event Planner v0.5//EN\nVERSION:2.0\n" \
              f"X-WR-TIMEZONE:{self.timezone}\n\n"

        for i in self.data:
            ret += f"{i}\n"

        ret += "END:VCALENDAR\n"
        return ret

    def read_file(self, file: str):
        """
        Method to read data from the specified file and append it to data attribute

        Parameters
        ----------
        file: str
            location of the file to read data from
        """
        if self.file:
            self.file.close()

        self.file = open(file)
        begin = False
        read_event = False

        temp_list = self.file.read().split("\n")
        temp_event = {}

        for i in temp_list:
            begin = (i == "BEGIN:VCALENDAR") or begin
            if begin:
                read_event = (i != "END:VEVENT") and ((i == "BEGIN:VEVENT") or read_event)

                if i == "END:VEVENT":
                    # after reaching line of END:VEVENT, append the current temp_event onto data list
                    try:
                        self.data.append(VEvent(temp_event))
                    except TypeError:
                        self.fail += 1

                    temp_event.clear()
                    read_event = False
                elif read_event and i not in ["", "BEGIN:VEVENT"]:
                    # only executes if the line isn't empty and after BEGIN:VEVENT
                    if not (i.startswith("DT") and i.find(";") != -1):
                        if i.find(":") != -1:
                            temp = i.split(':', 1)
                            temp_event[temp[0]] = temp[1]
                    else:
                        temp = i.split(';')
                        temp_event[temp[0]] = temp[1].split(":")
                else:
                    temp = i.split(":", 1)
                    if temp[0] == "X-WR-TIMEZONE":
                        self.timezone = pytz.timezone(temp[1])

            if i == "END:VCALENDAR":
                # EOF indicator
                break

    def write_file(self, file: str = None):
        """
        Method to save class content to opened file or the passed in file location

        Parameters
        ----------
        file: str
            place to save the file to

        Raises
        ------
        ValueError
            if there is no location to write to
        """
        if not self.file and not file:
            raise ValueError("Nothing to write to")

        if self.file:
            self.file.close()

        self.location = self.location if not file else file
        self.file = open(self.location, mode="w")

        now = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        write = "BEGIN:VCALENDAR\nPRODID:-//Team Oak Tree Flakes//Event Planner v0.5//EN\nVERSION:2.0\n" \
              f"X-WR-TIMEZONE:{self.timezone}\n"

        for i in self.data:
            write += f"{i.stringify(now)}"

        write += "END:VCALENDAR\n"

        self.file.write(write)
        self.file.close()
        self.file = open(self.location)

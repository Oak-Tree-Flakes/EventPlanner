import pytz
import datetime
from Components.Calendar import CalendarCore, VEvent


future = datetime.datetime(2020, 8, 13, 20, 0, 0, 0, pytz.UTC)
write_to = CalendarCore([VEvent({"DTSTART": future, "DTEND": future + datetime.timedelta(hours=3),
                                 "SUMMARY": "Study for exam",
                                 "LOCATION": "2550 McCarthy Mall, Honolulu, HI 96822, USA"})
                         ])
print(f"Contents to write to Test.ics file:\n{write_to}\n")
write_to.write_file("Example ICS Files/Exam.ics")
print("All Done!")

import datetime
from Components.Calendar import CalendarCore, VEvent

core = CalendarCore("Example ICS Files/Example.ics")
print(f"Contents of Example.ics:\n{core}\n=================================================================")

future = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
write_to = CalendarCore([VEvent({"DTSTART": future, "DTEND": future + datetime.timedelta(hours=3),
                                 "DESCRIPTION": "ICS file generated through Python!",
                                 "SUMMARY": "An hour from present!"})
                         ])
print(f"Contents to write to Test.ics file:\n{write_to}\n")
write_to.write_file("Example ICS Files/Test.ics")
print("All Done!")

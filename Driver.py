from Components.Calendar import CalendarCore, VEvent

core = CalendarCore("Example ICS Files/Example.ics")
print(f"Contents of Example.ics:\n{core}\n=================================================================")

write_to = CalendarCore([VEvent({"DTSTART": "20200625T120000Z", "DTEND": "20200625T180000Z",
                                 "SUMMARY": "ICS file generated through Python!"})
                         ])
print(f"Contents to write to Test.ics file:\n{write_to}\n")
write_to.write_file("Example ICS Files/Test.ics")
print("All Done!")

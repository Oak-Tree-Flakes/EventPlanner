import datetime
from Components.Calendar import VEvent, CalendarCore

print("Test Event UI w/ existing data")

now = datetime.datetime.now()
event1 = VEvent({"DTSTART": now + datetime.timedelta(days=12), "DTEND": now + datetime.timedelta(hours=3, days=12),
                 "CLASS": "PUBLIC", "STATUS": "CONFIRMED",
                 "SUMMARY": "Last", "DESCRIPTION": "Future", "PRIORITY": 2})

event2 = VEvent({"DTSTART": now, "DTEND": now + datetime.timedelta(hours=3), "CLASS": "PUBLIC", "STATUS": "CANCELLED",
                 "SUMMARY": "Yahooo", "DESCRIPTION": "In the middle", "PRIORITY": 1,
                 "LOCATION": "Honolulu, Hawaii, USA", "RRULE": "FREQ=DAILY;INTERVAL=5;UNTIL=20201225"})

event3 = VEvent({"DTSTART": now - datetime.timedelta(days=29, hours=6),
                 "DTEND": now - datetime.timedelta(days=29), "CLASS": "PUBLIC", "STATUS": "CANCELLED",
                 "SUMMARY": "First", "DESCRIPTION": "Hey hey hey!", "PRIORITY": 0,
                 "LOCATION": "Honolulu, Hawaii, USA"})

core = CalendarCore([event1, event2, event3])
core.data.sort()

print(core)

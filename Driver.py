import datetime
from tkinter import *
from Components.UI import EventUI
from Components.Calendar import VEvent

print("Test Event UI w/ existing data")

now = datetime.datetime.now()
event = VEvent({"DTSTART": now, "DTEND": now + datetime.timedelta(hours=3), "CLASS": "PUBLIC", "STATUS": "CANCELLED",
                "SUMMARY": "Yahooo", "DESCRIPTION": "Hey hey hey!", "PRIORITY": 1,
                "LOCATION": "Honolulu, Hawaii, USA", "RRULE": "FREQ=DAILY;INTERVAL=5;UNTIL=20201225"})

testUI = Tk()
testUI.minsize(900, 600)
bg = Frame(testUI, bg="black")
bg.place(relwidth=1, relheight=1)
details = Label(bg, text="Clear", fg="white", bg="black", justify=LEFT)
testUI.title("VEvent Tester")


def reload():
    temp = str(event)
    global details
    details.destroy()

    details = Label(bg, text=temp, fg="white", bg="black", justify=LEFT)
    details.grid(row=0, column=0)


reload()
EventUI(testUI, reload, event).generate()

testUI.mainloop()

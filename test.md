TEST CASES

Step 1. 
    
    Action: select "New Event"
    Expected Result: new window pop up with following options - 
        Event Name, Start Date and Time, End Date and Time, Recurrence,
        Event Type, Event Priority, Event Status, Location, Description
        and a Create button
    
Step 2. 
    
    Action: input the following
            Event Name: Test
            Start Date and Time: 7/14/2020, 6:30:30
            End Date and Time: 7/15/2020, 8:40:20
            Event Information: Testing
            Event Location: Honolulu
      then click "Create"
    Expected Result: window pop up informing successful event creation 
        
Step 3.
    
    Action: click "ok" on window
    Expected Result: the event can be seen on main page with all 
    relevant data
    
Step 4. 
    
    Action: On the event tab, select "Edit"
    Expected Result: new window pop up with following options - 
        Event Name, Start Date and Time, End Date and Time, Recurrence,
        Event Type, Event Priority, Event Status, Location, Description
        and a Create button
        
Step 5. 

    Action: Change the end date to "7/14/2020" and click "Update"
        then "ok"
    Expected Result: the event appears on the main screen with the 
        updated date visible    
    
Step 6. 
    
    Action: click "Save"
    Expected Result: pop up window to set where file is saved
    
Step 7.

    Action: set the file to save to some part of the computer call it 
        "test" then click "Save"
    Expected Result: A file named "test" is created in the location 
        allocated

Step 8.

    Action: import the "test.ics" file to calendar program
    Expected Result: All information set within the test file is 
        displayed within the calendar program

Step 9.

    Action: close then reopen program
    Expected Result: page has no event data listed
    
Step 10.

    Action: click "Load File" and select the "test.ics" file  
    Expected Result: the test event's information is displayed

Step 11.

    Action: Click "Edit" on the event's tab
    Expected Result: new window pop up with following options - 
        Event Name, Start Date and Time, End Date and Time, Recurrence,
        Event Type, Event Priority, Event Status, Location, Description
        and a Create button
        
Step 12. 

    Action: Change the status to "Cancelled" and click "Update"
        then "ok"
    Expected Result: the event appears on the main screen with the 
        updated date visible  

Step 13. 
    
    Action: select "Edit" at the top of the screen then click 
        "New Event" 
    Expected Result: new window pop up with following options - 
        Event Name, Start Date and Time, End Date and Time, Recurrence,
        Event Type, Event Priority, Event Status, Location, Description
        and a Create button

Step 14.

    Action: input nothing, then click "Create"
    Expected result: window pop up, informing of failed event creation
        due to input missing key details
        
Step 15.

    Action: input the following
            Event Name: Test 2
            Start Date and Time: 8/20/2020, 10:30:30
            End Date and Time: 8/15/2020, 8:40:20
        then click "Create"
    Expected Result: window pop up informing of failed event creation due 
        to starting event time being after the ending event time

Step 16. 

    Action: change the Start Date and Time: 8/15/2020, 8:10:10
            change the End Date and Time: 8/15/2020, 6:10:10
        the click "Create"
    Expected Result: window pop up informing of failed event creation due 
        to starting event time being after the ending event time
        
Step 17.

    Action: change the Start Date and Time: 8/15/2020, 8:10:10
            change the End Date and Time: 8/15/2020, 8:09:10
        the click "Create"
    Expected Result: window pop up informing of failed event creation due 
        to starting event time being after the ending event time
    
Step 18.

    Action: change the Start Date and Time: 8/15/2020, 8:10:10
            change the End Date and Time: 8/15/2020, 8:10:09
        the click "Create"
    Expected Result: window pop up informing of failed event creation due 
        to starting event time being after the ending event time
        
Step 19.

    Action: change the Start Date and Time: 8/15/2020, 8:10:10
            change the End Date and Time: 8/15/2020, 8:10:10
        the click "Create"
    Expected Result: window pop up informing successful event creation 
    
Step 20.     
    
    Action: click "ok" on window
    Expected Result: the event can be seen with the other events, 
        location and description fields are empty
        
Step 21.

    Action: select "File" and click "save"
    Expected Result: The new information is updated within the file 
        
Step 22.

    Action: import "test.ics" file to calendar program
    Expected Result: All information set within the test file is 
        displayed within the calendar program
        
Step 23.
        
    Action: select "Edit" at the top of the screen then click 
        "New Event" 
    Expected Result: new window pop up with following options - 
        Event Name, Start Date and Time, End Date and Time, Recurrence,
        Event Type, Event Priority, Event Status, Location, Description
        and a Create button
    
Step 24. 
    
    Action: input the following
            Event Name: Test 3
            Start Date and Time: 9/20/2020, 10:30:30
            End Date and Time: 9/20/2020, 11:40:20
            Recurrence: Daily
            Event Type: Public
            Event Priority: High
            Event Status: Tentative
        Then click "Create"
    Expected Result: window pop up informing successful event creation

Step 25.
    
    Action: input the following
            Event Name: Test 3
            Start Date and Time: 9/20/2020, 10:30:30
            End Date and Time: 9/20/2020, 11:40:20
            Recurrence: Daily
            Event Type: Public
            Event Priority: High
            Event Status: Tentative
        Then click "Create"
    Expected Result: window pop up informing successful event creation
        two "Test 3" events should now exist

Step 26.

    Action: select "File" and click "save"
    Expected Result: The new information is updated within the file        

Step 27. 

    Action: import "test.ics" file to calendar program
    Expected Result: All information set within the test file is 
        displayed within the calendar program, with two identical 
        "Test 3" both cancelled

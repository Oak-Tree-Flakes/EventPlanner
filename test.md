TEST CASES

Step 1. 
    
    Action: select "New Event"  
    Expected Result: new window pop up with following options - Event Name, 
        Start Date and Time, End Date and Time, Event Information, 
        Event Description, and a Create button
    
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
    Expected Result: the event can be seen on main page with all relevant 
        data
        
Step 4. 
    
    Action: click "Save"
    Expected Result: pop up window to set where file is saved
    
Step 5.

    Action: set the file to save to some part of the computer then 
        click "save"
    Expected Result: The related file is created in the location allocated

Step 6.

    Action: close then reopen program
    Expected Result: page has no event data listed
    
Step 7.

    Action: click "Load File" and select the .ics file we just created 
    Expected Result: the test event's information is displayed
    
Step 8. 
    
    Action: select "New Event" 
    Expected Result: new window pop up with following options - Event Name, 
        Start Date and Time, End Date and Time, Event Information, 
        Event Description, and a Create button

Step 9.

    Action: input nothing, then click "Create"
    Expected result: window pop up, informing of failed event creation
        due to input missing key details
        
Step 10.

    Action: input the following
            Event Name: Test 2
            Start Date and Time: 8/20/2020, 10:30:30
            End Date and Time: 8/15/2020, 8:40:20
        then click "Create"
    Expected Result: window pop up informing of failed event creation due 
        to starting event time being after the ending event time

Step 11. 

    Action: change the Start Date and Time: 8/15/2020, 8:10:10
            change the End Date and Time: 8/15/2020, 6:10:10
        the click "Create"
    Expected Result: window pop up informing of failed event creation due 
        to starting event time being after the ending event time
        
Step 12.

    Action: change the Start Date and Time: 8/15/2020, 8:10:10
            change the End Date and Time: 8/15/2020, 8:09:10
        the click "Create"
    Expected Result: window pop up informing of failed event creation due 
        to starting event time being after the ending event time
    
Step 13.

    Action: change the Start Date and Time: 8/15/2020, 8:10:10
            change the End Date and Time: 8/15/2020, 8:10:09
        the click "Create"
    Expected Result: window pop up informing of failed event creation due 
        to starting event time being after the ending event time
        
Step 14.

    Action: change the Start Date and Time: 8/15/2020, 8:10:10
            change the End Date and Time: 8/15/2020, 8:10:10
        the click "Create"
    Expected Result: window pop up informing successful event creation 
Step 15.     
    
    Action: click "ok" on window
    Expected Result: the event can be seen with the other events, 
        location and description fields are empty
    
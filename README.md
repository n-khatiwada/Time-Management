# Time-Management

Time-Management is an automation program written in Python and an extension of <a href="https://github.com/samg/timetrap">time-scrapper</a> program written in Ruby. The program, right now, is not complete, but I aim to make it extensible and add features on the way. Current characteristics include:

* Based on generic schedule (fixed meetings, appointments, lectures), the program builds the schedule for the next day.
* Program manages _Deep Work_ and _Shallow Work_ timesheets, so you can always know how to priotize your time for the work.
*  Program calculates all free time you didn't work in the working time (say 7 a.m. to 10 p.m.).
* The scheudle's status is shown in the <a href="https://github.com/polybar/polybar">polybar</a>, so always infront of your eyes.
* The program has easy Pause/Play button develope in <a href="https://github.com/davatorium/rofi">rofi</a>, which helps to manage your schedule, if something goes unplanned.
* The schedule runs in <a href="https://en.wikipedia.org/wiki/Cron">Cron</a>, so you don't need to worry about forgetting to update the schedule.

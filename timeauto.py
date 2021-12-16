import os
import subprocess
from humanfriendly import format_timespan
import numpy as np
from datetime import datetime, timedelta

def timesheet_tomorrow(work_type):

    # Format
    switch = 't s {}'.format(work_type)
    entry_format = "t in --at 'tomorrow {}' {}"
    out_format = "t out --at 'tomorrow {}'"

    # Entries
    # time_in_entries, time_out_entries, planung = generic_schedule(work_type)
    time_in_entries, time_out_entries, planung = tomorrow_events(work_type)
    
    # Later, move verification part to different function that returns True or False
    # Verification of entries
    time_in_entries, time_out_entries, planung = list(filter(None, time_in_entries)), list(filter(None, time_out_entries)), list(filter(None, planung))   # Filtering out empty entries if there exists.
    ntin = len(time_in_entries)
    ntout = len(time_out_entries)
    npl = len(planung)
    if ntin != ntout or ntin != npl or ntout != npl:
            print("The length of the entries do not match.")
            return 1 
    for i in range(ntin):
        x = datetime.strptime(time_in_entries[i], '%H:%M')
        y = datetime.strptime(time_out_entries[i], '%H:%M')
        if x > y:
            print("Exit time is ahead of entry in {} being entry time:{} and exit time:{}".format(work_type, x, y))
            return 1
        if i < (ntin - 1):
            x = datetime.strptime(time_in_entries[i+1], '%H:%M')
            y = datetime.strptime(time_in_entries[i], '%H:%M')
            if x < y:
                print("There is a clash in the schedule in {} entry time being {}.".format(work_type, x))
                return 1

    # Later, make an algorithm to either suggest or automatically fix the errors of entries with notifications if entries have been fixed
    
    queries = []
    for i in range(len(time_in_entries)):
        entry = entry_format.format(time_in_entries[i], planung[i])
        exit = out_format.format(time_out_entries[i])
        query = entry + ' && ' + exit
        queries.append(query)

    final_query = switch + ' && ' + ' && '.join(queries)
    
    return final_query

def generic_schedule(work_type):
    

    # Later, I'll keep the schedule in a separate file.
    # Deep Work
    if work_type == 'Deep Work':
        monday = {
                '': ['7:00', '8:30'],
                '': ['', '']
                }
        tuesday = {
                '': ['', ''],
                '': ['', '']
                }
        wednesday = {}
        thursday = {
                '': ['', '']
                }
        friday = {}
        saturday = {}
        sunday = {}

    # Shallow Work
    else:
        monday = {
                '': ['7:00', '8:30'],
                '': ['9:30', '11:30']
                }
        tuesday = {
                '': ['7:00', '8:30'],
                '': ['9:30', '12:30']
                }
        wednesday = {
                'work5': ['8:00', '10:00']
                }
        thursday = {}
        friday = {
                'work6': ['7:00', '9:00']
                }
        saturday = {}
        sunday = {}

    week_day = datetime.today().weekday()
    options = {
            0: monday,
            1: tuesday,
            2: wednesday,
            3: thursday,
            4: friday,
            5: saturday,
            6: sunday
            }
    all_entries = options.get(week_day)
    time_entries, work_entries = np.array(list(all_entries.values())), list(all_entries.keys())
    time_in_entries, time_out_entries = list(time_entries[:,0]), list(time_entries[:,1])

    return time_in_entries, time_out_entries, work_entries
    
   
def tomorrow_events(work_type):

    ''' Reads a file and gets events for tomorrow. '''
    f = open('events.txt', 'r')
    out = f.read().splitlines()
    events = [' '.join([x]).split() for x in out]
    dtie, dtoe, dp, stie, stoe, sp = [], [], [], [], [], []
    for i in range(len(events)):
        if events[i][0] == 'd':
            # Deep Work
            dtie.append(events[i][2])
            dtoe.append(events[i][3])
            dp.append(events[i][1])
        if events[i][0] == 's':
            # Shallow Work
            stie.append(events[i][2])
            stoe.append(events[i][3])
            sp.append(events[i][1])
    if work_type == 'Deep Work':
        return dtie, dtoe, dp
    else:
        return stie, stoe, sp

def free_times():
    ''' Calculates the free times of the day '''

    # Finding free time in the schedule
    start_times, end_times = [], []
    timesheets = ['Deep Work', 'Shallow Work']
    for j in range(2): # No. of Time-Sheets: Deep Work and Shallow Work
        os.system('t s {} >/dev/null 2>&1 '.format(timesheets[j]))
        # For tomorrow: 't d --start "tomorrow" --format csv'
        output = subprocess.run(['t today --format csv'], shell=True, capture_output=True, text=True).stdout.splitlines()[1:]
        print(output)
        for i in range(len(output)):
            event = [output[i]][0].split(',')
            event_start_date = datetime.strptime(event[0], '"%Y-%m-%d %H:%M:%S"')
            event_end_date = datetime.strptime(event[1], '"%Y-%m-%d %H:%M:%S"')
            start_time, end_time = event_start_date.time(), event_end_date.time()
            start_times.append(timedelta(hours=start_time.hour, minutes=start_time.minute))
            end_times.append(timedelta(hours=end_time.hour, minutes=end_time.minute))
    start_times.sort(), end_times.sort()
    start_time, end_time = start_times[1:], end_times[:-1]
    free_times = sum([(x-y).total_seconds() for x, y in zip(start_time, end_time)])
    early_time = datetime.strptime('7:00:00', '%H:%M:%S')
    et = timedelta(hours=early_time.hour, minutes=early_time.minute)
    bed_time = datetime.strptime('22:00:00', '%H:%M:%S')
    bt = timedelta(hours=bed_time.hour, minutes=bed_time.minute)
    boundary_free_time = ((start_times[0]-et) + (bt-end_times[-1])).total_seconds()
    total_free_time = format_timespan(free_times + boundary_free_time)
    return total_free_time

def timesheet_update():
    os.system(timesheet_tomorrow('Deep Work'))
    os.system(timesheet_tomorrow('Shallow Work'))
    os.system('Time-sheet successfully updated for tomorrow. Printing . . .')
    os.system('t s Deep Work && t week')
    os.system('t s Shallow Work && t week')

timesheet_update()

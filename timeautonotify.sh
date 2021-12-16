#!/bin/bash
notify-send 'Please update the events for tomorrow.' 'A schedule will be printed in half an hour'
date >> ~/timemanagement/timelog && echo Notified to update the events file for tomorrow >> ~/timemanagement/timelog 2>&1
vim ~/timemanagement/events.txt

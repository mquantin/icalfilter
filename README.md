# fork
this is a fork of (icalfilter)[https://github.com/klemensschindler/icalfilter] by klemensschindler 

# icalfilter
Filter out old ical events from a calendar.

The main use case for this script is to filter out old events from a cluttered, slow-performing calendar that contains years of events.

This script filters out events that are older than the specified trim date: year, month, day.
This includes recurrent events that have an *until* date earlier than that trim date. Events that have no *until* date or where the *until* date is not earlier than the specified year are preserved.

## Installation
Using your python 3 installation run:

```
pip install pytz icalendar
```

## Usage
* Make an export of your calendar in ICS format
* Save the ics file as `in.ics` in the folder of this script
* Set the `YEAR` `MONTH` `DAY` variable inside the script (events older than this year will be filtered out)
* Run `python icalfilter.py`, a filtered version of the calendar named `out.ics` is produced
* Clear out your original calendar (making a backup first is highly recommended)
* Re-import the filterd `out.ics` file.




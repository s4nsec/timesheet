#!/usr/bin/env python

from datetime import datetime
from datetime import timedelta
import time
import subprocess
import dateparser

# Get a datetime object with the start of the current work week.  day
# is a string specifying the name of the day.  time is the 24-hour
# time inside the starting day.
def get_week_start(day, start_time, week=datetime.today()):
  assert isinstance(week, datetime)
  weekday = time.strptime(day, '%A').tm_wday
  start_time = datetime.strptime(start_time, '%H:%M').time()
  start_day = week
  while start_day.weekday() != weekday:
    start_day = start_day - timedelta(days=1)
  return datetime(start_day.year, start_day.month, start_day.day, start_time.hour, start_time.minute, start_time.second)

# Get a datetime object with the start of the current day, i.e. 00:00.
def get_day_start(day=datetime.today()):
  assert isinstance(day, datetime)
  return datetime(day.year, day.month, day.day, 0, 0, 0)

# Converts string to formatted date by calling out to the unix date
# utility.  Returns None if conversion failed.
def interpretdate(string):
    return dateparser.parse(string)

def string2date(s):
  assert isinstance(s, str)
  return datetime.strptime(s, '%Y/%m/%d %H:%M:%S')

def date2string(date):
  assert isinstance(date, datetime)
  return date.strftime('%Y/%m/%d %H:%M:%S')

def delta2string(delta, show_days=False, decimal=False, abbr=False):
  assert isinstance(delta, timedelta)
  days = delta.days
  seconds = delta.seconds
  minutes = seconds / 60
  seconds = seconds % 60
  hours = minutes / 60
  minutes = minutes % 60
  if not show_days:
    hours += 24 * days
    days = 0
  pl = ''
  if days > 0:
    if not decimal:
      number_str = "%d:%02d:%02d:%02d" % (days, hours, minutes, seconds)
    else:
      number_str = '%.1f' % (days + float(hours) / 24)
    if abbr:
      units = ' d'
    else:
      if days > 1 or hours > 0 or minutes > 0 or seconds > 0:
        pl = 's'
      units = ' day' + pl
    return number_str + units
  elif hours > 0:
    if not decimal:
      number_str = "%d:%02d:%02d" % (hours, minutes, seconds)
    else:
      number_str = '%.1f' % (hours + float(minutes) / 60)
    if abbr:
      units = ' hr'
    else:
      if hours > 1 or minutes > 0 or seconds > 0:
        pl = 's'
      units = ' hour' + pl
    return number_str + units
  elif minutes > 0:
    if not decimal:
      number_str = "%d:%02d" % (minutes, seconds)
    else:
      number_str = "%.1f" % (minutes + float(seconds) / 60)
    if abbr:
      units = ' min'
    else:
      if minutes > 1 or seconds > 0:
        pl = 's'
      units = ' minute' + pl
    return number_str + units
  else:
    number_str = "%d" % (seconds)
    if abbr:
      units = ' sec'
    else:
      if not seconds == 1:
        pl = 's'
      units = ' second' + pl
    return number_str + units


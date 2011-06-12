#!/usr/bin/env python2.7
# This code is in the public domain; it can be used
# for any purpose with absolutely no restrictions

from datetime import datetime, timedelta
import sqlite3

REPORT_FILE = '/usr/local/www/nginx/turbine/stats.txt'

def get_current_data():
    """Return a tuple of the form

       (production, consumption)

       where production is the current output of the
       turbine and consumption is the current electrical
       use of Veale Center."""

    db = sqlite3.connect('journal.sqlite')
    cursor = db.cursor()

    cursor.execute("SELECT production, consumption FROM turbine_data "
        "ORDER BY timestamp DESC LIMIT 1")
    result = cursor.fetchone()
    db.close()
    return result

def get_daily_average_data():
    """Return a tuple of the form

       (production, consumption)

       where production is the average output of the
       turbine and consumption is the average electrical
       use of Veale Center, over the past 24 hours."""

    db = sqlite3.connect('journal.sqlite')
    cursor = db.cursor()

    end = datetime.now()
    start = end - timedelta(days=1)

    cursor.execute("SELECT AVG(production), AVG(consumption) FROM turbine_data "
        "WHERE timestamp > '%s' AND timestamp < '%s'" % (start, end))
    result = cursor.fetchone()
    db.close()
    return result

def write():
    """Write out the report data."""

    report_fd = open(REPORT_FILE, "w")
    db = sqlite3.connect('journal.sqlite')
    cursor = db.cursor()
    
    cursor.execute('SELECT MIN(timestamp), MAX(timestamp) FROM turbine_data')
    result = cursor.fetchone()
    report_fd.write("Reporting period: %s to %s\n" % (result[0], result[1]))

    current_data = get_current_data()
    report_fd.write("Current wind turbine production: %s kilowatts\n" % current_data[0])
    report_fd.write("Current Veale Center consumption: %s kilowatts\n" % current_data[1])

    average_data = get_daily_average_data()
    report_fd.write("24-hour average wind turbine production: %s kilowatts\n" % average_data[0])
    report_fd.write("24-hour average Veale Center consumption: %s kilowatts\n" % average_data[1])

    report_fd.close()
    db.close()

if __name__ == "__main__":
    write()

#!/usr/bin/env python2.7

# This code is in the public domain; it can be used
# for any purpose with absolutely no restrictions

import sqlite3
import turbine_data

def sync():
    """Get the latest batch of turbine data and write it
       to the database, ignoring any rows we already have"""

    db = sqlite3.connect('journal.sqlite')
    cursor = db.cursor()

    cursor.execute('SELECT timestamp FROM turbine_data ORDER BY timestamp DESC LIMIT 1')
    latest_row = cursor.fetchone()
    
    for row in turbine_data.retrieve_all_rows():
        values = {'timestamp': str(row[0]),
                  'production': row[1],
                  'consumption': row[2]}
        if latest_row is not None:
            if latest_row[0] >= str(row[0]):
                continue
        cursor.execute("INSERT INTO turbine_data ('timestamp', production, consumption) " + \
                       "VALUES (:timestamp, :production, :consumption)", values)
    db.commit()
    cursor.close()

if __name__ == "__main__":
    sync()

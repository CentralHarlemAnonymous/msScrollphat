#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal
import scrollphathd
import argparse
import time
import msClock
import msWeather
import sqlite3
import secrets
from sqlite3 import Error
from scrollphathd.fonts import font5x7

print("""
Scroll pHAT HD: msScrollphat

Press Ctrl+C to exit.
""")

parser = argparse.ArgumentParser(description='textclock code.')
parser.add_argument('-dt' ,'-delay_text', help="text delay time", default=0.025)
parser.add_argument('-dm' ,'-delay_message', help="message delay time", default=0.02)
parser.add_argument('-bd' ,'-brightnessDay', help="brightness in daytime", default=0.3)
parser.add_argument('-bn' ,'-brightnessNight', help="brightness at night", default=0.1)
parser.add_argument('-db' ,'-debug', help="debug by logging to file", default=0)

args = parser.parse_args()

# Uncomment the below if your display is upside down
#   (e.g. if you're using it in a Pimoroni Scroll Bot)
scrollphathd.rotate(degrees=180)

def brightness(sunrisetime, sunsettime):
    if isinstance(sunrisetime, int) and isinstance(sunsettime, int) and sunrisetime > 0 and sunsettime > 0:
        print('setting brightness. sunrisetime: ' + str(sunrisetime) + '. sunsettime: ' + str(sunsettime))
        timenow = time.time()
        morningTime = sunrisetime + 3600
        if timenow <= morningTime:
            brightNow = float(args.bn)
        elif morningTime < timenow <= sunsettime:
            brightNow = float(args.bd)
        elif timenow > sunsettime:
            brightNow = float(args.bn)
        else:
            brightNow = float(args.bn)
    else:
        # print('prob setting brightness. sunrisetime: '+ str(sunrisetime) + '. sunsettime: ' + str(sunsettime))
        brightNow = float(args.bn)
    return brightNow


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None


def run():
    # create a database connection
    database = "clockBase.db"
    conn = create_connection(database)
    cur = conn.cursor()
    sql = 'SELECT messageNo, text FROM messages WHERE displayedP = 0;'
    showit = True

    scrollphathd.clear()
    scrollphathd.show()
    counter = 1
    weatherD = msWeather.combinedReport()
    brightNow = brightness(weatherD['sunrise_time'], weatherD['sunset_time'])

    while True:
        # check db
        cur.execute("SELECT messageNo,text FROM messages WHERE displayedP = 0;")
        rows = cur.fetchall()

        # pick a message
        if counter < 3:
            text = msClock.paddedTime()
            counter = counter + 1
            showIt = True
#            counter = 7 # for debugging
        elif counter == 3:
            try:
               holderD = msWeather.combinedReport()
            except:
               print('no response from weather server. re-using data.')
               holderD = weatherD
            weatherD = holderD
            text = weatherD['status']
            brightNow = brightness(weatherD['sunrise_time'], weatherD['sunset_time'])
            counter = counter + 1
        elif 3 < counter <= 5:
            text = msClock.paddedTime()
            counter = counter + 1
        elif counter == 6:
            text = 'forecast: ' + weatherD['detailed_status']
            counter = counter + 1
        elif counter == 7:
            cur.execute(sql)
            rows = cur.fetchall()
            if len(rows) > 0:
                text = rows[0][1]
                cur.execute('''UPDATE messages SET displayTime = ?, displayedP = 1 WHERE messageNo = ?''',(time.time(),rows[0][0]))
                conn.commit()
                showIt = True
            else:
                text = ''
                showIt = False
            counter = 1

        if (showIt):
            text = "    " + text
        if int(args.db) == 1:
            debugText = text.encode('ascii', 'ignore').decode('ascii')
            print(text)
            with open("./debug.txt", "a") as debugFile:
                debugFile.write(debugText+'\n')
        if (showIt):
            textWidth=scrollphathd.write_string(text, x=0, y=0, font=font5x7, brightness=brightNow)
            scrollphathd.show()

            for deltaX in range(textWidth):
                 scrollphathd.scroll(x=1)
                 scrollphathd.show()
                 time.sleep(float(args.dt))
            scrollphathd.clear()
            scrollphathd.show()
            time.sleep(float(args.dm))

# Main function
if __name__ == "__main__":
    run_text = run()
    if (not run_text.process()):
        run_text.print_help()
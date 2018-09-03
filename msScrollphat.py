#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal
import scrollphathd
import argparse
import time
import msClock
import msWeather
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


args = parser.parse_args()


# Uncomment the below if your display is upside down
#   (e.g. if you're using it in a Pimoroni Scroll Bot)
scrollphathd.rotate(degrees=180)

def brightness(sunrisetime, sunsettime):
    timenow = time.time()
    morningTime = sunrisetime + 3600
    if timenow <= morningTime:
        brightNow = float(args.bn)
    elif morningTime < timenow <= sunsettime:
        brightNow = float(args.bd)
    elif timenow > sunsettime:
        brightNow = float(args.bn)
    else:
        brightNow = -1.0
    return brightNow

def run():
    scrollphathd.clear()
    scrollphathd.show()
    counter = 1
    weatherD = msWeather.currentReport()
    brightNow = brightness(weatherD['sunrise_time'], weatherD['sunset_time'])

    while True:
        if counter < 4:
            text = msClock.paddedTime()
            counter = counter + 1
        elif counter == 4:
            weatherD = msWeather.currentReport()
            text = weatherD['status']
            brightNow = brightness(weatherD['sunrise_time'], weatherD['sunset_time'])
            counter = 1
        text = "    " + text
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

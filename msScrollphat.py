#!/usr/bin/env python

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
parser.add_argument('-dm' ,'-delay_message', help="message delay time", default=0.2)
parser.add_argument('-b' ,'-brightness', help="brightness", default=0.15)


args = parser.parse_args()


# Uncomment the below if your display is upside down
#   (e.g. if you're using it in a Pimoroni Scroll Bot)
scrollphathd.rotate(degrees=180)

def run():
    scrollphathd.clear()
    scrollphathd.show()
    counter = 1

    while True:
        if counter < 4:
            text = msClock.paddedTime()
            counter = counter + 1
        elif counter == 4:
            text = msWeather.currentReport()
            counter = 1
        text = "    " + text
        textWidth=scrollphathd.write_string(text, x=0, y=0, font=font5x7, brightness=float(args.b))
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

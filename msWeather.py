#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyowm
import json

owm = pyowm.OWM('8473ffbb38cc053f91ecb29ae8ff9bf5')  # You MUST provide a valid API key

def forecasts(num):
    forecaster = owm.three_hours_forecast('Dobbs Ferry, US')
    forecast = forecaster.get_forecast()
    forecastJSON=json.loads(forecast.to_JSON())
    nForecasts = forecastJSON['weathers'][:num]
    return nForecasts

def currentWeather():
    currentObs = owm.weather_at_place('Dobbs Ferry, US')
    currentW = currentObs.get_weather()
    return currentW

def currentReport():
    currentW = currentWeather()
    currentJSON = json.loads(currentW.to_JSON())
    status = currentJSON['detailed_status']
    tempA = currentW.get_temperature('fahrenheit')
    tempS = str(round(tempA['temp'],1)) + u'°F'
    ans = status + "  " + tempS
    return {u'sunrise_time': currentJSON[u'sunrise_time'], u'sunset_time': currentJSON[u'sunset_time'], 'status': ans}

def oneForecast():
    mrForecast = forecasts(1)
    return mrForecast[0]['detailed_status']

def printForecast():
    print oneForecast()

if __name__ == "__main__":
#    printForecast()
    print currentReport()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pyowm
import json
import datetime
import secrets
from pyowm.exceptions.api_call_error import APICallError # is this really needed?

owm = pyowm.OWM(secrets.OWMAPIKEY)  # You MUST provide a valid API key

def forecasts(num):
    forecaster = owm.three_hours_forecast('Dobbs Ferry, US')
    forecast = forecaster.get_forecast()
    forecastJSON=json.loads(forecast.to_JSON())
    nForecasts = forecastJSON['weathers'][:num]
    return nForecasts

def currentWeather():
    try:
        currentObs = owm.weather_at_place('Dobbs Ferry, US')
        currentW = currentObs.get_weather()
    except (APICallError, TypeError):
        try:
            text=str(currentW)
            debugText = text.encode('ascii', 'ignore').decode('ascii')
        except:
            debugText = 'failed to get weather_at_place from OpenWeatherMap'
        with open("./debug.txt", "a") as debugFile:
            debugText = str(datetime.datetime.now())+': '+debugText+'\n'
            debugFile.write(debugText)
        currentW = 'error'
    return currentW

def currentReport():
    currentW = currentWeather()
    tempS = ''
    if currentW != 'error':
        try:
            currentJSON = json.loads(currentW.to_JSON())
            status = currentJSON['detailed_status']
            tempA = currentW.get_temperature('fahrenheit')
            if isinstance(tempA['temp'], float):
                tempS = str(round(tempA['temp'],1)) + u'°F'
        except:
            status = 'error extracting weather components'
    else:
        status = 'error fetching weather'

    ans = status + '  ' + tempS
    return {u'status': ans}


def combinedReport():
    currentD = currentReport()
    forecastD = forecasts(1)[0]
    forecastD.update(currentD)
    return forecastD


def oneForecast():
    mrForecast = forecasts(1)
    return mrForecast[0]['detailed_status']

if __name__ == "__main__":
#    print oneForecast()
#    print currentReport()
    print combinedReport()

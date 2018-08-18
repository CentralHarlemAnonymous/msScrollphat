#!/usr/bin/env python
import pyowm
import json

owm = pyowm.OWM('8473ffbb38cc053f91ecb29ae8ff9bf5')  # You MUST provide a valid API key

def forecasts(num):
    forecaster = owm.three_hours_forecast('Dobbs Ferry, US')
    forecast = forecaster.get_forecast()
    forecastJSON=json.loads(forecast.to_JSON())

    nForecasts = forecastJSON['weathers'][:num]
    return nForecasts

def oneForecast():
    mrForecast = forecasts(1)
    return mrForecast[0]['detailed_status']

def printForecast():
    print oneForecast()

if __name__ == "__main__":
    printForecast()

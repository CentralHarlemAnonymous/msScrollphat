#!/usr/bin/env python
import pyowm
import json

owm = pyowm.OWM('8473ffbb38cc053f91ecb29ae8ff9bf5')  # You MUST provide a valid API key
# https://pyowm.readthedocs.io/en/latest/

forecaster = owm.three_hours_forecast('Dobbs Ferry, US')
forecast = forecaster.get_forecast()
weather_list = forecast.get_weathers()
forecastJSON=json.loads(forecast.to_JSON())

# for key in forecastJSON.keys():
#    print key

def forecasts(num):
    outL = []
    nForecasts = forecastJSON['weathers'][:num]
    # for forecastDict in fourForecasts:
    #     print forecastDict['detailed_status']
    for n in nForecasts:
       outL.append(n['detailed_status'])
    return ''.join(outL)

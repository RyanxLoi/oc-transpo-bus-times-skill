from mycroft import MycroftSkill, intent_file_handler

import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime, timedelta

load_dotenv()

class OcTranspoBusTimes(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('ask.for.stop.no.intent')
    def handle_times_bus_transpo_oc(self, message):
        
        stopNumber = self.get_response('ask.for.stop.no')
        url = 'https://api.octranspo1.com/v2.0/GetNextTripsForStop?appID=' + self.settings.get('AppID') + '&apiKey=' + self.settings.get('APIKey') + '&stopNo=' + stopNumber
        response = requests.get(url).json()
        self.speak_dialog('Here are the bus arrival times for stop number ' + stopNumber)
        

        for i in range(0,(len(response.get('GetNextTripsForStopResult'))-2)):
            routeNo = response.get('GetNextTripsForStopResult').get('Route').get('RouteDirection')[i].get('RouteNo')
            routeLabel = response.get('GetNextTripsForStopResult').get('Route').get('RouteDirection')[i].get('RouteLabel')
            self.speak_dialog('The ' + routeNo + " " + routeLabel + " comes in approximately ")
            for j in range(0,len(response.get('GetNextTripsForStopResult').get('Route').get('RouteDirection')[i].get('Trips').get('Trip'))):
                estMinutes = response.get('GetNextTripsForStopResult').get('Route').get('RouteDirection')[i].get('Trips').get('Trip')[j].get('AdjustedScheduleTime')
                hours = 0
                if int(estMinutes) > 60:
                    hours = int(estMinutes) // 60
                    minutes = int(estMinutes) - (60 * hours)
                estTimeArrival = datetime.now() + timedelta(minutes=int(estMinutes))
                if hours == 1:
                    if minutes == 1:
                        self.speak_dialog(str(hours) + " hour and " + str(minutes) + " minute at " + estTimeArrival.strftime("%H:%M"))
                    else:
                        self.speak_dialog(str(hours) + " hour and " + str(minutes) + " minutes at " + estTimeArrival.strftime("%H:%M"))
                elif hours > 1:
                    if minutes == 1:
                        self.speak_dialog(str(hours) + " hours and " + str(minutes) + " minute at " + estTimeArrival.strftime("%H:%M"))
                    else:
                        self.speak_dialog(str(hours) + " hours and " + str(minutes) + " minutes at " + estTimeArrival.strftime("%H:%M"))
                else:
                    self.speak_dialog(estMinutes + " minutes at " + estTimeArrival.strftime("%H:%M"))

def create_skill():
    return OcTranspoBusTimes()


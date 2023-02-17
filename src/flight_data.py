import json
import os


class FlightData:
    '''
    This class loads the flight data
    '''

    def __init__(self):
        self.cruise_conditions = json.load(open(os.path.abspath('flights/cruiseConditions.json'), 'r'))
        self.stability_der = json.load(open(os.path.abspath('flights/longitudinalSD.json'), 'r'))
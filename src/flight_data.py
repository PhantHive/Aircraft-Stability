import json


class FlightData:
    '''
    This class loads the flight data
    '''

    def __init__(self):
        self.cruise_conditions = json.load(open('../flights/cruiseConditions.json', 'r'))
        self.stability_der = json.load(open('../flights/stabilityDerivatives.json', 'r'))
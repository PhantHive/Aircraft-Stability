import json
import os


class FlightData:
    '''
    This class loads the flight data
    '''

    def __init__(self, user_file=None):
        if user_file is None:
            print("No user file provided, using default files")
            user_file = [os.path.abspath('calculation/flights/longitudinalSD.json'), os.path.abspath('calculation/flights/steadyConditions.json')]

        self.stability_der = json.load(open(user_file[0], 'r'))
        self.cruise_conditions = json.load(open(user_file[1], 'r'))

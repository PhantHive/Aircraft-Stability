import json
import os


class FlightData:
    '''
    This class loads the flight data
    '''

    def __init__(self, axis="longitudinal", user_file=None):
        print(axis)
        if user_file is None:
            print("No user file provided, using default files")
            if axis == "longitudinal":
                user_file = [os.path.abspath('calculation/flights/longitudinal/longitudinalSD.json'), os.path.abspath('calculation/flights/longitudinal/steadyConditions.json')]
            elif axis == "lateral":
                user_file = [os.path.abspath('calculation/flights/lateral/lateralSD.json'), os.path.abspath('calculation/flights/lateral/steadyConditions.json')]
            self.stability_der = json.load(open(user_file[0], 'r'))
            self.cruise_conditions = json.load(open(user_file[1], 'r'))

        else:
            self.stability_der = json.loads(user_file[0])
            self.cruise_conditions = json.loads(user_file[1])

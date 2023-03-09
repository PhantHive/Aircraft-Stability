import numpy as np
from data.flight_data import FlightData


class LatControlMatrix(FlightData):
    '''
    This class calculates the control matrix for the elevator and throttle control
    '''

    def __init__(self, user_file=None):
        # get the flight data
        FlightData.__init__(self, "lateral", user_file=user_file)
        self.control_matrix = None
        self.Y_delta_r = 0
        self.L_delta_r = 0
        self.N_delta_r = 0
        self.Y_delta_a = 0
        self.L_delta_a = 0
        self.N_delta_a = 0

        if self.cruise_conditions["q_mean"]["value"] == -1111:
            self.q_mean = (self.cruise_conditions["rho"]["value"] *
                           self.cruise_conditions["V"]["value"] ** 2) / 2
        else:
            self.q_mean = self.cruise_conditions["q_mean"]["value"]
        

    def calculate_Y_delta_r(self, wing_area):

        first_part = self.q_mean * wing_area / \
                     (self.cruise_conditions["m"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = self.stability_der["C_Y_delta_r"]["value"]
        self.Y_delta_r = first_part * second_part

    def calculate_L_delta_r(self, wing_area, wing_span):
        first_part = self.q_mean * wing_area * wing_span / \
                     (self.cruise_conditions["Ixx"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = self.stability_der["C_L_delta_r"]["value"]
        self.L_delta_r = first_part * second_part


    def calculate_N_delta_r(self, wing_area, wing_span):
        first_part = self.q_mean * wing_area * wing_span / \
                     (self.cruise_conditions["Izz"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = self.stability_der["C_N_delta_r"]["value"]
        self.N_delta_r = first_part * second_part

    def calculate_Y_delta_a(self, wing_area):
        first_part = self.q_mean * wing_area / \
                     (self.cruise_conditions["m"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = self.stability_der["C_Y_delta_a"]["value"]
        self.Y_delta_a = first_part * second_part

    def calculate_L_delta_a(self, wing_area, wing_span):
        first_part = self.q_mean * wing_area * wing_span / \
                     (self.cruise_conditions["Ixx"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = self.stability_der["C_L_delta_a"]["value"]
        self.L_delta_a = first_part * second_part

    def calculate_N_delta_a(self, wing_area, wing_span):
        first_part = self.q_mean * wing_area * wing_span / \
                     (self.cruise_conditions["Izz"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = self.stability_der["C_N_delta_a"]["value"]
        self.N_delta_a = first_part * second_part


    def show_control_matrix(self):
        return self.control_matrix

    def set_lat_stability_control_matrix(self):

        # set the elevator vector
        self.control_matrix = np.array(
            [
                [
                    self.Y_delta_r,
                    self.Y_delta_a
                ],
                [
                    self.L_delta_r,
                    self.L_delta_a
                ],
                [
                    self.N_delta_r,
                    self.N_delta_a
                ],
                [
                    0,
                    0
                ]
            ])






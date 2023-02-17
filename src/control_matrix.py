import numpy as np
from src.flight_data import FlightData


class ControlMatrix(FlightData):
    '''
    This class calculates the control matrix for the elevator and throttle control
    '''

    def __init__(self):
        # get the flight data
        super().__init__()
        self.X_delta_e = 0
        self.Z_delta_e = 0
        self.M_delta_e = 0
        self.X_delta_T = 0

        self.elevator_vector = None

    def calculate_X_delta_e(self, wing_area):

        first_part = self.cruise_conditions["q_mean"]["value"] * wing_area / \
                     self.cruise_conditions["m"]["value"] * self.cruise_conditions["V"]["value"]
        second_part = self.stability_der["C_D_d_E"]["value"]
        self.X_delta_e = first_part * second_part

    def calculate_Z_delta_e(self, wing_area):
        first_part = self.cruise_conditions["q_mean"]["value"] * wing_area / \
                     self.cruise_conditions["m"]["value"] * self.cruise_conditions["V"]["value"]
        second_part = self.stability_der["C_L_d_E"]["value"]
        self.Z_delta_e = first_part * second_part


    def calculate_M_delta_e(self, wing_mean_chord, wing_area):
        first_part = self.cruise_conditions["q_mean"]["value"] * wing_area * wing_mean_chord / \
                     self.cruise_conditions["Iyy"]["value"] * self.cruise_conditions["V"]["value"]
        second_part = self.stability_der["C_m_d_E"]["value"]
        self.M_delta_e = first_part * second_part

    def calculate_X_delta_T(self, wing_area):
        first_part = self.cruise_conditions["q_mean"]["value"] * wing_area / \
                     self.cruise_conditions["m"]["value"] * self.cruise_conditions["V"]["value"]
        second_part = self.stability_der["C_D_d_T"]["value"]
        self.X_delta_T = first_part * second_part


    def get_elevator_derivatives(self):
        return self.elevator_vector

    def set_long_stability_control_matrix(self, Mw_dot):

        # set the elevator vector
        self.elevator_vector = np.array(
            [
                self.X_delta_e,
                self.Z_delta_e,
                self.M_delta_e + self.Z_delta_e * Mw_dot
            ])




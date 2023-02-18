import numpy as np
from calculation.src.flight_data import FlightData


class AircraftMatrix(FlightData):
    '''
    This class calculates the aircraft matrix
    '''

    def __init__(self):
        '''
        :param cruise_condition: json file with the cruise condition
        :param stability_der: json file with the longitudinal stability derivatives
        :param X: longitudinal stability derivative vector (Xu, Xw, Xw_dot, Xq)
        :param Z: lateral stability derivative vector (Zu, Zw, Zw_dot, Zq)
        :param M: rolling moment derivative vector (Mu, Mw, Mw_dot, Mq)
        '''

        super().__init__()

        self.Yv = 0
        self.Yp = 0
        self.Yr = 0

        self.Lv = 0
        self.Lp = 0
        self.Lr = 0

        self.Nv = 0
        self.Np = 0
        self.Nr = 0

    def calculate_Yv(self, wing_area):
        first_part = (self.cruise_conditions["q_mean"]["value"] * wing_area) / (
                self.cruise_conditions["m"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = (self.stability_der["C_Y_beta"]["value"])
        self.Yv = first_part * second_part

    def calculate_Yp(self, wing_area):
        first_part = (self.cruise_conditions["q_mean"]["value"] * wing_area) / (
                2 * self.cruise_conditions["m"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = (self.stability_der["C_Y_p"]["value"])
        self.Yp = first_part * second_part

    def calculate_Yr(self, wing_area):
        first_part = (self.cruise_conditions["q_mean"]["value"] * wing_area) / (
                2 * self.cruise_conditions["m"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = (self.stability_der["C_Y_r"]["value"])
        self.Yr = first_part * second_part

    def calculate_Lv(self, wing_area, wing_span):
        first_part = (self.cruise_conditions["q_mean"]["value"] * wing_area * wing_span) / (
                2 * self.cruise_conditions["Ixx"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = (self.stability_der["C_L_beta"]["value"])
        self.Lv = first_part * second_part

    def calculate_Lp(self, wing_area, wing_span):
        first_part = (self.cruise_conditions["q_mean"]["value"] * wing_area * wing_span**2) / (
                2 * self.cruise_conditions["Ixx"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = (self.stability_der["C_L_p"]["value"])
        self.Lp = first_part * second_part

    def calculate_Lr(self, wing_area, wing_span):
        first_part = (self.cruise_conditions["q_mean"]["value"] * wing_area * wing_span**2) / (
                2 * self.cruise_conditions["Ixx"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = (self.stability_der["C_L_r"]["value"])
        self.Lr = first_part * second_part

    def calculate_Nv(self, wing_area, wing_span):
        first_part = (self.cruise_conditions["q_mean"]["value"] * wing_area * wing_span) / (
                    self.cruise_conditions["Izz"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = (self.stability_der["C_N_beta"]["value"])
        self.Nv = first_part * second_part

    def calculate_Np(self, wing_area, wing_span):
        first_part = (self.cruise_conditions["q_mean"]["value"] * wing_area * wing_span**2) / (
                2 * self.cruise_conditions["Izz"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = (self.stability_der["C_N_p"]["value"])
        self.Np = first_part * second_part

    def calculate_Nr(self, wing_area, wing_span):
        first_part = (self.cruise_conditions["q_mean"]["value"] * wing_area * wing_span**2) / (
                2 * self.cruise_conditions["Izz"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = (self.stability_der["C_N_r"]["value"])
        self.Nr = first_part * second_part



    def set_long_stability_aircraft_matrix(self):
        '''
        :return: np array of the aircraft matrix
        3 columns, 4 rows:
        columns: X, Z, M
        rows: u, w, w_dot, q
        '''
        self.aircraft_matrix = np.array(
            [
                [self.Yv, self.Yp, -(self.cruise_conditions["V"]["value"] - self.Yr), self.cruise_conditions["g"]["value"]*np.cos(self.cruise_conditions["theta"]["value"])],
                [self.Lv, self.Lp, self.Lr, 0],
                [self.Nv, self.Np, self.Nr, 0],
                [0, 1, 0, 0]
            ])

        # without scientific notation
        np.set_printoptions(suppress=True)
        self.aircraft_matrix[self.aircraft_matrix == -0.0] = 0.0

    def get_aircraft_matrix(self):
        return self.aircraft_matrix

    def get_param(self, name):

        if hasattr(self, name):
            return getattr(self, name)
        else:
            print("Parameter does not exist")


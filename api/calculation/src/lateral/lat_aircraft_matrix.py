import numpy as np
from data.flight_data import FlightData


class LatAircraftMatrix(FlightData):
    '''
    This class calculates the aircraft matrix
    '''

    def __init__(self, user_file=None):
        '''
        :param cruise_condition: json file with the cruise condition
        :param stability_der: json file with the longitudinal stability derivatives
        :param X: longitudinal stability derivative vector (Xu, Xw, Xw_dot, Xq)
        :param Z: lateral stability derivative vector (Zu, Zw, Zw_dot, Zq)
        :param M: rolling moment derivative vector (Mu, Mw, Mw_dot, Mq)
        '''

        FlightData.__init__(self, "lateral", user_file)

        self.damping_ratio = None
        self.natural_frequency = None
        self.characteristic_equation = None
        self.eigenvectors = None
        self.eigenvalues = None
        self.aircraft_matrix = None
        self.Yv = 0
        self.Yp = 0
        self.Yr = 0

        self.Lv = 0
        self.Lp = 0
        self.Lr = 0

        self.Nv = 0
        self.Np = 0
        self.Nr = 0

        if self.cruise_conditions["q_mean"]["value"] == -1111:
            self.q_mean = (self.cruise_conditions["rho"]["value"] *
                           self.cruise_conditions["V"]["value"] ** 2) / 2
        else:
            self.q_mean = self.cruise_conditions["q_mean"]["value"]

    def calculate_Yv(self, wing_area):
        first_part = (self.q_mean * wing_area) / (
                self.cruise_conditions["m"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = (self.stability_der["C_Y_beta"]["value"])
        self.Yv = first_part * second_part

    def calculate_Yp(self, wing_area, wing_span):
        first_part = (self.q_mean * wing_area * wing_span) / (
                2 * self.cruise_conditions["m"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = (self.stability_der["C_Y_p"]["value"])
        self.Yp = first_part * second_part

    def calculate_Yr(self, wing_area, wing_span):
        first_part = (self.q_mean * wing_area * wing_span) / (
                2 * self.cruise_conditions["m"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = (self.stability_der["C_Y_r"]["value"])
        self.Yr = first_part * second_part

    def calculate_Lv(self, wing_area, wing_span):
        first_part = (self.q_mean * wing_area * wing_span) / (
                self.cruise_conditions["Ixx"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = (self.stability_der["C_L_beta"]["value"])
        self.Lv = first_part * second_part

    def calculate_Lp(self, wing_area, wing_span):
        first_part = (self.q_mean * wing_area * wing_span**2) / (
                2 * self.cruise_conditions["Ixx"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = (self.stability_der["C_L_p"]["value"])
        self.Lp = first_part * second_part

    def calculate_Lr(self, wing_area, wing_span):
        first_part = (self.q_mean * wing_area * wing_span**2) / (
                2 * self.cruise_conditions["Ixx"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = (self.stability_der["C_L_r"]["value"])
        self.Lr = first_part * second_part

    def calculate_Nv(self, wing_area, wing_span):
        first_part = (self.q_mean * wing_area * wing_span) / (
                    self.cruise_conditions["Izz"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = (self.stability_der["C_N_beta"]["value"])
        self.Nv = first_part * second_part

    def calculate_Np(self, wing_area, wing_span):
        first_part = (self.q_mean * wing_area * wing_span**2) / (
                2 * self.cruise_conditions["Izz"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = (self.stability_der["C_N_p"]["value"])
        self.Np = first_part * second_part

    def calculate_Nr(self, wing_area, wing_span):
        first_part = (self.q_mean * wing_area * wing_span**2) / (
                2 * self.cruise_conditions["Izz"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = (self.stability_der["C_N_r"]["value"])
        self.Nr = first_part * second_part



    def set_lat_stability_aircraft_matrix(self):
        '''
        :return: np array of the aircraft matrix
        3 columns, 4 rows:
        columns: X, Z, M
        rows: u, w, w_dot, q
        '''
        self.aircraft_matrix = np.array(
            [
                [self.Yv, self.Yp, -(self.cruise_conditions["V"]["value"] - self.Yr),self.cruise_conditions["g"]["value"]*np.cos((np.pi * self.cruise_conditions["theta"]["value"] / 180))],
                [self.Lv, self.Lp, self.Lr, 0],
                [self.Nv, self.Np, self.Nr, 0],
                [0, 1, 0, 0]
            ])

        # without scientific notation
        np.set_printoptions(suppress=True)
        self.aircraft_matrix[self.aircraft_matrix == -0.0] = 0.0
        
    def set_eigenvalues(self):
        self.eigenvalues = np.linalg.eigvals(self.aircraft_matrix)
        
    def set_eigenvectors(self):
        self.eigenvectors = np.linalg.eig(self.aircraft_matrix)[1]
        
    def set_characteristic_equation(self):
        self.characteristic_equation = np.polynomial.polynomial.polyfromroots(self.eigenvalues)
        
    def set_natural_frequency(self):
        # find natural frequency from eigenvalues there should be 2 frequency one for short period mode and one for phugoid
        # mode
        real_parts = np.real(self.eigenvalues)
        imag_parts = np.imag(self.eigenvalues)

        # Sort eigenvalues in ascending order of real parts
        idx = real_parts.argsort()
        real_parts = real_parts[idx]
        imag_parts = imag_parts[idx]

        # Calculate natural frequencies
        omega_sp = np.sqrt(real_parts[0] ** 2 + imag_parts[0] ** 2)
        omega_p = np.sqrt(real_parts[-1] ** 2 + imag_parts[-1] ** 2)

        self.natural_frequency = np.array([omega_sp, omega_p])

    def set_damping_ratio(self):
        damping_ratio_sp = -np.real(self.eigenvalues[0]) / np.abs(self.eigenvalues[0])
        damping_ratio_p = -np.real(self.eigenvalues[-1]) / np.abs(self.eigenvalues[-1])
        self.damping_ratio = np.array([damping_ratio_sp, damping_ratio_p])

    def get_lat_aircraft_matrix(self):
        return self.aircraft_matrix

    def get_param(self, name):

        if hasattr(self, name):
            return getattr(self, name)
        else:
            print("Parameter does not exist")


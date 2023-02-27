from data.flight_data import FlightData
import numpy as np
import sys

from matplotlib import pyplot as plt

sys.path.append("data/")


class AircraftMatrix(FlightData):
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

        FlightData.__init__(self, user_file=user_file)

        self.damping_ratio = None
        self.natural_frequency = None
        self.eigenvectors = None
        self.eigenvalues = None
        self.characteristic_equation = None

        self.Xu = 0
        self.Xw = 0

        self.Zu = 0
        self.Zw = 0
        self.Zw_dot = 0
        self.Zq = 0

        self.Mu = 0
        self.Mq = 0
        self.Mw = 0
        self.Mw_dot = 0

    def calculate_Xu(self, S):
        first_part = (self.cruise_conditions["q_mean"]["value"] * S) / (
            self.cruise_conditions["m"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = (
            2 * self.cruise_conditions["C_D_0"]["value"] + self.stability_der["C_D_u"]["value"])
        self.Xu = -first_part * second_part

    def calculate_Xw(self, aspect_ratio, oswald, S):
        first_part = (self.cruise_conditions["q_mean"]["value"] * S) / (
            self.cruise_conditions["m"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = (self.cruise_conditions["C_L_0"]["value"] * (
            1 - (2 / (np.pi * aspect_ratio * oswald)) * self.stability_der["C_L_alpha"]["value"]))
        self.Xw = first_part * second_part

    def calculate_Zu(self, S):
        first_part = (self.cruise_conditions["q_mean"]["value"] * S) / (
            self.cruise_conditions["m"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = (
            2 * self.cruise_conditions["C_L_0"]["value"] + self.stability_der["C_L_u"]["value"])
        self.Zu = -first_part * second_part

    def calculate_Zw(self, S):
        first_part = (self.cruise_conditions["q_mean"]["value"] * S) / (
            self.cruise_conditions["m"]["value"] * self.cruise_conditions["V"]["value"])
        second_part = (
            self.cruise_conditions["C_D_0"]["value"] + self.stability_der["C_L_alpha"]["value"])
        self.Zw = - first_part * second_part

    def calculate_Zw_dot(self, wing_mean_chord, S):
        first_part = (self.cruise_conditions["q_mean"]["value"] * S * wing_mean_chord) / \
                     (2 * self.cruise_conditions["m"]["value"] *
                      np.power(self.cruise_conditions["V"]["value"], 2))
        second_part = (
            self.cruise_conditions["C_D_0"]["value"] * self.stability_der["C_L_alpha_dot"]["value"])
        self.Zw_dot = first_part * second_part

    def calculate_Zq(self, wing_mean_chord, S):
        first_part = (self.cruise_conditions["q_mean"]["value"] * S * wing_mean_chord) / \
                     (2 * self.cruise_conditions["m"]["value"] *
                      np.power(self.cruise_conditions["V"]["value"], 2))
        second_part = self.stability_der["C_L_q"]["value"]
        self.Zq = first_part * second_part

    def calculate_Mu(self, wing_mean_chord, S):
        first_part = (self.cruise_conditions["q_mean"]["value"] * S * wing_mean_chord) / \
                     (self.cruise_conditions["Iyy"]["value"]
                      * self.cruise_conditions["V"]["value"])
        second_part = self.stability_der["C_m_u"]["value"]
        self.Mu = first_part * second_part

    def calculate_Mw(self, wing_mean_chord, S):
        first_part = (self.cruise_conditions["q_mean"]["value"] * S * wing_mean_chord) / \
                     (self.cruise_conditions["Iyy"]["value"]
                      * self.cruise_conditions["V"]["value"])
        second_part = self.stability_der["C_m_alpha"]["value"]
        self.Mw = first_part * second_part

    def calculate_Mw_dot(self, wing_mean_chord, S):
        first_part = (self.cruise_conditions["q_mean"]["value"] * S * np.power(wing_mean_chord, 2)) / \
                     (2 * self.cruise_conditions["Iyy"]["value"] *
                      np.power(self.cruise_conditions["V"]["value"], 2))
        second_part = self.stability_der["C_m_alpha_dot"]["value"]
        self.Mw_dot = first_part * second_part

    def calculate_Mq(self, wing_mean_chord, S):
        first_part = (self.cruise_conditions["q_mean"]["value"] * S * np.power(wing_mean_chord, 2)) / \
                     (2 * self.cruise_conditions["Iyy"]["value"]
                      * self.cruise_conditions["V"]["value"])
        second_part = self.stability_der["C_m_q"]["value"]
        self.Mq = first_part * second_part

    def calculate_X_delta_e(self, S):
        first_part = (self.cruise_conditions["q_mean"]["value"] * S) / \
                     (self.cruise_conditions["m"]["value"]
                      * self.cruise_conditions["V"]["value"])
        second_part = self.stability_der["C_D_d_E"]["value"]
        self.X_gamma_e = first_part * second_part

    def calculate_Z_delta_e(self, S):
        first_part = (self.cruise_conditions["q_mean"]["value"] * S) / \
                     (self.cruise_conditions["m"]["value"]
                      * self.cruise_conditions["V"]["value"])
        second_part = self.stability_der["C_L_d_E"]["value"]
        self.Z_gamma_e = first_part * second_part

    def calculate_M_delta_e(self, wing_mean_chord, S):
        first_part = (self.cruise_conditions["q_mean"]["value"] * S * wing_mean_chord) / \
                     (self.cruise_conditions["Iyy"]["value"]
                      * self.cruise_conditions["V"]["value"])
        second_part = self.stability_der["C_m_d_E"]["value"]
        self.M_gamma_e = first_part * second_part

    def set_long_stability_aircraft_matrix(self):
        '''
        :return: np array of the aircraft matrix
        3 columns, 4 rows:
        columns: X, Z, M
        rows: u, w, w_dot, q
        '''
        self.aircraft_matrix = np.array(
            [
                [self.Xu, self.Xw, 0,
                 -self.cruise_conditions["g"]["value"] * np.cos(self.cruise_conditions["theta"]["value"])],
                [self.Zu, self.Zw, self.cruise_conditions["V"]["value"],
                 -self.cruise_conditions["g"]["value"] * np.sin(self.cruise_conditions["theta"]["value"])],
                [self.Mu + self.Zu * self.Mw_dot, self.Mw + self.Zw * self.Mw_dot,
                 self.Mq + self.cruise_conditions["V"]["value"] * self.Mw_dot, 0],
                [0, 0, 1, 0]
            ])

        # without scientific notation
        np.set_printoptions(suppress=True)
        self.aircraft_matrix[self.aircraft_matrix == -0.0] = 0.0

    def set_eigenvalues(self):
        self.eigenvalues = np.linalg.eigvals(self.aircraft_matrix)

    def set_eigenvectors(self):
        self.eigenvectors = np.linalg.eig(self.aircraft_matrix)[1]

    def set_characteristic_equation(self):
        self.characteristic_equation = np.polynomial.polynomial.polyfromroots(
            self.eigenvalues)

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
        damping_ratio_sp = - \
            np.real(self.eigenvalues[0]) / np.abs(self.eigenvalues[0])
        damping_ratio_p = - \
            np.real(self.eigenvalues[-1]) / np.abs(self.eigenvalues[-1])
        self.damping_ratio = np.array([damping_ratio_sp, damping_ratio_p])

    def get_aircraft_matrix(self):
        return self.aircraft_matrix

    def get_characteristic_equation(self):
        return self.characteristic_equation

    def get_eigenvalues(self):
        return self.eigenvalues

    def get_eigenvectors(self):
        return self.eigenvectors

    def get_natural_frequency(self):
        return self.natural_frequency

    def get_damping_ratio(self):
        return self.damping_ratio

    def get_param(self, name):

        if hasattr(self, name):
            return getattr(self, name)
        else:
            print("Parameter does not exist")

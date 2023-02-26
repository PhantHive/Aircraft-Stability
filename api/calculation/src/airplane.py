import sys
sys.path.append("calculation/src")

from longitudinal.lon_aircraft_matrix import AircraftMatrix
from longitudinal.lon_control_matrix import ControlMatrix
from longitudinal.lon_plot_stability import PlotLongitudinalModes


class Airplane(AircraftMatrix, ControlMatrix):
    '''
    This class is used to calculate the aircraft matrix and the control matrix
    It is also used to get the cruise conditions
    '''

    def __init__(self, name, wing_area, aspect_ratio, taper_ratio, wingspan, wing_mean_chord, wing_oswald, user_file=None):
        super().__init__(user_file=user_file)
        self.name = name
        self.wing_area = wing_area  # S
        self.aspect_ratio = aspect_ratio  # A
        self.taper_ratio = taper_ratio  # lambda
        self.wingspan = wingspan  # b
        self.wing_mean_chord = wing_mean_chord  # c
        self.wing_oswald = wing_oswald  # e
        self.user_file = user_file

    def get_longitudinal_aicraft_matrix(self):
        # ----------------- Calculate the aircraft matrix for longitudinal stability ----------------- #
        # Calculate X matrix coefficients (Xu, Xw)
        AircraftMatrix.calculate_Xu(self, self.wing_area)
        AircraftMatrix.calculate_Xw(self, self.aspect_ratio, self.wing_oswald, self.wing_area)

        # Calculate Z matrix coefficients (Zu, Zw, Zw_dot, Zq)
        AircraftMatrix.calculate_Zu(self, self.wing_area)
        AircraftMatrix.calculate_Zw(self, self.wing_area)
        AircraftMatrix.calculate_Zw_dot(self, self.wing_mean_chord, self.wing_area)
        AircraftMatrix.calculate_Zq(self, self.wing_mean_chord, self.wing_area)

        # Calculate M matrix coefficients (Mu, Mw, Mw_dot, Mq)
        AircraftMatrix.calculate_Mu(self, self.wing_mean_chord, self.wing_area)
        AircraftMatrix.calculate_Mw(self, self.wing_mean_chord, self.wing_area)
        AircraftMatrix.calculate_Mw_dot(self, self.wing_mean_chord, self.wing_area)
        AircraftMatrix.calculate_Mq(self, self.wing_mean_chord, self.wing_area)

        # Get aircraft matrix for longitudinal stability
        AircraftMatrix.set_long_stability_aircraft_matrix(self)
        # ------------------------------------------------------------------------------------------ #

    def get_longitudinal_control_matrix(self):
        # ----------------- Calculate the control matrix for longitudinal stability ----------------- #
        # Calculate X_delta_e
        ControlMatrix.calculate_X_delta_e(self, self.wing_area)

        # Calculate Z_delta_e
        ControlMatrix.calculate_Z_delta_e(self, self.wing_area)

        # Calculate M_delta_e
        ControlMatrix.calculate_M_delta_e(self, self.wing_area, self.wing_mean_chord)

        ControlMatrix.calculate_X_delta_T(self, self.wing_area)

        ControlMatrix.calculate_Z_delta_T(self, self.wing_area)

        ControlMatrix.calculate_M_delta_T(self, self.wing_area, self.wing_mean_chord)

        # Get control matrix
        ControlMatrix.set_long_stability_control_matrix(self, self.Mw_dot)
        # ------------------------------------------------------------------------------------------ #

    def get_cruise_condition(self, coeff):
        return f"{self.cruise_conditions[coeff]['value']} {self.cruise_conditions[coeff]['unit']}"

    def lon_plot_stability(self, mode):
        plot_aircraft_stability = PlotLongitudinalModes(self.get_natural_frequency(), self.get_damping_ratio())
        data = plot_aircraft_stability.plot(mode)
        return data
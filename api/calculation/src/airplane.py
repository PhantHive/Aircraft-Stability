import sys

from lateral.lat_aircraft_matrix import LatAircraftMatrix
from lateral.lat_control_matrix import LatControlMatrix
from longitudinal.lon_aircraft_matrix import LongAircraftMatrix
from longitudinal.lon_control_matrix import LongControlMatrix
from longitudinal.lon_plot_stability import PlotLongitudinalModes

sys.path.append("calculation/src")


class Airplane(LongAircraftMatrix, LongControlMatrix, LatAircraftMatrix,
               LatControlMatrix):
    """
    This class is used to calculate the aircraft matrix and the control matrix
    It is also used to get the cruise conditions
    """

    def __init__(
        self,
        name,
        wing_area,
        aspect_ratio,
        taper_ratio,
        wingspan,
        wing_mean_chord,
        wing_oswald,
        axis="longitudinal",
        user_file=None,
    ):
        if axis == "longitudinal":
            LongAircraftMatrix.__init__(self, user_file=user_file)
            LongControlMatrix.__init__(self, user_file=user_file)
        elif axis == "lateral":
            LatAircraftMatrix.__init__(self, user_file=user_file)
            LatControlMatrix.__init__(self, user_file=user_file)

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
        LongAircraftMatrix.calculate_Xu(self, self.wing_area)
        LongAircraftMatrix.calculate_Xw(self, self.aspect_ratio,
                                        self.wing_oswald, self.wing_area)

        # Calculate Z matrix coefficients (Zu, Zw, Zw_dot, Zq)
        LongAircraftMatrix.calculate_Zu(self, self.wing_area)
        LongAircraftMatrix.calculate_Zw(self, self.wing_area)
        LongAircraftMatrix.calculate_Zw_dot(self, self.wing_mean_chord,
                                            self.wing_area)
        LongAircraftMatrix.calculate_Zq(self, self.wing_mean_chord,
                                        self.wing_area)

        # Calculate M matrix coefficients (Mu, Mw, Mw_dot, Mq)
        LongAircraftMatrix.calculate_Mu(self, self.wing_mean_chord,
                                        self.wing_area)
        LongAircraftMatrix.calculate_Mw(self, self.wing_mean_chord,
                                        self.wing_area)
        LongAircraftMatrix.calculate_Mw_dot(self, self.wing_mean_chord,
                                            self.wing_area)
        LongAircraftMatrix.calculate_Mq(self, self.wing_mean_chord,
                                        self.wing_area)

        # Get aircraft matrix for longitudinal stability
        LongAircraftMatrix.set_long_stability_aircraft_matrix(self)
        # ------------------------------------------------------------------------------------------ #

    def get_longitudinal_control_matrix(self):
        # ----------------- Calculate the control matrix for longitudinal stability ----------------- #
        # Calculate X_delta_e
        LongControlMatrix.calculate_X_delta_e(self, self.wing_area)

        # Calculate Z_delta_e
        LongControlMatrix.calculate_Z_delta_e(self, self.wing_area)

        # Calculate M_delta_e
        LongControlMatrix.calculate_M_delta_e(self, self.wing_area,
                                              self.wing_mean_chord)

        LongControlMatrix.calculate_X_delta_T(self, self.wing_area)

        LongControlMatrix.calculate_Z_delta_T(self, self.wing_area)

        LongControlMatrix.calculate_M_delta_T(self, self.wing_area,
                                              self.wing_mean_chord)

        # Get control matrix
        LongControlMatrix.set_long_stability_control_matrix(self, self.Mw_dot)
        # ------------------------------------------------------------------------------------------ #

    def get_lateral_aircraft_matrix(self):
        # ----------------- Calculate the aircraft matrix for lateral stability ----------------- #
        # Calculate Y matrix coefficients (Yv, Yp, Yr)
        LatAircraftMatrix.calculate_Yv(self, self.wing_area)
        LatAircraftMatrix.calculate_Yp(self, self.wing_area, self.wingspan)
        LatAircraftMatrix.calculate_Yr(self, self.wing_area, self.wingspan)

        # Calculate L matrix coefficients (Lv, Lp, Lr)
        LatAircraftMatrix.calculate_Lv(self, self.wing_area, self.wingspan)
        LatAircraftMatrix.calculate_Lp(self, self.wing_area, self.wingspan)
        LatAircraftMatrix.calculate_Lr(self, self.wing_area, self.wingspan)

        # Calculate N matrix coefficients (Nv, Np, Nr)
        LatAircraftMatrix.calculate_Nv(self, self.wing_area, self.wingspan)
        LatAircraftMatrix.calculate_Np(self, self.wing_area, self.wingspan)
        LatAircraftMatrix.calculate_Nr(self, self.wing_area, self.wingspan)

        # Get aircraft matrix for lateral stability
        LatAircraftMatrix.set_lat_stability_aircraft_matrix(self)
        # ------------------------------------------------------------------------------------------ #

    def get_lateral_control_matrix(self):
        # ----------------- Calculate the control matrix for lateral stability ----------------- #
        # Calculate Y_delta_r
        LatControlMatrix.calculate_Y_delta_r(self, self.wing_area)

        # Calculate L_delta_r
        LatControlMatrix.calculate_L_delta_r(self, self.wing_area,
                                             self.wingspan)

        # Calculate N_delta_r
        LatControlMatrix.calculate_N_delta_r(self, self.wing_area,
                                             self.wingspan)

        # Calculate Y_delta_a
        LatControlMatrix.calculate_Y_delta_a(self, self.wing_area)

        # Calculate L_delta_a
        LatControlMatrix.calculate_L_delta_a(self, self.wing_area,
                                             self.wingspan)

        # Calculate N_delta_a
        LatControlMatrix.calculate_N_delta_a(self, self.wing_area,
                                             self.wingspan)

        # Get control matrix
        LatControlMatrix.set_lat_stability_control_matrix(self)
        # ------------------------------------------------------------------------------------------ #

    def get_cruise_condition(self, coeff):
        return f"{self.cruise_conditions[coeff]['value']} {self.cruise_conditions[coeff]['unit']}"

    def lon_plot_stability(self, mode):
        plot_aircraft_stability = PlotLongitudinalModes(
            self.get_natural_frequency(), self.get_damping_ratio())
        data = plot_aircraft_stability.plot(mode)
        return data

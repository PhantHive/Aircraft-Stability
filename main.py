from src.aircraft_matrix import AircraftMatrix
from src.control_matrix import ControlMatrix


class Airplane(AircraftMatrix, ControlMatrix):
    '''
    This class is used to calculate the aircraft matrix and the control matrix
    It is also used to get the cruise conditions
    '''

    def __init__(self, name, wing_area, aspect_ratio, taper_ratio, wingspan, wing_mean_chord, wing_oswald):
        super().__init__()
        self.name = name
        self.wing_area = wing_area  # S
        self.aspect_ratio = aspect_ratio  # A
        self.taper_ratio = taper_ratio  # lambda
        self.wingspan = wingspan  # b
        self.wing_mean_chord = wing_mean_chord  # c
        self.wing_oswald = wing_oswald  # e

    def calculate_aircraft_matrix(self):
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

        # Get aircraft matrix
        AircraftMatrix.set_aircraft_matrix(self)

    def calculate_control_matrix(self):
        # Calculate X_delta_e
        ControlMatrix.calculate_X_delta_e(self, self.wing_area)

        # Calculate Z_delta_e
        ControlMatrix.calculate_Z_delta_e(self, self.wing_area)

        # Calculate M_delta_e
        ControlMatrix.calculate_M_delta_e(self, self.wing_mean_chord, self.wing_area)

        # Get control matrix
        ControlMatrix.set_control_matrix(self, self.Mw_dot)

    def get_cruise_condition(self, coeff):
        return f"{self.cruise_conditions[coeff]['value']} {self.cruise_conditions[coeff]['unit']}"


if __name__ == '__main__':

    # Example to use the class
    # (the values are from a Business JET aircraft)
    S = 21.55
    A = 5.1
    lambda_ = 0.5
    b = 10.48
    c_mean = 2.13
    e = 0.94

    airplane = Airplane("Business JET", S, A, lambda_, b, c_mean, e)
    print("--------------------------------")
    print("Exemple to get the aircraft matrix:\n")
    airplane.calculate_aircraft_matrix()
    print(airplane.aircraft_matrix)
    print("--------------------------------")

    print("Exemple to get a cruise condition")
    print("U0 = ", airplane.get_cruise_condition("V"))
    print("--------------------------------")

    '''print("Exemple to get the elevator derivatives vector:\n")
    airplane.calculate_control_matrix()
    print(airplane.get_elevator_derivatives())'''

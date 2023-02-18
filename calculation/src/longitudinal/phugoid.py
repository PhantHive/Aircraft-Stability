import numpy as np
from matplotlib import pyplot as plt


class Phugoid:

    def __init__(self):


        # short-period mode (high frequency)
        self.w_nsp = 4.04 # rad/s natural frequency
        self.Xi_sp = 0.2786 # damping ratio

        # phugoid mode (low frequency)
        self.Xi_p = 0.061 # damping ratio
        self.w_np = 0.09 # rad/s natural frequency


    def plot_phugoid(self):
        pass


if __name__ == '__main__':

    phugoid = Phugoid()

    phugoid.plot_phugoid()




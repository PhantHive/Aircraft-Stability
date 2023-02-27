import numpy as np
from matplotlib import pyplot as plt
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


class PlotLongitudinalModes:
    def __init__(self, natural_frequency, damping_ratio):
        self.natural_frequency = natural_frequency
        self.damping_ratio = damping_ratio

    def plot(self, mode):
        omega_n = 0
        zeta = 0
        t = 0
        if mode == "short_period":
            omega_n = self.natural_frequency[0]
            zeta = self.damping_ratio[0]
            t = np.linspace(0, 4, 1000)
        elif mode == "phugoid":
            omega_n = self.natural_frequency[1]
            zeta = self.damping_ratio[1]
            t = np.linspace(0, 600, 1000)
            plt.yticks(np.arange(-1, 2, 0.5))
        else:
            print("Mode does not exist")

        A = 1  # initial disturbance in pitch angle

        # Define time vector

        # Compute phugoid mode response
        wn_zeta = omega_n * zeta
        A1 = A
        A2 = -A * wn_zeta / omega_n
        u = A1 * np.exp(-zeta * omega_n * t) * np.cos(
            omega_n * np.sqrt(1 - zeta**2) * t
        ) + A2 * np.exp(-zeta * omega_n * t) * np.sin(
            omega_n * np.sqrt(1 - zeta**2) * t
        )

        fig = plt.figure()
        # Plot response
        plt.plot(t, u)
        plt.xlabel("Time (s)")
        plt.ylabel("Pitch angle (rad)")
        plt.title("Phugoid Mode Response")
        plt.grid(True)

        # Render the plot as a bitmap or vector graphics format
        canvas = FigureCanvas(fig)
        buf = io.BytesIO()
        # Or use print_svg or print_pdf for other formats
        canvas.print_png(buf)

        # Convert the rendered plot to a binary data payload
        data = base64.b64encode(buf.getvalue()).decode("utf-8")

        return data

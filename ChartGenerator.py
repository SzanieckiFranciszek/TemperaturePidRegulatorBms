import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import make_interp_spline


class ChartGenerator:

    feedback_list = []
    time_list = []
    setpoint_list = []

    def __init__(self, total_sampling):
        self.total_sampling = total_sampling

    def chart_generator(self):
        time_sm = np.array(self.time_list)
        time_smooth = np.linspace(time_sm.min(), time_sm.max(), 300)
        helper_x3 = make_interp_spline(self.time_list, self.feedback_list)
        feedback_smooth = helper_x3(time_smooth)

        fig1 = plt.gcf()
        fig1.subplots_adjust(bottom=0.15, left=0.1)

        plt.plot(time_smooth, feedback_smooth, color='red')
        plt.plot(self.time_list, self.setpoint_list, color='blue')
        plt.xlim((0, self.total_sampling))
        plt.ylim((min(self.feedback_list) - 0.5, max(self.feedback_list) + 0.5))
        plt.xlabel('time (s)')
        plt.ylabel('PID (PV)')
        plt.title('Temperature PID Controller')
        plt.grid(True)

        fig1.savefig('pid_temperature.png', dpi=100)

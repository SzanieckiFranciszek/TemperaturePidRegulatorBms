import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import make_interp_spline


class ChartGenerator:

    first_pid_feedback_list = []
    second_pid_feedback_list = []
    time_list = []

    def __init__(self, total_sampling):
        self.total_sampling = total_sampling

    def chart_generator(self):
        time_array = np.array(self.time_list)
        time_smooth = np.linspace(time_array.min(), time_array.max(), 300)
        line_first_pid = make_interp_spline(self.time_list, self.first_pid_feedback_list)
        line_second_pid = make_interp_spline(self.time_list, self.second_pid_feedback_list)
        first_pid_feedback = line_first_pid(time_smooth)
        second_pid_feedback = line_second_pid(time_smooth)

        fig1 = plt.gcf()
        fig1.subplots_adjust(bottom=0.15, left=0.1)

        plt.plot(time_smooth, first_pid_feedback, color='green')
        plt.plot(time_smooth, second_pid_feedback, color='blue')
        plt.xlim((0, self.total_sampling))
        plt.ylim((min(self.first_pid_feedback_list) - 0.5, max(self.first_pid_feedback_list) + 0.5))
        plt.ylim((min(self.second_pid_feedback_list) - 0.5, max(self.second_pid_feedback_list) + 0.5))
        plt.xlabel('time')
        plt.ylabel("pid value\n[green - first pid [temp]; blue - second pid [%]]")
        plt.title('Temperature PID Controller')
        plt.grid(True)

        fig1.savefig('pid_temperature.png', dpi=100)

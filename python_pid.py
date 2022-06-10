import matplotlib

from pid_regulator import PidRegulator

matplotlib.use('Agg')

import time
import random
from ChartGenerator import ChartGenerator


def print_chart(total_sampling):
    chart = ChartGenerator(total_sampling)
    chart.chart_generator()


class PythonPID:

    def __init__(self, P=1, I=0.01, D=0.01, first_pid_min_output=10, first_pid_max_output=40, second_pid_min_output=0,
                 second_pid_max_output=100, total_sampling=100):
        self.P = P
        self.I = I
        self.D = D
        self.pidFirst = PidRegulator(P, I, D)
        # ToDo To implement Second Regulator
        self.pidSecond = PidRegulator(P, I, D)
        self.pidFirst.output_limits = (first_pid_min_output, first_pid_max_output)
        self.pidSecond.output_limits = (second_pid_min_output, second_pid_max_output)
        self.total_sampling = total_sampling
        self.sampling_i = 0
        self.measurement = 0
        self.feedback = 0

        print('PID controller is running..')

    def run_pid_controller(self):
        try:
            while 1:
                temperature = random.randint(0,
                                             30)  # zasymulować jakoś dane które reagują na feedback - najlepiej przy pomocy PID
                if temperature is not None:
                    if self.pidFirst.setpoint > 0:
                        self.feedback = temperature
                output = self.pidFirst(self.feedback)
                print('i={0} desired.temp={1:0.1f}*C temp={2:0.1f}*C pid.out = {3: 0.1f}feedback = {4: 0.1f}'.format(
                    self.sampling_i,
                    self.pidFirst.setpoint,
                    temperature,
                    output,
                    self.feedback))
                if self.sampling_i < 20:
                    self.pidFirst.setpoint = 28  # celsius
                if 20 < self.sampling_i < 40:
                    self.pidFirst.setpoint = 25  # celsius
                if 40 < self.sampling_i < 60:
                    self.pidFirst.setpoint = 20  # celsius
                if 60 < self.sampling_i < 80:
                    self.pidFirst.setpoint = 25  # celsius
                if self.sampling_i > 80:
                    self.pidFirst.setpoint = 28  # celsius
                time.sleep(1)
                self.sampling_i += 1
                ChartGenerator.feedback_list.append(self.feedback)
                ChartGenerator.setpoint_list.append(self.pidFirst.setpoint)
                ChartGenerator.time_list.append(self.sampling_i)
                if self.sampling_i >= self.total_sampling:
                    break
        except KeyboardInterrupt:
            print("exit")

        print("pid controller done.")
        print("generating a report...")
        print_chart(self.total_sampling)
        print("finish")






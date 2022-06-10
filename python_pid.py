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

    def __init__(self, P1=1.0, I1=0.25, D1=0.0, P2=1.0, I2=0.5, D2=0.0, first_pid_min_output=10, first_pid_max_output=40, second_pid_min_output=0,
                 second_pid_max_output=100, total_sampling=2000):
        self.P1 = P1
        self.I1 = I1
        self.D1 = D1
        self.P2 = P2
        self.I2 = I2
        self.D2 = D2
        self.pidFirst = PidRegulator(P1, I1, D1)
        self.pidSecond = PidRegulator(P2, I2, D2)
        self.pidFirst.output_limits = (first_pid_min_output, first_pid_max_output)
        self.pidSecond.output_limits = (second_pid_min_output, second_pid_max_output)
        self.total_sampling = total_sampling
        self.sampling_i = 0
        self.feedback = 0
        self.outdoor_temperature = 10
        self.pidFirst.setpoint = 22

        self.loss_heat = 0.153424 # utrata ciepla w pomieszczeniu
         # init
        self.output_first_regulator=0
        self.output_second_regulator = 0

        self.supply_temperature = self.outdoor_temperature
        self.room_temperature = self.outdoor_temperature

        print('PID controller is running..')

    def run_pid_controller(self):
        try:
            while 1:
                self.supply_temperature = self.outdoor_temperature + (self.output_second_regulator / 100 * 40)
                self.room_temperature = (0.9 * self.room_temperature) + (0.1 * self.supply_temperature) - self.loss_heat

                self.output_first_regulator = self.pidFirst(self.room_temperature)

                print('PID 1 : i={0} SP room temp={1:0.1f}*C measured room temp={2:0.1f}*C pid out value = {3: 0.1f}*C '.format(
                    self.sampling_i,
                    self.pidFirst.setpoint,
                    self.room_temperature,
                    self.output_first_regulator))

                # self.feedback_second_regulator = ventilation_temperature

                self.pidSecond.setpoint = self.output_first_regulator

                self.output_second_regulator = self.pidSecond(self.supply_temperature)

                print('PID 2 : i={0} SP supply temp={1:0.1f}*C measured ventilator temp={2:0.1f}*C pid out value = {3: 0.1f}%  '.format(
                    self.sampling_i,
                    self.pidSecond.setpoint,
                    self.supply_temperature,
                    self.output_second_regulator))
                print('-----------------------------------------------------------------------------------------------------')

                if 500 < self.sampling_i:
                    self.pidFirst.setpoint = 24  # celsius
                # if 20 < self.sampling_i < 40:
                #     self.
            #     pidFirst.setpoint = 25  # celsius
                # if 40 < self.sampling_i < 60:
                #     self.pidFirst.setpoint = 20  # celsius
                # if 60 < self.sampling_i < 80:
                #     self.pidFirst.setpoint = 25  # celsius
                # if self.sampling_i > 80:
                #     self.pidFirst.setpoint = 28  # celsius

                time.sleep(0.1)
                self.sampling_i += 1
                ChartGenerator.feedback_list.append(self.feedback)
                ChartGenerator.setpoint_list.append(self.pidFirst.setpoint)
                ChartGenerator.time_list.append(self.sampling_i)
                if self.sampling_i >= self.total_sampling:
                    break

        except KeyboardInterrupt:
            print("exit")

        print_chart(self.total_sampling)






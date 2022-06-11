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

    def __init__(self, P1=1.0, I1=0.25, D1=0.0, P2=1.0, I2=0.5, D2=0.0, first_pid_min_output=10,
                 first_pid_max_output=40, second_pid_min_output=0,
                 second_pid_max_output=100, total_sampling=1000):
        self.P1 = P1
        self.I1 = I1
        self.D1 = D1
        self.P2 = P2
        self.I2 = I2
        self.D2 = D2
        self.first_pid = PidRegulator(P1, I1, D1)
        self.second_pid = PidRegulator(P2, I2, D2)
        self.first_pid.output_limits = (first_pid_min_output, first_pid_max_output)
        self.second_pid.output_limits = (second_pid_min_output, second_pid_max_output)
        self.total_sampling = total_sampling
        self.iteration_sampling = 0
        self.feedback = 0
        self.outdoor_temperature = 10
        self.first_pid.setpoint = 22

        self.loss_heat = 0.153424  # utrata ciepla w pomieszczeniu
        self.output_first_regulator = 0
        self.output_second_regulator = 0

        self.supply_temperature = self.outdoor_temperature
        self.room_temperature = self.outdoor_temperature

        print('PI controller is running..')

    def run_pid_controller(self):
        try:
            while 1:
                self.supply_temperature = self.outdoor_temperature + (self.output_second_regulator / 100 * 40)
                self.room_temperature = (0.9 * self.room_temperature) + (0.1 * self.supply_temperature) - self.loss_heat

                self.output_first_regulator = self.first_pid(self.room_temperature)
                self.first_pid_data_printer()

                self.second_pid.setpoint = self.output_first_regulator
                self.output_second_regulator = self.second_pid(self.supply_temperature)
                self.second_pid_data_printer()

                ChartGenerator.first_pid_feedback_list.append(self.output_first_regulator)
                ChartGenerator.second_pid_feedback_list.append(self.output_second_regulator)
                ChartGenerator.time_list.append(self.iteration_sampling)

                if 200 < self.iteration_sampling:
                    self.first_pid.setpoint = 24
                if 500 < self.iteration_sampling:
                    self.first_pid.setpoint = 22
                time.sleep(0.1)
                self.iteration_sampling += 1
                if self.iteration_sampling >= self.total_sampling:
                    break

        except KeyboardInterrupt:
            print("exit")

        finally:
            print_chart(self.total_sampling)

    def first_pid_data_printer(self):
        print('PID 1 : i={0} SP room temp={1:0.1f}*C measured room temp={2:0.1f}*C pid out value = {3: 0.1f}*C '
            .format(
                self.iteration_sampling,
                self.first_pid.setpoint,
                self.room_temperature,
                self.output_first_regulator))

    def second_pid_data_printer(self):
        print('PID 2 : i={0} SP supply temp={1:0.1f}*C measured ventilator temp={2:0.1f}*C pid out value = {3: 0.1f}%  '
            .format(
                self.iteration_sampling,
                self.second_pid.setpoint,
                self.supply_temperature,
                self.output_second_regulator))
        print('\n------------------------------------------------------------------------------------------------\n')

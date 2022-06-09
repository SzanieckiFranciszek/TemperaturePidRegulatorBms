import matplotlib

matplotlib.use('Agg')

import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import random
from pid_regulator import PidRegulator



P = 1
I = 0.01
D = 0.1
pidFirst = PidRegulator(P, I, D)
#ToDo To implement Second Regulator
pidSecond = PidRegulator(P, I, D)
pidFirst.output_limits = (10, 40)
pidSecond.output_limits = (0,100)
total_sampling = 100
sampling_i = 0
measurement = 0
feedback = 0

feedback_list = []
time_list = []
setpoint_list = []

print('PID controller is running..')
try:
    while 1:
        temperature = random.randint(0, 30) # zasymulować jakoś dane które reagują na feedback - najlepiej przy pomocy PID
        if temperature is not None:
            if pidFirst.setpoint > 0:
                feedback = temperature
        output = pidFirst(feedback)
        print('i={0} desired.temp={1:0.1f}*C temp={2:0.1f}*C pid.out = {3: 0.1f}feedback = {4: 0.1f}'.format(sampling_i, pidFirst.setpoint, temperature, output, feedback))

        if  sampling_i < 20:
            pidFirst.setpoint = 28  # celsius
        if  20 < sampling_i < 40:
            pidFirst.setpoint = 25  # celsius
        if 40 < sampling_i < 60:
            pidFirst.setpoint = 20  # celsius
        if 60 < sampling_i < 80:
            pidFirst.setpoint = 25  # celsius
        if sampling_i > 80:
            pidFirst.setpoint = 28  # celsius
        time.sleep(1)
        sampling_i += 1
        feedback_list.append(feedback)
        setpoint_list.append(pidFirst.setpoint)
        time_list.append(sampling_i)
        if sampling_i >= total_sampling:
            break
except KeyboardInterrupt:
    print("exit")

print("pid controller done.")
print("generating a report...")
time_sm = np.array(time_list)
time_smooth = np.linspace(time_sm.min(), time_sm.max(), 300)
helper_x3 = make_interp_spline(time_list, feedback_list)
feedback_smooth = helper_x3(time_smooth)
fig1 = plt.gcf()
fig1.subplots_adjust(bottom=0.15, left=0.1)
plt.plot(time_smooth, feedback_smooth, color='red')
plt.plot(time_list, setpoint_list, color='blue')
plt.xlim((0, total_sampling))
plt.ylim((min(feedback_list) - 0.5, max(feedback_list) + 0.5))
plt.xlabel('time (s)')
plt.ylabel('PID (PV)')
plt.title('Temperature PID Controller')
plt.grid(True)
fig1.savefig('pid_temperature.png', dpi=100)
print("finish")

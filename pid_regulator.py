import time
import warnings


def _clamp(value, limits):

    lower, upper = limits
    if value is None:
        return None
    elif (upper is not None) and (value > upper):
        return upper
    elif (lower is not None) and (value < lower):
        return lower
    return value


try:
    _current_time = time.monotonic

except AttributeError:
    _current_time = time.time
    warnings.warn('time.monotonic() not available in python < 3.3, using time.time() as fallback')


class PidRegulator(object):

    def __init__(self, Kp=1.0, Ki=0.0, Kd=0.0, setpoint=0, sample_time=1, output_limits=(None, None), error_map=None,):

        self.Kp, self.Ki, self.Kd = Kp, Ki, Kd
        self.setpoint = setpoint
        self.sample_time = sample_time

        self._min_output, self._max_output = None, None
        self.error_map = error_map

        self._proportional = 0
        self._integral = 0
        self._derivative = 0

        self._last_time = None
        self._last_output = None
        self._last_input = None

        self.output_limits = output_limits
        self.reset()

    def __call__(self, input_, dt=None):

        now = _current_time()
        if dt is None:
            dt = now - self._last_time if (now - self._last_time) else 1e-16
        elif dt <= 0:
            raise ValueError('dt has negative value {}, must be positive'.format(dt))

        if self.sample_time is not None and dt < self.sample_time and self._last_output is not None:
            return self._last_output

        error = self.setpoint - input_
        d_input = input_ - (self._last_input if (self._last_input is not None) else input_)

        if self.error_map is not None:
            error = self.error_map(error)

        self._proportional = self.Kp * error
        self._integral += self.Ki * error * dt
        self._integral = _clamp(self._integral, self.output_limits)

        self._derivative = -self.Kd * d_input / dt

        output = self._proportional + self._integral
        output = _clamp(output, self.output_limits)

        self._last_output = output
        self._last_input = input_
        self._last_time = now

        return output

    @property
    def output_limits(self):
        return self._min_output, self._max_output

    @output_limits.setter
    def output_limits(self, limits):

        if limits is None:
            self._min_output, self._max_output = None, None
            return

        min_output, max_output = limits

        if (None not in limits) and (max_output < min_output):
            raise ValueError('lower limit must be less than upper limit')

        self._min_output = min_output
        self._max_output = max_output

        self._integral = _clamp(self._integral, self.output_limits)
        self._last_output = _clamp(self._last_output, self.output_limits)

    def reset(self):

        self._proportional = 0
        self._integral = 0
        self._derivative = 0

        self._integral = _clamp(self._integral, self.output_limits)

        self._last_time = _current_time()
        self._last_output = None
        self._last_input = None

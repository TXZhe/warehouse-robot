from types import *


class TCPData(object):
    def __init__(self):
        self.mode = None
        self.option = None
        self.ultrasonic = None
        self.leftWheelSpeed = None
        self.rightWheelSpeed = None
        self.gyro = None

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        # auto/manual 0/1
        self._mode = value
        if self._mode is None:
            self._mode = 0

    @mode.deleter
    def mode(self):
        del self._mode

    @ultrasonic.setter
    def ultrasonic(self, value):
        # auto/manual 0/1
        self._ultrasonic = value
        if self._ultrasonic is None:
            self._ultrasonic = 0

    @ultrasonic.deleter
    def ultrasonic(self):
        del self._ultrasonic

    @leftWheelSpeed.setter
    def leftWheelSpeed(self, value):
        # auto/manual 0/1
        self._leftWheelSpeed = value
        if self._leftWheelSpeed is None:
            self._leftWheelSpeed = 0

    @leftWheelSpeed.deleter
    def leftWheelSpeed(self):
        del self._leftWheelSpeed

    @rightWheelSpeed.setter
    def rightWheelSpeed(self, value):
        # auto/manual 0/1
        self._rightWheelSpeed = value
        if self._rightWheelSpeed is None:
            self._rightWheelSpeed = 0

    @rightWheelSpeed.deleter
    def rightWheelSpeed(self):
        del self._rightWheelSpeed

    @gyro.setter
    def gyro(self, value):
        # auto/manual 0/1
        self._gyro = value
        if self._gyro is None:
            self._gyro = 0

    @gyro.deleter
    def gyro(self):
        del self._gyro

    @property
    def option(self):
        return self._option

    @option.setter
    def option(self, value):
        self._option = value
        if self._option is None:
            self._option = 1

    @option.deleter
    def option(self):
        del self._option

    def data_print(self):
        print("Data: {}, {}, {}, {}, {}, {}").format(self._mode, self._option,self._ultrasonic,self._leftWheelSpeed,self._rightWheelSpeed,self._gyro)

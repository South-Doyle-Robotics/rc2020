from wpilib import Spark

class LED(Spark):
    def __init__(self, pwm_channel):
        '''
        To adjust the Rev LEDs, it must be treated as a Spark motor. 
        The percentage output determines the LEDs' pattern.
        '''
        super().__init__(pwm_channel)
        self.set_default()

    def set_default(self):
        '''
        Automatically sets it to the rainbow pattern.
        '''
        super().set(-0.99)

    def slow_heartbeat(self):
        super().set(0.03)

    def medium_heartbeat(self):
        super().set(0.05)

    def fast_heartbeat(self):
        super().set(0.07)

    def red(self):
        super().set(0.61)

    def yellow(self):
        super().set(0.69)

    def green(self):
        super().set(0.71)
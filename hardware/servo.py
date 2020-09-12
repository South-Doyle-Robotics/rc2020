import wpilib

class Servo(wpilib.Servo):
    def __init__(self, pwm_channel):
        super().__init__(pwm_channel)

    def set_position(self, position):
        '''
        Set position relative to the total range of the servo.

        0 is all the way to the left, 1 is all the way to the right
        '''

        self.set(position)
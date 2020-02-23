from hardware import SparkMax
from constants import MAGAZINE_FEED_MOTOR, MAGAZINE_LEFT_MOTOR, MAGAZINE_RIGHT_MOTOR
from tools import Timer


class Magazine:
    '''
    This object is responsible for managing the singulator,
    which is both the intake and the magazine.
    '''

    def __init__(self):
        '''
        '''
        self.feed_motor = SparkMax(MAGAZINE_FEED_MOTOR)
        self.left_agitator = SparkMax(MAGAZINE_LEFT_MOTOR)
        self.right_agitator = SparkMax(MAGAZINE_RIGHT_MOTOR)

        # Timer used to get motor up to speed
        self.timer = Timer()

    def is_ready(self):
        '''
        Checks if the motor underneath the shooter is at maximum voltage.
        '''
        return self.timer.get() > 0.25

    def stop(self):
        '''
        Stops all the motors. 
        Note: It's better to use stopMotor() instead of setting the percentage to zero.
        '''
        self.feed_motor.stopMotor()
        self.left_agitator.stopMotor()
        self.right_agitator.stopMotor()
        self.timer.start()

    def agitate(self):
        '''
        '''
        if self.ready_to_index():
            self.left_agitator.set_percent_output(-0.5)
            self.right_agitator.set_percent_output(0.5)

    def dump(self):
        '''
        '''
        self.feed_motor.set_percent_output(0.5)
        self.agitate()

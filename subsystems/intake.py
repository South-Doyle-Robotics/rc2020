from hardware import SparkMax, Falcon, DoubleSolenoid
from constants import INTAKE_MOTOR, INTAKE_SOLENOID_DEPLOY, INTAKE_SOLENOID_RETRACT


class Intake:
    '''
    The object thats responsible for managing the intake
    '''

    INTAKE_SPEED = 0.4

    def __init__(self):
        self.motor = SparkMax(INTAKE_MOTOR)
        self.solenoid = DoubleSolenoid(
            INTAKE_SOLENOID_DEPLOY, INTAKE_SOLENOID_RETRACT)

    def idle(self):
        '''
        Retract the intake and stop its motors

        idle(self)
        '''
        self.motor.set_percent_output(0)
        self.solenoid.forward()

    def intake(self):
        '''
        Deploy the intake and start its motors

        intake(self)
        '''
        self.motor.set_percent_output(self.INTAKE_SPEED)
        self.solenoid.reverse()

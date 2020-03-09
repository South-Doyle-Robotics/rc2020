from hardware import Servo, Falcon, DoubleSolenoid
from constants import ELEVATOR_SERVO, ELEVATOR_SOLENOID_DEPLOY, ELEVATOR_SOLENOID_LOWER, ELEVATOR_MOTOR


class Climber:
    '''
    The object thats responsible for managing the intake
    '''

    UNSPOOL_SPEED = 0.35
    SPOOL_SPEED = 0.8

    def __init__(self):
        self.servo = Servo(ELEVATOR_SERVO)
        self.motor = Falcon(ELEVATOR_MOTOR)
        self.solenoid = DoubleSolenoid(
            ELEVATOR_SOLENOID_DEPLOY, ELEVATOR_SOLENOID_LOWER)
        self.lower()
        self.motor.reset()

    def is_deployed(self):
        return self.has_been_deployed

    def deploy(self):
        '''
        Pump the pneumatics to raise the climber to position 
        '''
        self.solenoid.forward()
        self.has_been_deployed = True

    def lower(self):
        '''
        Pump the pneumatics to pull the climber back to its lowered state 
        '''
        self.solenoid.reverse()
        self.has_been_deployed = False

    def extend(self):
        '''
        Extend the climber mechanism outward to hook onto the bar
        '''
        self.motor.set_percent_output(self.UNSPOOL_SPEED)
        self.servo.set(0.46)

    def retract(self):
        '''
        Retract the climber mechanism inward to pull the robot up
        '''
        counts = self.motor.get_counts()
        self.motor.set_percent_output(-self.SPOOL_SPEED)
        # if abs(counts) > 4096 * 10:
        #     print("FAST", counts)
        #     self.motor.set_percent_output(-self.SPOOL_SPEED)
        # else:
        #     print("SLOW")
        #     self.motor.set_percent_output(-0.08)

        self.servo.set(1)

    def stop(self):
        self.motor.set_percent_output(0)
from hardware import Servo, Falcon, DoubleSolenoid
from constants import ELEVATOR_SERVO, ELEVATOR_SOLENOID_DEPLOY, ELEVATOR_SOLENOID_LOWER, ELEVATOR_MOTOR, ELEVATOR_LIMIT_SWITCH
from wpilib import DigitalInput
from tools import Timer


class Climber:
    '''
    The object thats responsible for managing the climber
    '''

    UNSPOOL_SPEED = 0.5
    SPOOL_SPEED = 0.8

    def __init__(self):
        self.servo = Servo(ELEVATOR_SERVO)
        self.motor = Falcon(ELEVATOR_MOTOR)
        self.solenoid = DoubleSolenoid(
            ELEVATOR_SOLENOID_DEPLOY, ELEVATOR_SOLENOID_LOWER)
        self.lower()
        self.motor.reset()

        self.limit_switch = DigitalInput(ELEVATOR_LIMIT_SWITCH)
        self.timer = Timer()

        self.has_been_extended = False
        self.extend_position = 0.46

    def is_limit_switch_pressed(self):
        return self.limit_switch.get()

    def is_deployed(self):
        return self.has_been_deployed

    def is_extended(self):
        return self.has_been_extended and self.servo_at_position(self.extend_position)

    def servo_at_position(self, position):
        if self.servo.get() == position:
            return True

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
        #print("In climber extend")
        # self.motor.set_percent_output(self.UNSPOOL_SPEED)
        self.servo.set(self.extend_position)
        self.has_been_extended = True

    def retract(self):
        '''
        Retract the climber mechanism inward to pull the robot up
        '''
        # The limit switch appears to be backwards. Flipped logic from
        # NOT self.is_limit_switched_pressed to self.is_limit_switch_pressed
        # print("limit switch:", self.is_limit_switch_pressed())
        # print("spool speed", self.SPOOL_SPEED)
        if self.is_limit_switch_pressed():
            # print("in the limit switch loop")
            self.motor.set_percent_output(-self.SPOOL_SPEED)
            self.servo.set(1)
        self.has_been_extended = False
        # else:
        #print("NOT in the limit switch loop limit switch is pressed", self.is_limit_switch_pressed)

    def stop(self):
        self.motor.set_percent_output(0)

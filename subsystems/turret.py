from wpilib import SpeedControllerGroup, DigitalInput
from wpilib.controller import PIDController
from constants import TURRET_CLOCKWISE_LIMIT_SWITCH, TURRET_COUNTERCLOCKWISE_LIMIT_SWITCH, TURRET_TURN_MOTOR
from hardware import SparkMax
from math import pi

from .camera import Limelight


def encoder_to_angle(encoder_counts):
    '''
    Takes the encoder count of the turret motor, and converts it to
    an equivalent angle of the turret.
    '''
    # 112.5 is the motor revolutions per 1 turret revolution. 4096 is the encoder count.
    degrees_per_count = 360 / (112.5 * 4096)
    return degrees_per_count * encoder_counts


def angle_to_encoder(angle):
    '''
    Takes the angle of the turret and converts it into an encoder count.
    '''
    counts_per_degree = (112.5 * 4096) / 360
    return counts_per_degree * angle


class Turret:
    '''
    The object thats responsible for managing the shooter
    '''

    def __init__(self):
        self.clockwise_limit_switch = DigitalInput(
            TURRET_CLOCKWISE_LIMIT_SWITCH)
        self.counterclockwise_limit_switch = DigitalInput(
            TURRET_COUNTERCLOCKWISE_LIMIT_SWITCH)

        self.turn_motor = SparkMax(TURRET_TURN_MOTOR)
        self.turn_pid = PIDController(0.1, 0, 0)

    def set_target_angle(self, angle):
        '''
        Sets the target angle of the turret. This will use a PID to turn the
        turret to the target angle.
        '''

        target_encoder = angle_to_encoder(angle)
        self.turn_pid.setSetpoint(target_encoder)

    def update(self):
        '''
        This is used to continuously update the turret's event loop.

        All this manages as of now is the turrets PID controller.
        '''

        motor_speed = self.turn_pid.calculate(self.turn_motor.get_counts())

        if self.clockwise_limit_switch.get() and motor_speed < 0:
            self.turn_motor.set_percent_output(motor_speed)

        elif self.counterclockwise_limit_switch.get() and motor_speed > 0:
            self.turn_motor.set_percent_output(motor_speed)

        # Only turn to the target if the limelight can actually see the target. Otherwise, there can be someone who moves the turret with the controller.
        '''
        if self.limelight.has_target:
            # self.motor_speed sets to whatever the PID calculates
        '''

    def rotate_turret(self, direction):
        '''
        This is used to manually turn the turret so that the limelight is in sight of the target.
        '''
        self.turn_motor.set_percentage_output(direction)

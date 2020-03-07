from wpilib import SpeedControllerGroup, DigitalInput
from wpilib.controller import PIDController
from constants import TURRET_CLOCKWISE_LIMIT_SWITCH, TURRET_COUNTERCLOCKWISE_LIMIT_SWITCH, TURRET_TURN_MOTOR, TURRET_SHOOT_MOTORS
from hardware import SparkMax, Falcon
from math import pi
from tools import Timer

from .camera import Limelight


# For whatever our turn motor is. Neos are 42, Falcons are 2048
counts_per_revolution = 42


def encoder_to_angle(encoder_counts):
    '''
    Takes the encoder count of the turret motor, and converts it to
    an equivalent angle of the turret.
    '''
    # 112.5 is the motor revolutions per 1 turret revolution.
    # Probably should figure the motor revolutions per 1 turret revolution for the NEO550s.
    degrees_per_count = 360 / (112.5 * counts_per_revolution)
    return degrees_per_count * encoder_counts


def angle_to_encoder(angle):
    '''
    Takes the angle of the turret and converts it into an encoder count.
    '''
    counts_per_degree = (112.5 * counts_per_revolution) / 360
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
        self.turn_pid = PIDController(0.4, 0.001, 0.02)

        self.shoot_motor_1 = Falcon(TURRET_SHOOT_MOTORS[0])
        self.shoot_motor_2 = Falcon(TURRET_SHOOT_MOTORS[1])
        self.timer = Timer()

        self.limelight = Limelight()

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

        The shoot motor is constantly running at a low percentage until we need it.
        '''

        motor_speed = self.turn_pid.calculate(
            self.limelight.get_target_screen_x())

        if self.clockwise_limit_switch.get() and motor_speed < 0:
            self.turn_motor.set_percent_output(motor_speed)

        elif self.counterclockwise_limit_switch.get() and motor_speed > 0:
            self.turn_motor.set_percent_output(motor_speed)

    def shoot(self):
        '''
        The wheel to shoot will rev up completely before balls start feeding
        in from the singulator.
        '''
        # One of the motors will be reversed, so make sure the shoot motor has the correct ID!
        speed = self.shoot_motor_1.get_percent_output()
        if speed < 1:
            speed += 0.02
        elif speed > 1:
            speed -= 0.02

        self.shoot_motor_1.set_percent_output(speed)
        self.shoot_motor_2.set_percent_output(-speed)

    def idle(self):
        '''
        Resets the motors back to their default state.
        '''
        speed = self.shoot_motor_1.get_percent_output()
        if speed < 0.5:
            speed += 0.02
        elif speed > 0.5:
            speed -= 0.02

        self.shoot_motor_1.set_percent_output(speed)
        self.shoot_motor_2.set_percent_output(-speed)

    def is_full_speed(self):
        '''
        Returns if the motor is at full speed or not.
        '''
        self.timer.get() > 0.4

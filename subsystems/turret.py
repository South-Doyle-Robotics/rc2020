from wpilib import SpeedControllerGroup, DigitalInput
from wpilib.controller import PIDController
from constants import TURRET_CLOCKWISE_LIMIT_SWITCH, TURRET_COUNTERCLOCKWISE_LIMIT_SWITCH, TURRET_TURN_MOTOR, TURRET_SHOOT_MOTORS, TURRET_HOOD_MOTOR
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
    return encoder_counts / 77 * 360


def angle_to_encoder(angle):
    '''
    Takes the angle of the turret and converts it into an encoder count.
    '''
    return angle * 77 / 360


def distance_to_hood_encoder(distance):
    '''
    Converts the distance to the target to the hood's encoder counts.
    '''
    return (abs(distance) ** 0.695 + 0.25) * 100


class Turret:
    HOME_ANGLE = 250/2
    '''
    The object thats responsible for managing the shooter
    '''

    def __init__(self):
        self.clockwise_limit_switch = DigitalInput(
            TURRET_CLOCKWISE_LIMIT_SWITCH)
        self.counterclockwise_limit_switch = DigitalInput(
            TURRET_COUNTERCLOCKWISE_LIMIT_SWITCH)

        self.turn_motor = SparkMax(TURRET_TURN_MOTOR)
        self.turn_motor.set_current_limit(1)
        self.turn_pid = PIDController(0.4, 0.008, 0.0125)

        self.hood_motor = SparkMax(TURRET_HOOD_MOTOR)
        self.hood_motor.set_current_limit(1)
        self.hood_pid = PIDController(0.2, 0.008, 0)

        self.shoot_motor_1 = Falcon(TURRET_SHOOT_MOTORS[1])
        self.shoot_motor_2 = Falcon(TURRET_SHOOT_MOTORS[0])
        self.timer = Timer()

        self.limelight = Limelight()
        self.is_zeroed = False

    def reset(self):
        self.is_zeroed = False

    def stop_turning(self):
        self.turn_motor.set_percent_output(0)
        self.hood_motor.set_percent_output(0)

    def goto_angle(self, angle):
        '''
        This will make the turret follow a given angle.
        '''
        current_angle = encoder_to_angle(self.turn_motor.get_counts()) / 45
        # print("GOTO", current_angle, "setpoint", angle / 50)
        self.turn_pid.setSetpoint(angle / 45)
        motor_speed = self.turn_pid.calculate(current_angle)
        self.rotate(motor_speed)

    def track_limelight(self):
        '''
        This is used to continuously update the turret's event loop.

        All this manages as of now is the turrets PID controller.

        The shoot motor is constantly running at a low percentage until we need it.
        '''
        if self.limelight.has_target():
            self.turn_pid.setSetpoint(0)
            motor_speed = self.turn_pid.calculate(
                self.limelight.get_target_screen_x()+0.05)
            self.rotate(motor_speed)
            self.track_distance(self.limelight.get_target_screen_y())
        else:
            self.goto_angle(self.HOME_ANGLE)

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
        self.timer.start()

    def is_full_speed(self):
        '''
        Returns if the motor is at full speed or not.
        '''
        return self.timer.get() > 1

    def zero(self):
        if not self.clockwise_limit_switch.get():
            self.turn_motor.reset()
            self.is_zeroed = True

        if not self.is_zeroed:
            self.turn_motor.reset()
            self.hood_motor.reset()
            self.turn_motor.set_percent_output(-0.08)
            self.hood_motor.set_percent_output(0.6)

    def rotate(self, speed):
        '''
        Rotates the turret with a given speed

        if the speed > 0, right clockwise, otherwise rotate counterclockwise
        '''
        if not self.is_zeroed:
            return

        if self.clockwise_limit_switch.get() and speed > 0:
            self.turn_motor.set_percent_output(speed)

        elif self.counterclockwise_limit_switch.get() and speed < 0:
            self.turn_motor.set_percent_output(speed)

    def track_distance(self, distance):
        '''
        Set the distance to the target.

        This will update the hood position
        '''
        if not self.is_zeroed:
            return

        current_encoder = self.hood_motor.get_counts()
        self.hood_pid.setSetpoint(-distance_to_hood_encoder(distance))
        motor_speed = self.hood_pid.calculate(current_encoder)
        print("hood", current_encoder, "y val", distance, "setpoint",
              -distance_to_hood_encoder(distance), "output", motor_speed)
        if current_encoder < -100 and motor_speed < 0:
            self.hood_motor.set_percent_output(0)
        else:
            self.hood_motor.set_percent_output(motor_speed)

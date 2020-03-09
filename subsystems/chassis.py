from os.path import dirname
from constants import LEFT_CHASSIS_MOTORS, RIGHT_CHASSIS_MOTORS
from wpilib import SpeedControllerGroup
from hardware import Falcon, DoubleSolenoid
from traits import implements, DriveTrain, Gyro
from ctre import Orchestra, NeutralMode
from math import pi
from os.path import dirname


@implements(DriveTrain)
class Chassis:
    HIGH_GEAR_CONSTANT = 8.5
    LOW_GEAR_CONSTANT = 13.24

    def __init__(self):
        self.left_master = Falcon(LEFT_CHASSIS_MOTORS[0])
        self.left_motors = [self.left_master, *
                            list(map(Falcon, LEFT_CHASSIS_MOTORS[1:]))]

        self.right_master = Falcon(RIGHT_CHASSIS_MOTORS[0])
        self.right_motors = [self.right_master, *
                             list(map(Falcon, RIGHT_CHASSIS_MOTORS[1:]))]

        for motor in (self.left_motors + self.right_motors):
            motor.setNeutralMode(NeutralMode.Brake)

        self.shifter = DoubleSolenoid(7, 0)
        self.set_low_gear()

    def set_low_gear(self):
        self.shifter.forward()

    def set_high_gear(self):
        self.shifter.reverse()

    def get_average_distance(self):
        return (self.get_left_distance() + self.get_right_distance()) / 2

    def get_left_distance(self):
        return self.get_left_forward_revolutions() * self.get_wheel_diameter() * pi / self.LOW_GEAR_CONSTANT

    def get_right_distance(self):
        return self.get_right_forward_revolutions() * self.get_wheel_diameter() * pi / self.LOW_GEAR_CONSTANT

    def get_left_forward_revolutions(self):
        return -self.left_master.get_revolutions()

    def get_right_forward_revolutions(self):
        return self.right_master.get_revolutions()

    def get_wheel_diameter(self):
        return 0.1524

    def reset_encoders(self):
        self.left_master.reset()
        self.right_master.reset()

    def tank_drive(self, left, right):
        for motor in self.left_motors:
            motor.set(-left)

        for motor in self.right_motors:
            motor.set(right)

    arcade_drive = DriveTrain.arcade_drive

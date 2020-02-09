from constants import LEFT_CHASSIS_MOTORS, RIGHT_CHASSIS_MOTORS
from wpilib import SpeedControllerGroup
from hardware import Falcon, DoubleSolenoid
from traits import implements, DriveTrain, Gyro
from ctre import Orchestra
from math import pi

orchestra = Orchestra()


@implements(DriveTrain)
class Chassis:
    HIGH_GEAR_CONSTANT = 8.5
    LOW_GEAR_CONSTANT = 18.38

    def __init__(self):
        self.left_master = Falcon(LEFT_CHASSIS_MOTORS[0])
        self.raw_left_motors = [self.left_master] + \
            list(map(Falcon, LEFT_CHASSIS_MOTORS[1:]))
        self.left_motors = SpeedControllerGroup(*self.raw_left_motors)

        self.right_master = Falcon(RIGHT_CHASSIS_MOTORS[0])
        self.raw_right_motors = [self.right_master] + \
            list(map(Falcon, RIGHT_CHASSIS_MOTORS[1:]))
        self.right_motors = SpeedControllerGroup(*self.raw_right_motors)

        self.shifter = DoubleSolenoid(0, 1)
        self.set_low_gear()

    def play_music(self):
        for motor in self.raw_left_motors + self.raw_right_motors:
            print("music add falcon ", orchestra.addInstrument(motor))
        print("music load", orchestra.loadMusic("chrp/mario.chrp"))
        print("music play", orchestra.play())

    def stop_music(self):
        orchestra.stop()

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
        self.left_motors.set(-left)
        self.right_motors.set(right)

    arcade_drive = DriveTrain.arcade_drive

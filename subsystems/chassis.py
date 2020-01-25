from wpilib import SpeedControllerGroup
from hardware import Falcon
from traits import implements, DriveTrain, Gyro

@implements(DriveTrain)
class Chassis:
    def __init__(self):
        self.left_master = Falcon(1)
        self.left_motors = SpeedControllerGroup(self.left_master, Falcon(2))

        self.right_master = Falcon(3)
        self.right_motors = SpeedControllerGroup(self.right_master, Falcon(4))

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
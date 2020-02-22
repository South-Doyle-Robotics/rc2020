from . import Trait
from math import copysign

class DriveTrain(Trait):
    '''
    A generic drivetrain for the bot
    '''

    def get_left_forward_revolutions(self):
        '''
        Gets the left encoder's revolutions traveled forward
        '''
        pass

    def get_right_forward_revolutions(self):
        '''
        Gets the right encoder's revolutions traveled forward
        '''
        pass

    def reset_encoders(self):
        '''
        Resets the left and right encoders on the drive train
        '''
        pass

    def get_wheel_diameter(self):
        '''
        Get the diameter of the drivetrain's wheels
        '''
        pass

    def tank_drive(self, left, right):
        '''
        Set the left and right drive train speeds

        -1 is backward and 1 is forward.
        '''
        pass

    def set_low_gear(self):
        '''
        Puts the drive train in low gear
        '''
        pass

    def set_high_gear(self):
        '''
        Puts the drive train in high gear
        '''
        pass

    def arcade_drive(self, forward, turn, squared_inputs=True):
        def limit(n):
            if n < -1: return -1
            elif n > 1: return 1
            else: return n

        forward = limit(forward)
        turn = -limit(turn)

        if squared_inputs:
            forward = copysign(forward * forward, forward)
            turn = copysign(turn * turn, turn)


        if forward > 0.0:
            if turn > 0.0:
                leftMotorSpeed = forward - turn
                rightMotorSpeed = max(forward, turn)
            else:
                leftMotorSpeed = max(forward, -turn)
                rightMotorSpeed = forward + turn

        else:
            if turn > 0.0:
                leftMotorSpeed = -max(-forward, turn)
                rightMotorSpeed = forward + turn
            else:
                leftMotorSpeed = forward - turn
                rightMotorSpeed = -max(-forward, -turn)

        self.tank_drive(leftMotorSpeed, rightMotorSpeed)
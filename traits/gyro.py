from . import Trait

class Gyro(Trait):
    '''
    A generic robot gyro.
    '''
    def reset(self):
        '''
        When reset is called, the current angle will be the new zero.
        '''
        pass

    def get_clockwise_degrees(self):
        '''
        This method returns the robot's angle such that counterclockwise is negative and clockwise is positive.

        The result of this function may range from -180 to 180.
        '''
        pass

    def get_counterclockwise_degrees(self):
        '''
        This method returns the robot's angle such that clockwise is negative and counterclockwise is positive.

        The result of this function may range from -180 to 180.

        This method is important because WPILIB Ramsete controllers require counterclockwise to be positive.
        '''
        pass

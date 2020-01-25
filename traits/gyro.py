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

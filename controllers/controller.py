from traits import Trait


class Controller(Trait):
    '''
    A controller connected to the driverstation
    '''
    def forward(self):
        '''
        Return the joystick value of the axis controlling
        the forward driving of the robot chassis.
        '''
        pass

    def turn(self):
        '''
        Return the joystick value of the axis controlling
        the turning of the robot chassis while driving.
        '''
        pass

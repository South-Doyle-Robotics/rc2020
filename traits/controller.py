from . import Trait


class Controller(Trait):
    '''
    A controller connected to the driverstation
    '''
    def get_joystick(self):
        '''
        Return the underlying wpilib.Joystick object
        '''
        pass

    def axis(port, inverted=False):
        return lambda self: self.get_joystick().getRawAxis(port) * (-1 if inverted else 1)
    
    def button(port, inverted=False):
        return lambda self: self.get_joystick().getRawButton(port) * (-1 if inverted else 1)
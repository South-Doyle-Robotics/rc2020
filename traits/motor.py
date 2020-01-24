from . import Trait

class Motor(Trait):
    '''
    A generic motor object on the bot
    '''

    def set_percent_output(self, percent):
        '''
        This sets the percent output voltage of the motor.

        The `percent` method ranges from -1 to 1.
        -1 supplies -12 volts to the motor, 1 supplies 12 volts to the motor.
        '''
        pass

    def get_percent_output(self):
        '''
        This gets the last percent output voltage set by the `set_percent` method.

        The returned value will range from -1 to 1.
        '''
        pass
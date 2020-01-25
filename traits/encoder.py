from . import Trait

class Encoder(Trait):
    '''
    A generic encoder on a motor
    '''

    def get_revolutions(self):
        '''
        Returns the number of revolutions recorded by the encoder since it's been reset.

        This function can be directly used by classes that implement the Encoder trait
        '''
        return self.get_counts() / self.get_counts_per_revolution()

    def get_pulses(self):
        '''
        Get the number of encoder counts recorded divided by four.
        A pulse is counted every four encoder counts.

        This function can be directly used by classes that implement the Encoder trait
        '''
        return self.get_counts() / 4

    def get_counts(self):
        '''
        Get the number of ticks per revolution
        '''
        pass

    def get_counts_per_revolution(self):
        '''
        Get the number of encoder counts per revolution.
        '''
        pass

    def reset(self):
        '''
        Recalibrate the encoder counter such that the current encoder count is 0
        '''
        pass
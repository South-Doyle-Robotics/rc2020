from hardware.spark import SparkMax


class LED(SparkMax):
    def __init__(self):
        '''
        To adjust the Rev LEDs, it must be treated as a Spark motor. 
        The percentage output determines the LEDs' pattern.
        '''
        self.set_default()

    def set_default(self):
        '''
        Automatically sets it to the rainbow pattern.
        '''
        super().set_percent_output(-0.99)

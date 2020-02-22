from hardware import SparkMax


class Singulator:
    '''
    This object is responsible for managing the singulator,
    which is both the intake and the magazine.
    '''

    def __init__(self, feed_id, left_agitator_id, right_agitator_id):
        '''
        Feed_motor: The motor that directly spins balls into the shooter
        Left motor: The motor that indexes balls from the left
        Right motor: The motor that indexes balls from the right
        Intake motor: The motor that takes in balls
        '''
        self.feed_motor = SparkMax(feed_id)
        self.left_agitator = SparkMax(left_agitator_id)
        self.right_agitator = SparkMax(right_agitator_id)

    def ready_to_index(self):
        '''
        Checks if the motor underneath the shooter is at maximum voltage.
        '''
        if self.feed_motor.get_percent_output() == 0.5:
            return True

    def stop(self):
        '''
        Stops all the motors. 
        Note: It's better to use stopMotor() instead of setting the percentage to zero.
        '''
        self.feed_motor.stopMotor()
        self.left_agitator.stopMotor()
        self.right_agitator.stopMotor()

    def agitate(self):
        '''
        '''
        if self.ready_to_index():
            self.left_agitator.set_percent_output(-0.5)
            self.right_agitator.set_percent_output(0.5)

    def feed(self):
        '''
        A separate function for running the intake,
        as we will use it to both pull in balls and run with the magazine.

        This is most likely a terrible, terrible idea.
        '''
        self.feed_motor.set_percent_output(0.5)
        self.agitate()

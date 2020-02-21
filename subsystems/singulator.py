from hardware import SparkMax


class Singulator:
    '''
    This object is responsible for managing the singulator,
    which is both the intake and the magazine.
    '''

    def __init__(self, ball_feed_id, left_id, right_id, intake_id):
        '''
        Feed_motor: The motor that directly spins balls into the shooter
        Left motor: The motor that indexes balls from the left
        Right motor: The motor that indexes balls from the right
        Intake motor: The motor that takes in balls
        '''
        self.feed_motor = SparkMax(ball_feed_id)
        self.left_motor = SparkMax(left_id)
        self.right_motor = SparkMax(right_id)
        self.intake_motor = SparkMax(intake_id)

    def ready_to_index(self):
        '''
        Checks if the motor underneath the shooter is at maximum voltage.
        '''
        if self.feed_motor.get_percent_output() == 0.5:
            return True

    def stop_all_motors(self):
        '''
        Stops all the motors. 
        Note: It's better to use stopMotor() instead of setting the percentage to zero.
        '''
        self.feed_motor.stopMotor()
        self.left_motor.stopMotor()
        self.right_motor.stopMotor()
        self.intake_motor.stopMotor()

    def update(self, turret_at_full_speed=bool):
        '''
        This feeds balls into the shooter, starting with the feed motor. 
        When the feed motor reaches the desired output, the other motors will activate
        to push the other balls in.
        '''
        if turret_at_full_speed:
            self.feed_motor.set_percent_output(0.5)
            if self.ready_to_index():
                self.left_motor.set_percent_output(-0.5)
                self.right_roll_motor.set_percent_output(0.5)
                self.run_intake()

    def run_intake(self):
        '''
        A separate function for running the intake,
        as we will use it to both pull in balls and run with the magazine.

        This is most likely a terrible, terrible idea.
        '''
        self.intake_motor.set_percent_output(-0.5)

from .path import Path


class Autonomous:
    def __init__(self, kS, kV, trackwidth, trajectories=[]):
        '''
        Creates a controller for following a PathWeaver trajectory.

        __init__(self, kS: Volts, kV: Volts * Seconds / Meters, trackwidth: Meters, trajectories: [wpilib.trajectory.Trajectory])

        :param kS: The kS gain determined by characterizing the Robot's drivetrain
        :param kV: The kV gain determined by characterizing the Robot's drivetrain
        :param trackwidth: The horizontal distance between the left and right wheels of the tank drive.
        :param trajectories: The list of trajectories to follow. These trajectories will be followed in order from first to last.
        '''
        # Store the list of trajectories
        self.trajectories = trajectories

        # Data for following the path
        self.kS = kS
        self.kV = kV
        self.trackwidth = trackwidth

        self.reset()

    def reset(self):
        '''
        Resets the state of the Autonomous so it can be executed another time as if
        it were never executed in the first place.

        reset(self)
        '''
        # This counts the index of the current trajectory
        self.current_trajectory = -1
        self.inbetween_paths = False

        # This will be assigned when the autonomous is started
        self.path = None

    def is_paused(self):
        '''
        This method returns whether or not the robot's autonomous is paused.
        The autonomous is paused when it finishes a path segment (an individual trajectory),
        and when it's not done.

        is_paused(self) -> bool
        '''
        return self.inbetween_paths and not self.is_done()

    def resume(self, chassis, gyro):
        '''
        Resume the autonomous and start following the next path segment.

        resume(self, chassis: traits.DriveTrain, gyro: traits.Gyro)

        :param chassis: An object that implements the DriveTrain trait. This object's encoders will be reset by this function.
        :param gyro: An object that implements the Gyro trait. This object's angle will be reset by this function.
        '''
        self.current_trajectory += 1

        # If the path is done, do nothing
        if not self.is_done():
            self.inbetween_paths = False
            self.path = Path(self.kS, self.kV, self.trackwidth,
                             self.trajectories[self.current_trajectory])

            self.path.reset(chassis, gyro)

    start = resume

    def is_done(self):
        '''
        Returns whether or not the autonomous has completed all of its paths.

        is_paused(self) -> bool
        '''
        return self.current_trajectory >= len(self.trajectories)

    def update(self, chassis, gyro):
        '''
        This drives the chassis to follow the current trajectory of the autonomous

        update(self, chassis: traits.DriveTrain, gyro: traits.Gyro)

        :param chassis: An object that implements the DriveTrain trait.
        :param gyro: An object that implements the gyro trait.
        '''
        # Check to see if the user called the `resume` or `start` method first
        if not self.path or self.current_trajectory == -1:
            raise Exception(
                "You did not `start` or `resume` your Autonomous object before running it. Try calling the `start` method at the end of your `autonomousInit` method.")

        # If the individual path is done, we are now inbetween paths. (we pause here)
        if self.path.is_done():
            self.inbetween_paths = True
        else:
            # Follow the path with the chassis and gyro if the path is not done
            self.path.follow(chassis, gyro)

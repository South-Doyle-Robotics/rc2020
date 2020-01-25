from wpilib import TimedRobot, run
from traits import DriveTrain, Encoder
from controllers import DriverController
from subsystems import Chassis
from hardware import ADXRS450
from tests import ForwardDriveCheck, TurnLeftCheck, TurnRightCheck
import math
# import pathfinder as pf


@run
class Kthugdess(TimedRobot):
    MAX_VELOCITY = 2
    MAX_ACCELERATION = 3

    def robotInit(self):
        self.chassis = Chassis()
        self.gyro = ADXRS450()
        self.controller = DriverController(0)
        self.test = None
        self.chassis.reset_encoders()

    def teleopPeriodic(self):
        self.chassis.arcade_drive(-self.controller.forward(), self.controller.turn())

        if self.controller.shift():
            self.chassis.set_high_gear()
        else:
            self.chassis.set_low_gear()

    def testInit(self):
        self.test = ForwardDriveCheck(self.chassis)

    def testPeriodic(self):
        self.test.run()


# class MyRobot(wpilib.TimedRobot):
#     """Main robot class"""
#     def robotInit(self):
#         """Robot-wide initialization code should go here"""

#         self.lstick = wpilib.Joystick(0)

#         self.l_motor = wpilib.Spark(1)
#         self.r_motor = wpilib.Spark(2)

#         # Position gets automatically updated as robot moves
#         self.gyro = wpilib.AnalogGyro(1)

#         self.robot_drive = wpilib.RobotDrive(self.l_motor, self.r_motor)

#         self.l_encoder = wpilib.Encoder(0, 1)
#         self.l_encoder.setDistancePerPulse(
#             (math.pi * self.WHEEL_DIAMETER) / self.ENCODER_COUNTS_PER_REV
#         )

#         self.r_encoder = wpilib.Encoder(2, 3)
#         self.r_encoder.setDistancePerPulse(
#             (math.pi * self.WHEEL_DIAMETER) / self.ENCODER_COUNTS_PER_REV
#         )

#     def autonomousInit(self):

#         # Set up the trajectory
#         points = [pf.Waypoint(0, 0, 0), pf.Waypoint(9, 5, 0)]

#         info, trajectory = pf.generate(
#             points,
#             pf.FIT_HERMITE_CUBIC,
#             pf.SAMPLES_HIGH,
#             dt=self.getPeriod(),
#             max_velocity=self.MAX_VELOCITY,
#             max_acceleration=self.MAX_ACCELERATION,
#             max_jerk=120.0,
#         )

#         # Wheelbase Width = 2 ft
#         modifier = pf.modifiers.TankModifier(trajectory).modify(2.0)

#         # Do something with the new Trajectories...
#         left = modifier.getLeftTrajectory()
#         right = modifier.getRightTrajectory()

#         leftFollower = pf.followers.EncoderFollower(left)
#         leftFollower.configureEncoder(
#             self.l_encoder.get(), self.ENCODER_COUNTS_PER_REV, self.WHEEL_DIAMETER
#         )
#         leftFollower.configurePIDVA(1.0, 0.0, 0.0, 1 / self.MAX_VELOCITY, 0)

#         rightFollower = pf.followers.EncoderFollower(right)
#         rightFollower.configureEncoder(
#             self.r_encoder.get(), self.ENCODER_COUNTS_PER_REV, self.WHEEL_DIAMETER
#         )
#         rightFollower.configurePIDVA(1.0, 0.0, 0.0, 1 / self.MAX_VELOCITY, 0)

#         self.leftFollower = leftFollower
#         self.rightFollower = rightFollower

#         # This code renders the followed path on the field in simulation (requires pyfrc 2018.2.0+)
#         if wpilib.RobotBase.isSimulation():
#             from pyfrc.sim import get_user_renderer

#             renderer = get_user_renderer()
#             if renderer:
#                 renderer.draw_pathfinder_trajectory(
#                     left, color="#0000ff", offset=(-1, 0)
#                 )
#                 renderer.draw_pathfinder_trajectory(
#                     modifier.source, color="#00ff00", show_dt=1.0, dt_offset=0.0
#                 )
#                 renderer.draw_pathfinder_trajectory(
#                     right, color="#0000ff", offset=(1, 0)
#                 )

#     def autonomousPeriodic(self):

#         l = self.leftFollower.calculate(self.l_encoder.get())
#         r = self.rightFollower.calculate(self.r_encoder.get())

#         gyro_heading = (
#             -self.gyro.getAngle()
#         )  # Assuming the gyro is giving a value in degrees
#         desired_heading = pf.r2d(
#             self.leftFollower.getHeading()
#         )  # Should also be in degrees

#         # This is a poor man's P controller
#         angleDifference = pf.boundHalfDegrees(desired_heading - gyro_heading)
#         turn = 5 * (-1.0 / 80.0) * angleDifference

#         l = l + turn
#         r = r - turn

#         # -1 is forward, so invert both values
#         self.robot_drive.tankDrive(-l, -r)

#     def teleopPeriodic(self):
#         self.robot_drive.arcadeDrive(self.lstick)

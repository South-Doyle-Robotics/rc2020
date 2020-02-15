from os.path import dirname
from math import radians, pi
from subsystems.turret import Turret
from wpilib import Joystick, run, TimedRobot
from wpilib import TimedRobot, run
from wpilib.controller import RamseteController
from wpilib.kinematics import DifferentialDriveOdometry
from wpilib.geometry import Rotation2d, Pose2d
from wpilib.trajectory import TrajectoryUtil
from controllers import DriverController, ShooterController
from subsystems import Chassis, Turret
from hardware import ADXRS450
from tools import Timer
# from tests import ForwardDriveCheck, TurnLeftCheck, TurnRightCheck
# from subsystems.camera import Limelight


trajectory = TrajectoryUtil.fromPathweaverJson(
    dirname(__file__) + "/paths/start.wpilib.json")


@run
class Kthugdess(TimedRobot):
    def robotInit(self):
        self.chassis = Chassis()
        self.turret = Turret()
        self.gyro = ADXRS450()
        self.controller = DriverController(0)

        self.test = None
        self.chassis.reset_encoders()

        self.ramsete = RamseteController(2, 0.7)
        self.odometry = DifferentialDriveOdometry(
            Rotation2d(0), Pose2d(13, -6, Rotation2d(pi)))
        self.timer = Timer()

    def reset(self):
        self.odometry = DifferentialDriveOdometry(
            Rotation2d(0), Pose2d(13, -6, Rotation2d(pi)))
        self.chassis.play_music()
        self.gyro.reset()
        self.chassis.reset_encoders()
        self.chassis.set_low_gear()
        self.timer.start()

    teleopInit = reset
    autonomousInit = reset

    def teleopPeriodic(self):
        self.chassis.arcade_drive(-self.controller.forward(),
                                  self.controller.turn())

        if self.controller.shift():
            self.chassis.set_high_gear()
        else:
            self.chassis.set_low_gear()

    def autonomousPeriodic(self):
        ld, rd = self.chassis.get_left_distance(), self.chassis.get_right_distance()
        angle = self.gyro.get_counterclockwise_degrees()
        current_pose = self.odometry.update(
            Rotation2d(radians(angle)),
            ld, rd
        )

        target_pose = trajectory.sample(self.timer.get())

        chassis_speed = self.ramsete.calculate(current_pose, target_pose)

        wheel_speeds = drive_kinematics.toWheelSpeeds(chassis_speed)
        l, r = wheel_speeds.left, wheel_speeds.right

        self.chassis.tank_drive((kS + l*kV)/12, (kS + r*kV)/12)

    def testInit(self):
        self.test = TurnRightCheck(self.chassis, self.gyro)

    def testPeriodic(self):
        self.test.run()

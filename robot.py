from wpilib import TimedRobot, run
from wpilib.controller import RamseteController, SimpleMotorFeedforwardMeters
from wpilib.kinematics import DifferentialDriveOdometry, DifferentialDriveKinematics, ChassisSpeeds
from wpilib.geometry import Rotation2d, Pose2d, Translation2d
from wpilib.trajectory import TrajectoryGenerator, TrajectoryConfig
from wpilib.trajectory.constraint import DifferentialDriveVoltageConstraint
from traits import DriveTrain, Encoder
from controllers import DriverController
from subsystems import Chassis, Turret
from hardware import ADXRS450
from tests import ForwardDriveCheck, TurnLeftCheck, TurnRightCheck
from tools import Timer
from constants import TRACKWIDTH, kS, kV, kA
import math


drive_kinematics = DifferentialDriveKinematics(TRACKWIDTH)

trajectory_config = TrajectoryConfig(3, 4)
trajectory_config.setKinematics(drive_kinematics)
trajectory_config.addConstraint(
    DifferentialDriveVoltageConstraint(
        SimpleMotorFeedforwardMeters(kS, kV, kA),
        drive_kinematics, 12
    )
)

trajectory = TrajectoryGenerator().generateTrajectory(
    Pose2d(0, 0, Rotation2d(0)),
    [],
    Pose2d(2, 0, Rotation2d(0)),
    trajectory_config
)


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
            Rotation2d(self.gyro.get_counterclockwise_degrees()))
        self.timer = Timer()

    def teleopInit(self):
        self.chassis.set_low_gear()

    def teleopPeriodic(self):
        self.turret.update()
        self.chassis.arcade_drive(-self.controller.forward(),
                                  self.controller.turn())
        if self.controller.shift():
            self.chassis.set_high_gear()
        else:
            self.chassis.set_low_gear()

    def autonomousInit(self):
        self.chassis.stop_music()
        self.gyro.reset()
        self.chassis.reset_encoders()
        self.chassis.set_low_gear()
        self.timer.start()

    def autonomousPeriodic(self):
        ld, rd = self.chassis.get_left_distance(), self.chassis.get_right_distance()

        current_pose = self.odometry.update(
            Rotation2d(self.gyro.get_counterclockwise_degrees()),
            ld, rd
        )

        target_pose = trajectory.sample(self.timer.get())

        chassis_speed = self.ramsete.calculate(current_pose, target_pose)
        # chassis_speed = self.ramsete.calculate(current_pose, Pose2d(1, 0, Rotation2d(0)), 1, 1.5)

        wheel_speeds = drive_kinematics.toWheelSpeeds(chassis_speed)
        l, r = wheel_speeds.left, wheel_speeds.right

        self.chassis.tank_drive((kS + l*kV)/12, (kS + r*kV)/12)
        # self.chassis.tank_drive(l, r)
        # print("dist", ld, rd, "speed", l, r)

    def testInit(self):
        self.test = TurnRightCheck(self.chassis, self.gyro)

    def testPeriodic(self):
        self.test.run()

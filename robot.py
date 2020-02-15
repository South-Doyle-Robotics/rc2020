from os.path import dirname
from subsystems.turret import Turret
from wpilib import Joystick, run, TimedRobot
from wpilib import TimedRobot, run
from controllers import DriverController, ShooterController
from subsystems import Chassis, Turret, PathfinderController
from hardware import ADXRS450
from tools import Timer
from constants import kS, kV, TRACKWIDTH
from wpilib.trajectory import TrajectoryUtil
# from tests import ForwardDriveCheck, TurnLeftCheck, TurnRightCheck
# from subsystems.camera import Limelight


start = TrajectoryUtil.fromPathweaverJson(
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
        self.pf = PathfinderController(kS, kV, TRACKWIDTH, 13, -6, 180)

    def reset(self):
        self.pf.reset(self.chassis, self.gyro)
        self.pf.set_trajectory(start)

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
        self.pf.update(self.chassis, self.gyro)

    def testInit(self):
        self.test = TurnRightCheck(self.chassis, self.gyro)

    def testPeriodic(self):
        self.test.run()

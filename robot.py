from os.path import dirname
from wpilib import Joystick, run, TimedRobot
from wpilib import TimedRobot, run
from controllers import DriverController, ShooterController
from subsystems import Chassis, Turret, PathfinderController, Singulator
from hardware import ADXRS450
from tools import Timer
from constants import kS, kV, TRACKWIDTH, TURRET_SHOOT_MOTORS
from wpilib.trajectory import TrajectoryUtil
# from tests import ForwardDriveCheck, TurnLeftCheck, TurnRightCheck


start = TrajectoryUtil.fromPathweaverJson(
    dirname(__file__) + "/paths/citrus.wpilib.json")


@run
class Kthugdess(TimedRobot):
    def robotInit(self):
        self.chassis = Chassis()
        self.turret = Turret()
        self.gyro = ADXRS450()
        # self.singulator = Singulator()  # Add it in when it's ready! Also, don't forget the CAN ids.
        self.controller = DriverController(0)

        self.test = None
        self.chassis.reset_encoders()
        self.pf = PathfinderController(kS, kV, TRACKWIDTH, 13, -2.5, 180)

    def reset(self):
        self.pf.reset(self.chassis, self.gyro)
        self.pf.set_trajectory(start)

    teleopInit = reset
    autonomousInit = reset

    def teleopPeriodic(self):
        self.chassis.arcade_drive(-self.controller.forward(),
                                  self.controller.turn())

        if self.controller.shoot():
            self.turret.run_shooter()
        #   self.singulator.update(self.turret.at_full_speed())
        # else:
        #   self.turret.stop_shooting()
        #   self.singulator.stop_all_motors()

        # if self.controller.intake():
        #     self.singulator.run_intake()

        # No need to put in an else because we will get all the balls and then stop all motors after shooting.

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

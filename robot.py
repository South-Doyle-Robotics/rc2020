from wpilib import TimedRobot, run
from traits import DriveTrain, Encoder
from controllers import DriverController
from subsystems import Chassis
from hardware import ADXRS450
from tests import ForwardDriveCheck, TurnLeftCheck, TurnRightCheck

@run
class Kthugdess(TimedRobot):
    def robotInit(self):
        self.chassis = Chassis()
        self.controller = DriverController(0)
        self.test = None

    def teleopPeriodic(self):
        self.chassis.arcade_drive(self.controller.forward(), self.controller.turn())

    def testInit(self):
        self.test = ForwardDriveCheck(self.chassis)

    def testPeriodic(self):
        self.test.run()

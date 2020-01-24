from wpilib import TimedRobot, run
from controllers import Xbox
from traits import DriveTrain
from subsystems import Chassis


@run
class Kthugdess(TimedRobot):
    def robotInit(self):
        self.chassis = Chassis()
        self.controller = Xbox(0)

    def teleopPeriodic(self):
        self.chassis.arcade_drive(self.controller.forward(), self.controller.turn())
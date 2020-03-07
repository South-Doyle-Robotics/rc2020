
from os.path import dirname, basename
from subsystems.turret import Turret
from wpilib import Joystick, run, TimedRobot
from wpilib import TimedRobot, run
from controllers import DriverController, ShooterController
from subsystems import Chassis, Turret, Autonomous
from hardware import ADXRS450
from tools import Timer
from constants import kS, kV, TRACKWIDTH
from wpilib.trajectory import TrajectoryUtil
from glob import glob as files


filenames = files(dirname(__file__) + "/paths/*.json")
try:
    filenames.sort(key=lambda filename: int(basename(filename).split(".")[0]))
except:
    raise Exception(
        "Files in `path` folder MUST follow 'INTEGER.*.json' pattern, where `INTEGER` is any integer value")
print("Path filenames are:", filenames)
trajectories = list(
    map(TrajectoryUtil.fromPathweaverJson, filenames))


@run
class Kthugdess(TimedRobot):
    def robotInit(self):
        self.chassis = Chassis()
        self.turret = Turret()
        self.gyro = ADXRS450()
        self.controller = DriverController(0)

        self.test = None
        self.chassis.reset_encoders()

        self.auto = Autonomous(kS, kV, TRACKWIDTH, trajectories)

        self.reset()

    def reset(self):
        self.auto.reset()
        self.auto.start(self.chassis, self.gyro)

    autonomousInit = reset
    teleopInit = reset

    def autonomousPeriodic(self):
        if self.auto.is_paused():
            print("SHOOT")
            self.auto.resume(self.chassis, self.gyro)
        elif not self.auto.is_done():
            self.auto.update(self.chassis, self.gyro)

    def teleopPeriodic(self):
        self.chassis.arcade_drive(-self.controller.forward(),
                                  self.controller.turn())

        if self.controller.shift():
            self.chassis.set_high_gear()
        else:
            self.chassis.set_low_gear()

    def testInit(self):
        self.test = TurnRightCheck(self.chassis, self.gyro)

    def testPeriodic(self):
        self.test.run()

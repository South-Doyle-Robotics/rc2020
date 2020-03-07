
from os.path import dirname, basename
from subsystems.turret import Turret
from wpilib import Joystick, run, TimedRobot
from wpilib import TimedRobot, run
from controllers import DriverController, ShooterController
from subsystems import Chassis, Turret, Autonomous, Magazine
from hardware import ADXRS450
from tools import Timer
from constants import kS, kV, TRACKWIDTH, TURRET_SHOOT_MOTORS
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
        # self.chassis = Chassis()
        self.turret = Turret()
        # self.gyro = ADXRS450()
        # Add it in when it's ready! Also, don't forget the CAN ids.
        # self.mag = Magazine()
        self.controller = DriverController(0)

    #     self.test = None
    #     self.chassis.reset_encoders()

    #     self.auto = Autonomous(kS, kV, TRACKWIDTH, trajectories)

    #     self.reset()

    # def reset(self):
    #     self.auto.reset()
    #     self.auto.start(self.chassis, self.gyro)

    # autonomousInit = reset
    # teleopInit = reset

    # def autonomousPeriodic(self):
    #     if self.auto.is_paused():
    #         print("SHOOT")
    #         self.auto.resume(self.chassis, self.gyro)
    #     elif not self.auto.is_done():
    #         self.auto.update(self.chassis, self.gyro)

    def teleopPeriodic(self):
        # self.chassis.arcade_drive(-self.controller.forward(),
        #                           self.controller.turn())

        self.turret.update()

        # if self.controller.shoot():
        #     self.turret.shoot()
        # else:
        #     self.turret.idle()

        #     self.singulator.update(self.turret.at_full_speed())
        # else:
        #     self.turret.stop_shooting()
        #     self.singulator.stop_all_motors()

        # if self.controller.intake():
        #     self.singulator.run_intake()

        # No need to put in an else because we will get all the balls and then stop all motors after shooting.

        '''if self.controller.shift():
            self.chassis.set_high_gear()
        else:
            self.chassis.set_low_gear()'''

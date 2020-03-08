from math import copysign
from os.path import dirname, basename
from subsystems.turret import Turret
from wpilib import Joystick, run, TimedRobot
from wpilib import TimedRobot, run
from controllers import DriverController, ShooterController
from subsystems import Chassis, Turret, Autonomous, Magazine, Intake
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
        self.chassis = Chassis()
        self.turret = Turret()
        self.gyro = ADXRS450()
        self.intake = Intake()
        self.mag = Magazine()
        self.controller = DriverController(0)
        self.chassis.reset_encoders()

        self.auto = Autonomous(kS, kV, TRACKWIDTH, trajectories)

        self.reset()

    def reset(self):
        self.turret.reset()
        self.auto.reset()
        self.auto.start(self.chassis, self.gyro)

    autonomousInit = reset
    teleopInit = reset

    def autonomousPeriodic(self):
        self.turret.zero()
        if self.auto.is_paused():
            self.auto.resume(self.chassis, self.gyro)
        elif not self.auto.is_done():
            self.auto.update(self.chassis, self.gyro)

    def teleopPeriodic(self):
        self.turret.zero()
        if self.controller.intake():
            # self.intake.intake()
            self.mag.intake()
        else:
            # self.intake.idle()
            self.shoot(self.controller.shoot())

        if self.controller.shift():
            self.chassis.set_high_gear()
        else:
            self.chassis.set_low_gear()

        forward = self.controller.forward()
        turn = self.controller.turn()
        self.chassis.arcade_drive(-copysign(abs(forward) ** 1.15, forward),
                                  copysign(abs(turn) ** 1.15, turn))

        # self.turret.goto_angle(self.turret.HOME_ANGLE)
        # print("cw", self.turret.clockwise_limit_switch.get(),
        #       "ccw", self.turret.counterclockwise_limit_switch.get())

    def shoot(self, shoot):
        if shoot:
            self.turret.shoot()
            self.turret.stop_turning()
            if self.turret.is_full_speed() and self.mag.is_ready():
                self.mag.dump()
            elif self.turret.is_full_speed():
                self.mag.agitate()
        else:
            self.turret.track_limelight()
            self.turret.idle()
            self.mag.stop()

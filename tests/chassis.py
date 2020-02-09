from traits import DriveTrain, Gyro
from . import Test


class ForwardDriveCheck(Test):
    '''
    This checks that the drivetrain encoders have the proper polarity
    '''
    def testStart(self, chassis):
        print("Test begin")
        self.chassis = chassis

        if not chassis.implements(DriveTrain):
            raise Exception("Must use this test on an object that implements the DriveTrain trait")

        chassis.reset_encoders()

    def testPeriodic(self):
        self.chassis.tank_drive(0.35, 0.35)

    def testEnd(self):
        l = self.chassis.get_left_distance()
        r = self.chassis.get_right_distance()

        if l < 0:
            raise Exception("Left encoder returned a negative distance after commanding positive speed")

        if r < 0:
            raise Exception("Right encoder returned a negative distance after commanding positive speed")

        self.chassis.tank_drive(0, 0)
        print("Test passed!")
        print("Left encoder distance:", l)
        print("Right encoder distance:", r)

class TurnRightCheck(Test):
    '''
    This checks that the drivetrain encoders and the gyro have the proper polarity
    '''
    def testStart(self, chassis, gyro):
        self.chassis = chassis
        self.gyro = gyro

        if not chassis.implements(DriveTrain):
            raise Exception("Must use this test on an object that implements the DriveTrain trait")

        if not gyro.implements(Gyro):
            raise Exception("Must use this test on an object that implements the Gyro trait")

        chassis.reset_encoders()
        gyro.reset()

    def testPeriodic(self):
        self.chassis.tank_drive(0.35, -0.35)

    def testEnd(self):
        heading = self.gyro.get_clockwise_degrees()
        l = self.chassis.get_left_distance()
        r = self.chassis.get_right_distance()

        if l < 0:
            raise Exception("Left encoder returned a negative distance after commanding positive speed")

        if r > 0:
            raise Exception("Right encoder returned a positive distance after commanding negative speed")

        if heading < 0:
            raise Exception("Robot turned right, but the gyro read the turned angle as " + str(heading) + " degrees")

        self.chassis.tank_drive(0, 0)
        print("Test passed!")
        print("Gyro heading:", heading)
        print("Left encoder distance:", l)
        print("Right encoder distance:", r)


class TurnLeftCheck(Test):
    '''
    This checks that the drivetrain encoders and the gyro have the proper polarity
    '''
    def testStart(self, chassis, gyro):
        self.chassis = chassis
        self.gyro = gyro

        if not chassis.implements(DriveTrain):
            raise Exception("Must use this test on an object that implements the DriveTrain trait")

        if not gyro.implements(Gyro):
            raise Exception("Must use this test on an object that implements the Gyro trait")

        chassis.reset_encoders()
        gyro.reset()

    def testPeriodic(self):
        self.chassis.tank_drive(-0.35, 0.35)

    def testEnd(self):
        heading = self.gyro.get_clockwise_degrees()
        l = self.chassis.get_left_distance()
        r = self.chassis.get_right_distance()

        if l > 0:
            raise Exception("Left encoder returned a positive distance after commanding negative speed")

        if r < 0:
            raise Exception("Right encoder returned a negative distance after commanding positive speed")

        if heading > 0:
            raise Exception("Robot turned left, but the gyro read the turned angle as " + str(heading) + " degrees")

        self.chassis.tank_drive(0, 0)
        print("Test passed!")
        print("Gyro heading:", heading)
        print("Left encoder distance:", l)
        print("Right encoder distance:", r)
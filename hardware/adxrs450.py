from traits import implements, Gyro
from wpilib import ADXRS450_Gyro

@implements(Gyro)
class ADXRS450:
    def __init__(self):
        self.gyro = ADXRS450_Gyro()
        self.reset()

    def reset(self):
        self.gyro.reset()
    
    def get_clockwise_degrees(self):
        heading = self.gyro.getAngle()
        while heading < -180: heading += 360
        while heading >  180: heading -= 360
        return heading
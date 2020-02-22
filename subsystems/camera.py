from networktables import NetworkTables

NetworkTables.initialize()


class Limelight:
    '''
    Responsible for interacting with the Limelight over NetworkTables.

    Used for getting the hexagonal target's position in 3d space
    '''

    MAX_VERTICAL_DEGREES = 24.85
    MAX_HORIZONTAL_DEGREES = 29.8

    def __init__(self):
        self.table = NetworkTables.getTable("limelight")

    def has_target(self):
        '''
        If there is a target, this will output 1. Otherwise, it will return 0.
        '''
        return bool(self.table.getNumber("tv", 0.0))

    def get_target(self):
        '''
        If the limelight sees a target, this will return a Target object
        with the three dimensional position and euler angles of the target.

        Otherwise, this will return None
        '''
        if self.has_target():
            positions = self.table.getNumberArray(
                "camtran", [0, 0, 0, 0, 0, 0])
            return Target(*positions)
        else:
            return None

    def get_target_screen_x(self):
        '''
        This represents the horizontal position of the target
        relative to the crosshair on the limelight.

        Ranges from -1 to 1
        '''
        return self.table.getNumber("tx", 0.0) / MAX_HORIZONTAL_DEGREES

    def get_target_screen_y(self):
        '''
        This represents the vertical position of the target
        relative to the crosshair on the limelight.

        Ranges from -1 to 1
        '''
        return self.table.getNumber("ty", 0.0) / MAX_VERTICAL_DEGREES


class Target:
    '''
    Represents a target in three dimensional space 
    '''

    def __init__(self, x, y, z, yaw, pitch, roll):
        '''
        Creates a target object with the given data
        '''
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll

    def get_x(self): return self.x
    def get_y(self): return self.y
    def get_z(self): return self.z
    def get_yaw(self): return self.yaw

from rev.color import ColorSensorV3


class ColorSensor(ColorSensorV3):
    '''
    The object responsible for managing the color sensor
    '''

    def detect_color(self): return super().getColor()

    def detect_proximity_from_wheel(self):
        '''
        Color detection works best at approximately 2 inches from the color wheel.
        '''
        return super().getProximity()

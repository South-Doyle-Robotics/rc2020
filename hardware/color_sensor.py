from rev.color import ColorMatch, ColorSensorV3, CIEColor


class ColorSensor(ColorSensorV3):
    '''
    The object responsible for managing the color sensor
    '''

    def detect_color(self):
        return super().getColor()

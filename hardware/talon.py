from ctre import WPI_TalonFX, FeedbackDevice, SupplyCurrentLimitConfiguration
from traits import Motor, Encoder, implements
from tools import Timed


@implements(Encoder, Motor)
class Falcon(WPI_TalonFX, Timed):
    def __init__(self, can_id):
        super().__init__(can_id)
        self.configSelectedFeedbackSensor(FeedbackDevice.IntegratedSensor)
        # Voltage compensation guarantees that pathfinder will work properly
        self.configVoltageCompSaturation(12, 100)
        self.enableVoltageCompensation(True)
        # Initialize the encoder to zero
        self.reset()

    def set_percent_output(self, percent):
        super().set(percent)

    def get_percent_output(self):
        return super().get()

    get_pulses = Encoder.get_pulses
    get_revolutions = Encoder.get_revolutions

    def get_counts(self):
        return self.getSelectedSensorPosition()

    def get_counts_per_revolution(self):
        return 2048

    def reset(self):
        self.setSelectedSensorPosition(0)

    def delayed_set_percent_output(self, percent, seconds):
        self.do(
            self.set_percent_output,
            seconds,
            percent
        )

    def set_current_limit(self, amps):
        self.configSupplyCurrentLimit(
            SupplyCurrentLimitConfiguration(True, 0, amps, 0.5)
        )

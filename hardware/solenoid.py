from wpilib import DoubleSolenoid as WPI_DoubleSolenoid, Compressor

class DoubleSolenoid(WPI_DoubleSolenoid):
    def __init__(self, pcm_id, forward_channel, reverse_channel):
        super().__init__(pcm_id, forward_channel, reverse_channel)
        Compressor(pcm_id)
    
    def forward(self):
        self.set(self.Value.kForward)
    
    def reverse(self):
        self.set(self.Value.kReverse)
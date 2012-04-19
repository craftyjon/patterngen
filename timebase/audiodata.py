class AudioData:
    """Holds information about a set of sampled audio data--beats, features, FFT, waveform, etc...  Passed to presets for their use."""
    def __init__(self):
        self.is_beat = False    # For now, let's try quantizing beat detection to the processing frame rate (30 FPS).  This should be OK for lighting...
        self.duration = 0.0
        self.waveform = []
        self.fft = []
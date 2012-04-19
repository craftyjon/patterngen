import copy

from audiodata import AudioData

class Timebase:
    def __init__(self):
        self.audio_data = AudioData()

    def get_data(self):
        c = copy.deepcopy(self.audio_data)
        self.audio_data = AudioData()
        return c
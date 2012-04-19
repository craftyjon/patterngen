from threading import Timer

from timebase import Timebase
from audiodata import AudioData

class Metronome(Timebase):
    def __init__(self, callback):
        Timebase.__init__(self)
        self.interval = 0.5
        self.callback = callback
        self.timer = Timer(self.interval, self.on_tick)
        self.timer.daemon = True
        self.running = False

    def start(self):
        self.running = True
        self.timer = Timer(self.interval, self.on_tick)
        self.timer.start()

    def stop(self):
        self.running = False
        if self.timer is not None:
            self.timer.cancel()
            self.timer.join()

    def toggle(self):
        if self.running:
            self.stop()
        else:
            self.start()

    def is_beat(self):
        if self.audio_data.is_beat:
            self.audio_data.is_beat = False
            return True
        else:
            return False

    def inject_beat(self):
        self.audio_data.is_beat = True

    def on_tick(self):
        #self.callback(self.interval)
        self.audio_data.is_beat = True
        if self.running:
            self.timer = Timer(self.interval, self.on_tick)
            self.timer.daemon = True
            self.timer.start()
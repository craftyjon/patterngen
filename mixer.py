import numpy as np
from threading import Timer
import inspect
import time

from frame import Frame
from timebase.audiodata import AudioData
import presets

class Mixer:
    def __init__(self, size=(24,24)):
        self.size = size
        self.frame = Frame(size)
        self.presets = []
        self.timebase = None
        self.draw_interval = 0.005
        self.draw_timer = Timer(self.draw_interval, self.on_tick)
        self.draw_timer.daemon = True
        self.active_preset = 0
        self.next_preset = 1
        self.loaded_preset = 1
        self.running = False
        self.paused = False
        self.blacked_out = False
        self.hard_cut = False
        self.in_transition = False
        self.preset_time = 8.0
        self.transition_time = 1.25
        self.transition_state = 0.0
        self.preset_runtime = 0.0
        self.time = 0.0
        self.last_time = 0.0
        self.time_delta = 0.0
        self.tick_callback = None


        #TODO: Make this less magical -- maybe a config file or sqlite DB for presets?
        for name,obj in inspect.getmembers(presets, inspect.isclass):
            #try:
            self.presets.append(obj(self.size))
            #except:
            #    print str(e)
            #    print "Error loading preset "+name+"!"

    def run(self):
        if self.paused:
            self.paused = False
            self.timebase.start()
            return
        self.last_time = time.time()
        self.draw_timer.start()
        self.running = True
        if self.timebase is not None:
            self.timebase.start()

    def stop(self):
        self.running = False
        if self.draw_timer is not None:
            self.draw_timer.cancel()
            self.draw_timer.join()
        self.timebase.stop()

    def pause(self):
        self.timebase.stop()
        self.preset_runtime = 0.0
        self.paused = True

    def set_tick_callback(self, cb):
        self.tick_callback = cb

    def on_tick(self):
        if not self.running:
            return False

        if not self.paused:
            audio_data = self.timebase.get_data()
            self.time_delta = time.time() - self.last_time
            self.last_time = time.time()
            if self.preset_runtime >= self.preset_time:
                self.preset_runtime = 0.0
                self.next()

            if self.in_transition:
                if self.hard_cut is True and audio_data.is_beat is True:
                    self.cut(1)
                    self.presets[self.active_preset].tick(self.time_delta, audio_data)
                else:
                    if audio_data.is_beat is True or self.transition_state > 0.0:    #delay start until beat
                        self.transition_state += self.time_delta
                        if self.transition_state >= self.transition_time:
                            self.in_transition = False
                            t = self.active_preset
                            self.active_preset = self.next_preset
                            self.next_preset = t
                    self.presets[self.active_preset].tick(self.time_delta, audio_data)
                    self.presets[self.next_preset].tick(self.time_delta, audio_data)
            else:
                self.preset_runtime += self.time_delta
                self.presets[self.active_preset].tick(self.time_delta, audio_data)

        self.draw()

        if self.tick_callback is not None:
            self.tick_callback(self)

        self.draw_timer = Timer(self.draw_interval, self.on_tick).start()

    def set_timebase(self, timebase):
        self.timebase = timebase(None)
        

    def toggle_paused(self):
        self.paused = not self.paused

    def draw(self):
        if self.blacked_out:
            self.frame = Frame(self.size)
        else:
            if self.in_transition is True:
                oldframe = self.presets[self.active_preset].get_frame() * (1.0 - (self.transition_state/self.transition_time))
                newframe = self.presets[self.next_preset].get_frame() * (self.transition_state/self.transition_time)
                self.frame = oldframe + newframe
            else:
                self.frame = self.presets[self.active_preset].get_frame()

    def next(self):
        if self.in_transition or self.paused or len(self.presets) < 2:
            return False
        self.next_preset = (self.active_preset + 1) % len(self.presets)
        self.in_transition = True
        self.transition_state = 0.0

    def prev(self):
        if self.in_transition or self.paused or len(self.presets) < 2:
            return False
        self.next_preset = (self.active_preset - 1)
        if self.next_preset < 0:
            self.next_preset = len(self.presets) - 1
        self.in_transition = True
        self.transition_state = 0.0

    def cut(self, delta):
        self.active_preset = (self.active_preset + delta) % len(self.presets)
        self.in_transition = False
        self.preset_runtime = 0.0

    def get_frame(self):
        return self.frame

    def get_preset_name(self):
        if self.in_transition:
            return self.presets[self.next_preset].__class__.__name__
        else:
            return self.presets[self.active_preset].__class__.__name__

    def blackout(self):
        self.blacked_out = not self.blacked_out
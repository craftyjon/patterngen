# import numpy as np
from threading import Timer
# import inspect
import sqlite3
import time
import copy
import logging

from frame import Frame
# from timebase.audiodata import AudioData
import presets

log = logging.getLogger('root')
log.setLevel(logging.INFO)


class Mixer:
    def __init__(self, size=(24, 24)):
        self.size = size
        self.frame = Frame(size)
        self.presets = []

        self.timebase = None
        self.draw_interval = 0.005
        self.draw_timer = Timer(self.draw_interval, self.on_tick)
        self.draw_timer.daemon = True

        #new preset stuff (database branch)
        self.preset_list = {}
        self.current_preset_index = 0
        self.current_preset_obj = None
        self.next_preset_obj = None

        self.active_preset = 0
        self.next_preset = 1
        self.loaded_preset = 1
        self.running = False
        self.paused = False
        self.blacked_out = False
        self.hard_cut = False
        self.in_transition = False
        self.preset_time = 3.0
        self.transition_time = 1.0
        self.transition_state = 0.0
        self.preset_runtime = 0.0
        self.time = 0.0
        self.last_time = 0.0
        self.time_delta = 0.0
        self.tick_callback = None
        self.con = None
        self.cur = None

        self.load_preset_db()
        self.current_preset_obj = getattr(presets, self.preset_list[0]['classname'])(self.size)

    def connect_db(self):
        try:
            self.con = sqlite3.connect('presets.db')
            self.con.row_factory = sqlite3.Row
            self.cur = self.con.cursor()
        except sqlite3.Error, e:
            log.error("Sqlite Error: %s" % e.args[0])
            if self.con:
                self.con.close()
        log.info("Connected to database")

    def load_preset_db(self):
        """Loads the preset information from the database, so that the threaded routines don't have to make DB calls."""
        # Make sure to call this again from the main thread when the DB is updated (via RPC ping?)
        if not self.con:
            self.connect_db()
        try:
            self.cur.execute("select * from presets")
            preset_rows = self.cur.fetchall()
        except sqlite3.Error, e:
            log.warn("Could not fetch presets: %s" % e.args[0])
            return False
        self.preset_list = {}
        for preset_row in preset_rows:
            self.preset_list[preset_row['idx']] = {'classname': preset_row['classname'], 'active': preset_row['active']}

    def reorder_presets(self, order_dict):
        """Expects a list of tuples in form [(classname, index), ...]"""
        pass

    def activate_preset(self, active=True):
        """Activates or deactivates a preset"""
        pass

    def get_next_preset(self, delta=1):
        # Pick the next index
        while True:
            index = self.current_preset_index + delta
            if index > len(self.preset_list) - 1:
                index = 0
            if index < 0:
                index = len(self.preset_list) - 1
            if index in self.preset_list.keys():
                if self.preset_list[index]['active']:
                    log.info("Current index: %d, next index: %d" % (self.current_preset_index, index))
                    break
                else:
                    index += delta
            else:
                log.error("Could not pick a next index for %d (last try: %d)" % (self.current_preset_index, index))
                break

        try:
            log.info("Loading preset %s (index %d)" % (self.preset_list[index]['classname'], index))
            obj = getattr(presets, self.preset_list[index]['classname'])
        except:
            log.error("Could not load preset %s" % self.preset_list[index]['classname'])
        self.current_preset_index = index
        return obj(self.size)

    def get_prev_preset(self):
        return self.get_next_preset(-1)

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
                    self.current_preset_obj.tick(self.time_delta, audio_data)
                else:
                    if audio_data.is_beat is True or self.transition_state > 0.0:    # delay start until beat
                        self.transition_state += self.time_delta
                        if self.transition_state >= self.transition_time:
                            self.current_preset_obj = copy.deepcopy(self.next_preset_obj)
                            self.in_transition = False
                    self.current_preset_obj.tick(self.time_delta, audio_data)
                    self.next_preset_obj.tick(self.time_delta, audio_data)
            else:
                self.preset_runtime += self.time_delta
                self.current_preset_obj.tick(self.time_delta, audio_data)

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
                oldframe = self.current_preset_obj.get_frame() * (1.0 - (self.transition_state / self.transition_time))
                newframe = self.next_preset_obj.get_frame() * (self.transition_state / self.transition_time)
                self.frame = oldframe + newframe
            else:
                self.frame = self.current_preset_obj.get_frame()

    def next(self):
        if self.in_transition or self.paused or len(self.preset_list) < 2:
            return False

        self.next_preset_obj = self.get_next_preset()
        self.in_transition = True
        self.transition_state = 0.0

    def prev(self):
        if self.in_transition or self.paused or len(self.preset_list) < 2:
            return False
        self.next_preset_obj = self.get_prev_preset()
        self.in_transition = True
        self.transition_state = 0.0

    def cut(self, delta):
        if delta:
            self.next()
            self.transition_state = 1.0
        else:
            self.prev()
            self.transition_state = 1.0

    def get_frame(self):
        return self.frame

    def get_preset_name(self):
        if self.in_transition:
            return self.next_preset_obj.__class__.__name__
        else:
            return self.current_preset_obj.__class__.__name__

    def blackout(self):
        self.blacked_out = not self.blacked_out

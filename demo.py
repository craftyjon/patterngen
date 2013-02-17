import pygame
import sys
from pygame.locals import *
from array import array
import zmq
import time
import struct
import serial
import logging as log

from message import *
from timebase.metronome import Metronome
#from timebase.beatdetector import BeatDetector
from mixer import Mixer
from outputmap import OutputMap

idx = 0
enable_graphics = True


def send_command(cmd, data):
    global ser
    l = len(data)
    checksum = 0
    for member in data:
        checksum ^= member
    data += [checksum]
    packet = [0x99, 0x00, cmd] + [l & 0xFF, (l & 0xFF00) >> 1] + data

    #print "send_command: ", [hex(c) for c in packet]
    buf = "".join([struct.pack('B', char) for char in packet])
    ser.write(buf)
    ser.flushInput()
    return True


def serial_update(mixer_context):
    global ser, outmap
    data = list(outmap.map(mixer_context.frame))

    strand1 = data[:len(data) / 2]
    strand2 = data[len(data) / 2:]

    checksum = 0
    for member in strand1:
        checksum ^= member

    strand1 += [checksum]
    packet = [0x99, 0x01, 0x10, 0xE0, 0x01] + strand1
   # print data

    buf = "".join([struct.pack('B', char) for char in packet])

    ser.write(buf)
    ser.flushInput()

    checksum = 0
    for member in strand2:
        checksum ^= member

    strand2 += [checksum]
    packet = [0x99, 0x02, 0x10, 0xE0, 0x01] + strand2
   # print data

    buf = "".join([struct.pack('B', char) for char in packet])

    ser.write(buf)
    ser.flushInput()


def demo_update(mixer_context):
    global ser
    e = pygame.event.Event(pygame.USEREVENT, {'code': 0})
    if ser is not None:
        serial_update(mixer_context)
    if not pygame.event.peek(pygame.USEREVENT):
        pygame.event.post(e)


def send_status():
    global mixer, socket
    status = {'running': not mixer.paused,
                'blacked_out': mixer.blacked_out,
                'timebase_running': mixer.timebase.running,
                'current_preset': mixer.get_preset_name()
                }
    socket.send_json(status)

if __name__ == "__main__":
    pygame.init()

    size = width, height = 336, 320
    screen = pygame.display.set_mode(size)
    pygame.event.set_allowed([QUIT, KEYDOWN, USEREVENT])

    s = pygame.Surface((32, 32))
    sc = pygame.Surface((320, 320))

    outmap = OutputMap()
    outmap.outputs = [[i, [(i / 2) % 32, i % 32]] for i in range(32 * 10)]
    #print outmap.outputs

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.connect("tcp://127.0.0.101:5443")

    try:
        ser = serial.Serial('/dev/ttyACM0', 2000000, timeout=2)

        #buf = "".join([struct.pack('B', char) for char in [0x99, 0x13, 0x03, 0x00, 0x33, 0x11, 0x00, 0x22]])
        #ser.write(buf)
    except:
        log.warn("Could not open serial port")
        ser = None

    #send_command(0x15, [0x40])

    mixer = Mixer((32, 32))
    mixer.set_timebase(Metronome)
    #mixer.set_timebase(BeatDetector)

    if ser:
        mixer.set_tick_callback(demo_update)

    mixer.run()

    pygame.surfarray.blit_array(s, mixer.get_frame().buffer)
    sc = pygame.transform.smoothscale(s, (320, 320))
    screen.blit(sc, sc.get_rect())
    screen.blit(s, (320, 0))
    pygame.display.flip()

    while True:
        try:
            msg = None
            msg = socket.recv_json(flags=zmq.NOBLOCK)
        except:
            pass

        if msg is not None:
            log.info("RPC: ", msg)
            if msg['cmd'] == MSG_START:
                mixer.run()
                send_status()
            if msg['cmd'] == MSG_STOP:
                mixer.stop()
                send_status()
            if msg['cmd'] == MSG_BLACKOUT:
                mixer.blackout()
                send_status()
            if msg['cmd'] == MSG_GET_STATUS:
                send_status()
            if msg['cmd'] == MSG_PRESET_NEXT:
                mixer.next()
                send_status()
            if msg['cmd'] == MSG_PRESET_PREV:
                mixer.prev()
                send_status()
            if msg['cmd'] == MSG_PLAYPAUSE:
                if not mixer.paused:
                    mixer.pause()
                else:
                    mixer.run()
                send_status()

        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            mixer.stop()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PERIOD:
                mixer.timebase.inject_beat()
            if event.key == pygame.K_BACKSLASH:
                mixer.timebase.toggle()
            if event.key == pygame.K_SPACE:
                mixer.next()
            if event.key == pygame.K_RIGHT:
                mixer.cut(1)
            if event.key == pygame.K_LEFT:
                mixer.cut(-1)
            if event.key == pygame.K_COMMA:
                mixer.toggle_paused()
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                mixer.stop()
                sys.exit()

        if enable_graphics:
            if event.type == pygame.USEREVENT:
                try:
                    pygame.surfarray.blit_array(s, mixer.get_frame().buffer)
                except:
                    mixer.stop()
                    sys.exit()

            sc = pygame.transform.smoothscale(s, (320, 320))
            screen.blit(sc, sc.get_rect())
            screen.blit(s, (320, 0))
            pygame.display.flip()

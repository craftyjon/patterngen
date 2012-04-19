from bottle import get, post, route, run, static_file, template
import paste
import time
import zmq
import sqlite3
import logging as log

from message import *

#log = logging.getLogger('server')
#log.setLevel(logging.DEBUG)

def send_msg(msg, timeout=100):
    global socket
    reply = None
    try:
        socket.send_json(msg, flags=zmq.NOBLOCK)
        if socket.poll(timeout=timeout) != 0:
            try:
                reply = socket.recv_json(flags=zmq.NOBLOCK)
            except:
                log.warn("Could not receive reply")
        else:
            log.warn("Timeout while waiting for reply")
    except:
        log.warn("Could not send command.  Trying to reopen socket...")
        #Try a reconnect
        socket = context.socket(zmq.REQ)
        try:
            socket.bind("tcp://127.0.0.101:5443")
        except:
            log.error("Could not open socket")
    return reply

@route('/')
def index():
    global preset_rows

    status = send_msg({'cmd':MSG_GET_STATUS}) or {'current_preset':'None'}
    return template('web/templates/base.tpl', {'current_preset':status['current_preset'], 'preset_rows':preset_rows})

@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='web/static')


@route('/rpc/start')
def rpc_start():
    status = send_msg({'cmd':MSG_START})
    if status is not None:
        return status
    else:
        return "Error"

@route('/rpc/stop')
def rpc_stop():
    status = send_msg({'cmd':MSG_STOP})
    if status is not None:
        return status
    else:
        return "Error"

@route('/rpc/blackout')
def rpc_blackout():
    status = send_msg({'cmd':MSG_BLACKOUT})
    if status is not None:
        return status
    else:
        return "Error"

@route('/rpc/playpause')
def rpc_blackout():
    status = send_msg({'cmd':MSG_PLAYPAUSE})
    if status is not None:
        return status
    else:
        return "Error"

@get('/rpc/status')
def rpc_status():
    status = send_msg({'cmd':MSG_GET_STATUS})
    if status is not None:
        return status
    else:
        return "Error"

@get('/rpc/next')
def rpc_status():
    status = send_msg({'cmd':MSG_PRESET_NEXT})
    if status is not None:
        return status
    else:
        return "Error"

@get('/rpc/prev')
def rpc_status():
    status = send_msg({'cmd':MSG_PRESET_PREV})
    if status is not None:
        return status
    else:
        return "Error"

if __name__=="__main__":
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    try:
        socket.bind("tcp://127.0.0.101:5443")
    except:
        print "Could not open socket"

    try:
        con = sqlite3.connect('presets.db')
        cur = con.cursor()
        con.row_factory = sqlite3.Row
    except sqlite3.Error, e:
        log.error("Sqlite Error: %s" % e.args[0])
        if con:
            con.close()

    preset_rows = None
    if con:
        cur.execute("select * from presets")
        preset_rows = cur.fetchall()

    print preset_rows

    run()#reloader=True)
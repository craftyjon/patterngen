from bottle import get, post, route, run, static_file, template
import paste
import time
import zmq
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
				log.error("Could not receive reply")
		else:
			log.error("Timeout while waiting for reply")
	except:
		log.error("Could not send command.  Is the socket open?")
	return reply

@route('/')
def index():
	status = send_msg({'cmd':MSG_GET_STATUS}) or {'current_preset':'None'}
	return template('web/templates/base.tpl', {'current_preset':status['current_preset']})

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

	run()#reloader=True)
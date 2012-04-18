from bottle import route, run
import paste
import time
import zmq

from message import *

@route('/')
def index():
	rpc_blackout()
	return 'test'

@route('/rpc/start')
def rpc_start():
	global socket
	try:
		socket.send_pyobj(Message().autoload(MSG_START), flags=zmq.NOBLOCK)
	except:
		print "Error sending"

@route('/rpc/stop')
def rpc_stop():
	global socket
	try:
		socket.send_pyobj(Message().autoload(MSG_STOP), flags=zmq.NOBLOCK)
	except:
		print "Error sending"

@route('/rpc/blackout')
def rpc_blackout():
	global socket
	try:
		socket.send_pyobj(Message().autoload(MSG_BLACKOUT), flags=zmq.NOBLOCK)
	except:
		print "Error sending"

if __name__=="__main__":
	context = zmq.Context()
	socket = context.socket(zmq.PAIR)
	socket.bind("tcp://127.0.0.101:5443")

	run(server='paste')
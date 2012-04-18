from bottle import route, run, static_file, template
import paste
import time
import zmq

from message import *

@route('/')
def index():
	rpc_blackout()
	return template('web/templates/base.tpl')

@route('/static/<filename:path>')
def send_static(filename):
	return static_file(filename, root='web/static')


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
	try:
		socket.bind("tcp://127.0.0.101:5443")
	except:
		print "Could not open socket"

	run(reloader=True)
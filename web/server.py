from bottle import route, run
import paste
import time
import zmq

@route('/')
def index():
	global socket
	socket.send("Hi there")
	return 'test'

if __name__=="__main__":
	context = zmq.Context()
	socket = context.socket(zmq.PAIR)
	socket.bind("tcp://127.0.0.101:5443")

	run(server='paste')
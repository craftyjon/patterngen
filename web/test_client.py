import zmq
import time

if __name__=="__main__":
	context = zmq.Context()
	socket = context.socket(zmq.PAIR)
	socket.connect("tcp://127.0.0.101:5443")
	while True:
		msg = socket.recv()
		print "recv: ", msg
		time.sleep(1)
from array import array

from frame import Frame

class OutputMap:
	def __init__(self):
		self.outputs = []

	def load(self, filename):
		pass

	def map(self, frame):
		buf = frame.buffer
		outlist = []

		for output in self.outputs:
			outlist.append(output[0])
			outlist.append(buf[output[1][0]][output[1][1]][0])
			outlist.append(buf[output[1][0]][output[1][1]][1])
			outlist.append(buf[output[1][0]][output[1][1]][2])

		arr = array('B', outlist)
		return arr
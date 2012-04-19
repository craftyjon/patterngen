import numpy as np
import colorsys
from preset import Preset

class ColorStatic(Preset):
    def __init__(self, size=(24,24)):
        Preset.__init__(self, size)
        self.size = size

    def draw(self):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                el = self.frame.buffer[x][y]
                el[0] *= 0.9
                el[1] *= 0.9
                el[2] *= 0.9

                r = np.random.rand()
                if self.audio_data.is_beat and r > 0.6:
                    h = np.random.rand()
                    (rf,gf,bf) = colorsys.hsv_to_rgb(h, 1.0, 1.0)
                    (el[0],el[1],el[2]) = (int(rf*255),int(gf*255),int(bf*255))

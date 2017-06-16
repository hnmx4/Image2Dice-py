import math
import cv2
import numpy as np
from matplotlib import pyplot as plt


class I2D:
    def __init__(self, filename):
        self.mag = cv2.imread('0.png').shape[0]  # mosaic magnification

        src = cv2.imread(filename, 0)  # read as GRAY
        h, w = src.shape[:2]
        dst = cv2.resize(src, (w - w % self.mag, h - h % self.mag), interpolation=cv2.INTER_CUBIC)

        self.src = dst
        self.h, self.w = dst.shape[:2]
        self.hh = math.floor(self.h / self.mag)
        self.ww = math.floor(self.w / self.mag)

    def mosaic(self):
        lv = 7
        tmp = np.zeros((self.h, self.ww))
        res = np.zeros((self.hh, self.ww))

        for i in range(self.h):
            for j in range(self.ww):
                for k in range(self.mag):
                    tmp[i, j] += self.src[i, j * self.mag + k]

        for i in range(self.hh):
            for j in range(self.ww):
                for k in range(self.mag):
                    res[i, j] += tmp[i * self.mag + k, j]
                res[i, j] = int(res[i, j] / (self.mag * self.mag * math.ceil(255 / lv)))  # quantize
                
        return res

    def dice(self):
        src = self.mosaic()
        h, w = src.shape[:2]
        return np.vstack((np.array([np.hstack((np.array([cv2.imread("%d.png" % src[i, j]) for j in range(w)]))) for i in range(h)])))


i2d = I2D('lenna.jpg')
dst = i2d.dice()

cv2.imwrite('dst.jpg', dst)
plt.imshow(dst, cmap='gray')
plt.show()

import math
import cv2
import numpy as np
from matplotlib import pyplot as plt


def trimming(img, mag):
    height, width = img.shape[:2]
    return cv2.resize(img, (width - width % mag, height - height % mag), interpolation=cv2.INTER_CUBIC)


def mosaic(img, mag):
    h, w = img.shape[:2]
    lv = 7
    ww = int(w / mag)
    hh = int(h / mag)
    tmp = np.zeros((h, ww))
    res = np.zeros((hh, ww))

    for i in range(h):
        for j in range(ww):
            for k in range(mag):
                tmp[i, j] += img[i, j * mag + k]

    for i in range(hh):
        for j in range(ww):
            for k in range(mag):
                res[i, j] += tmp[i * mag + k, j]
            res[i, j] = int(res[i, j] / (mag * mag * math.ceil(255 / lv)))  # quantize

    return res


def diceize(img):
    h, w = img.shape[:2]
    return np.vstack((np.array([np.hstack((np.array([cv2.imread("%d.png" % img[i, j]) for j in range(w)]))) for i in range(h)])))


img = cv2.imread('lenna.jpg', 0)
mag = 12
dst = diceize(mosaic(trimming(img, mag), mag))
cv2.imwrite('dst.jpg', dst)
plt.imshow(dst, cmap='gray')
plt.show()

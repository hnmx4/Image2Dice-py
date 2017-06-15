import cv2
import numpy as np
from matplotlib import pyplot as plt


def trimming(img, mag):
    height, width = img.shape[:2]
    return cv2.resize(img, (width - width % mag, height - height % mag), interpolation=cv2.INTER_CUBIC)


def mosaic(img, mag):
    h, w = img.shape[:2]
    for i in range(0, h, mag):
        for j in range(0, w, mag):
            print(img[i, j])


img = cv2.imread('lenna.jpg', 0)
mag = 12
trim_img = trimming(img, mag)
mosaic(trim_img, mag)

plt.imshow(trim_img, cmap='gray', interpolation='bicubic')
plt.show()

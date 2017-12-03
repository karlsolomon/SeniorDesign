# USAGE
# python compare_all.py

# import the necessary packages
from skimage.measure import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
import cv2.cv as cv
import os
import copy

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	return err

def print_results(a, b, i):
	a = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
	b = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
	m = mse(a, b)
	s = ssim(a, b)
	file.write("%s\tMSE:%.2f\tSSIM:%.6f\n" % (str(i+1),m,s))

def diff_polarize(a,b,i):
	c = cv2.copyMakeBorder(a,0,0,0,0,cv2.BORDER_REPLICATE)
	a = np.float32(a)
	a = a*(1.0/255)
	b = np.float32(b)
	b = b*(1.0/255)
	c = (a[::] - b[::]) / (a[::] + b[::])
	c[c < 0] = 0
	c = c*255
	c = np.uint8(c)
	c = 255-c
	cv2.imwrite("images/will/diff%s.jpeg" % (str(i)), c) #Write image to file

minNum = 1
maxNum = 29
for i in my_range(minNum,maxNum,1):
	a = cv2.imread("images/will/Co%s.jpeg" % (str(i)))
	b = cv2.imread("images/will/Cross%s.jpeg" % (str(i)))
	diff_polarize(a,b,i)




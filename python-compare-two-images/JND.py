# USAGE
# python compare_all.py

# import the necessary packages
from skimage.measure import structural_similarity as ssim
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.colorbar as colorbar
import matplotlib.cm as cm
import numpy as np
import cv2
import os
import copy
from skimage import measure
import math

acceptableRange = 2  # use to set "even illumination" tolerance definition
mid = 127.5		
scalar = 127.5
truncate = True 	# will "truncate" image around mid +/- acceptableRange. So any pixel that isn't deepest blue/red is w/in tolerance
wideSpread = False
path = "images/3.4/"
delta = 0

def diff_color(a,b,offset, name):
	c = a
	a = np.float32(a)
	a = a*(1.0/255)
	b = np.float32(b)
	b = b*(1.0/255)
	c = b-a
	c = (c*scalar)
	minimum = np.min(c)
	maximum = np.max(c)
	stdev = np.std(c)
	mean = np.mean(c)
	#c[::] = mid

	c[c>(mid+delta)] += offset
	c[c<(mid+delta)] -= offset
	stdev = np.std(c)
	c[0,1] = 0
	c[1,0] = 255
	print('offset = %s stdev = %s\n' % (offset, stdev))
	c = np.int8(c)
	plt.close()
	cmap = cm.RdBu
	plt.imshow(c, cmap)
	plt.savefig("%sspread/%s_%s_%s.png" % (path, name, str(offset), str(stdev)), bbox_inches='tight')
	return c

def diff_colors(imageA, imageB, i, name):
	blueA = imageA[:,:,0]
	greenA = imageA[:,:,1]
	redA = imageA[:,:,2]
	blueB = imageB[:,:,0]
	greenB = imageB[:,:,1]
	redB = imageB[:,:,2]
	diff = diff_color(blueA, blueB, i, '%s_blue' % name)
	diff = diff_color(greenA, blueB, i, '%s_green' % name)
	diff = diff_color(redA, redB, i, '%s_red' % name)
	diff = diff_color(imageA, imageB, i, '%s_all' % name)


def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

# for i in my_range(0,5,0.5):
# 	a = mpimg.imread("images/3.5/IMG_8272.JPG")
# 	b = mpimg.imread("images/3.5/IMG_8273.JPG")
# 	diff_colors(a,b,i, 'CONTROL')

# mpimg.imread("images/3.5/IMG_8272.JPG")
# mpimg.imread("images/3.5/IMG_8273.JPG")
# diff_colors(a,b,0, 'CONTROL_CONTROL')

for i in my_range(0,5,0.5):
	a = mpimg.imread("%sAF_Rex150.JPG" % path)
	b = mpimg.imread("%sIMG_8251.JPG" % path)
	diff_colors(a,b,i, 'TEST')

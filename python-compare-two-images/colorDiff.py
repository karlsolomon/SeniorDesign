# USAGE
# python compare_all.py

# import the necessary packages
from skimage.measure import structural_similarity as ssim
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import os
import copy
from skimage import measure
import math

def diff_color(a,b,i,color):
	c = a #mpimg.copyMakeBorder(a,0,0,0,0,mpimg.BORDER_REPLICATE)
	a = np.float32(a)
	a = a*(1.0/255)
	b = np.float32(b)
	b = b*(1.0/255)
	c = a-b
	c = (c*127) + 128
	c = np.uint8(c)
	minimum = np.min(c)
	maximum = np.max(c)
	stdev = np.std(c)
	mean = np.mean(c)
	print("\trange %s\tmean %s\tstdev %s\tmax %s\t min%s\t" % (maximum - minimum, mean - 127, stdev, maximum - 127, minimum - 127))
	#cv2.imwrite("images/2.7/diff%s_%s.jpeg" % (str(i), color), c)
	plt.close()
	plt.imshow(c)
	plt.colorbar()
	plt.savefig("images/2.7/diff%s_%s.png" % (str(i), color))
	plt.pause(5)
	return c

def diff_colors(imageA, imageB,i):
	diff = imageA
	blueA = imageA[:,:,0]
	greenA = imageA[:,:,1]
	redA = imageA[:,:,2]

	blueB = imageB[:,:,0]
	greenB = imageB[:,:,1]
	redB = imageB[:,:,2]

	diff[:,:,0] = diff_color(blueA,blueB,i,'blue')
	diff[:,:,1] = diff_color(greenA,greenB,i,'green')
	diff[:,:,2] = diff_color(redA,redB,i,'red')
	cv2.imwrite("images/2.7/diff%s_merge.jpeg"% (str(i)), diff)
	return diff

path = "images/2.7/"
file = open("compareAll.txt", "w")
file.write("outer\n")

whiteA = mpimg.imread("images/2.7/IMG_8125.JPG")
whiteB = mpimg.imread("images/2.7/IMG_8126.JPG")
a = mpimg.imread("images/2.7/IMG_8130.JPG")
b = mpimg.imread("images/2.7/IMG_8131.JPG")
diff5 = diff_colors(a,b,5)

whiteA = mpimg.imread("images/2.7/IMG_8134.JPG")
whiteB = mpimg.imread("images/2.7/IMG_8135.JPG")
a = mpimg.imread("images/2.7/IMG_8136.JPG")
b = mpimg.imread("images/2.7/IMG_8137.JPG")
diff10 = diff_colors(a,b,10)



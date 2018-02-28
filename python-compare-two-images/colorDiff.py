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

acceptableRange = 5  # use to set "even illumination" tolerance definition
mid = 128			 
scalar = 127
truncate = True 	# will "truncate" image around mid +/- acceptableRange. So any pixel that isn't deepest blue/red is w/in tolerance

def diff_color(a,b,i,color, truncate):
	c = a #mpimg.copyMakeBorder(a,0,0,0,0,mpimg.BORDER_REPLICATE)
	a = np.float32(a)
	a = a*(1.0/255)
	b = np.float32(b)
	b = b*(1.0/255)
	c = b-a
	c = (c*scalar) + mid
	minimum = np.min(c)
	maximum = np.max(c)
	stdev = np.std(c)
	mean = np.mean(c)

	if truncate:
		c[c>mid+acceptableRange] = mid+acceptableRange
		c[c<mid-acceptableRange] = mid-acceptableRange
	else:
		c[0:2] = 0
		c[0:1] = 255
	c = np.uint8(c)
	print("\trange %s\tmean %s\tstdev %s\tmax %s\t min%s\t" % (maximum - minimum, mean - scalar, stdev, maximum - scalar, minimum - scalar))
	plt.close()
	cmap = cm.RdBu
	plt.imshow(c, cmap)
	plt.colorbar()
	plt.savefig("images/2.7/diff%s_%s.png" % (str(i), color))
	return c

def diff_colors(imageA, imageB,i, truncate):
	diff = imageA
	blueA = imageA[:,:,0]
	greenA = imageA[:,:,1]
	redA = imageA[:,:,2]

	blueB = imageB[:,:,0]
	greenB = imageB[:,:,1]
	redB = imageB[:,:,2]
	diff[:,:,0] = diff_color(blueA,blueB,i,'blue', truncate)
	diff[:,:,1] = diff_color(greenA,greenB,i,'green', truncate)
	diff[:,:,2] = diff_color(redA,redB,i,'red', truncate)
	cv2.imwrite("images/2.7/diff%s_merge.jpeg"% (str(i)), diff)
	return diff

path = "images/2.7/"
file = open("compareAll.txt", "w")
file.write("outer\n")


a = mpimg.imread("images/2.7/IMG_8130.JPG")
b = mpimg.imread("images/2.7/IMG_8131.JPG")
diff5 = diff_colors(a,b,5, truncate)

a = mpimg.imread("images/2.7/IMG_8137.JPG")
b = mpimg.imread("images/2.7/IMG_8136.JPG")
diff10 = diff_colors(a,b,10, truncate)



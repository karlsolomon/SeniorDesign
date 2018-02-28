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

acceptableRange = 10  # use to set "even illumination" tolerance definition
mid = 128			 
scalar = 127
truncate = True 	# will "truncate" image around mid +/- acceptableRange. So any pixel that isn't deepest blue/red is w/in tolerance
path = "images/2.27/"

def diff_color(a,b,i,color, truncate):
	c = a
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
		c[c>mid+acceptableRange] = 255
		c[c<mid-acceptableRange] = 0
	else:
		c[0:2] = 0
		c[0:1] = 255
	c = np.uint8(c)
	#print("\trange %s\tmean %s\tstdev %s\tmax %s\t min%s\t" % (maximum - minimum, mean - scalar, stdev, maximum - scalar, minimum - scalar))
	plt.close()
	cmap = cm.RdBu
	plt.imshow(c, cmap)
	plt.colorbar()
	if truncate:
		plt.savefig("%struncate/%s_%s.png" % (path, str(i), color))
	else:
		plt.savefig("%snormal/%s_%s.png" % (path, str(i), color))
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
	#cv2.imwrite("%sdiff%s_together.jpeg" % (path, str(i)), diff)
	return diff

def white_balance(imageA, whiteA):
	c = whiteA
	c = c - mid
	c = c * -1
	return imageA + c

# a = mpimg.imread("%sPin12_White1.JPG" % path)
# b = mpimg.imread("%sPin12_White2.JPG" % path)
# diff5 = diff_colors(a,b,'12White', truncate)

# a = mpimg.imread("%sPin13_White1.JPG" % path)
# b = mpimg.imread("%sPin13_White2.JPG" % path)
# diff10 = diff_colors(a,b,'13White', truncate)

truncate = True
a = mpimg.imread("%sPin12_mole1.JPG" % path)
b = mpimg.imread("%sPin13_mole1.JPG" % path)
aW = mpimg.imread("%sPin12_White1.JPG" % path)
bW = mpimg.imread("%sPin13_White1.JPG" % path)
aBalanced = white_balance(a, aW)
bBalalced = white_balance(b, bW)
diff_colors(aBalanced,bBalalced,'1_Balanced', truncate)
diff_colors(a,b,'1_raw', truncate)
diff_colors(aW,bW,'1_white', truncate)

a = mpimg.imread("%sPin12_mole2.JPG" % path)
b = mpimg.imread("%sPin13_mole2.JPG" % path)
aW = mpimg.imread("%sPin12_White2.JPG" % path)
bW = mpimg.imread("%sPin13_White2.JPG" % path)
aBalanced = white_balance(a, aW)
bBalalced = white_balance(b, bW)
diff_colors(aBalanced,bBalalced,'2_Balanced', truncate)
diff_colors(a,b,'2_raw', truncate)
diff_colors(aW,bW,'2_white', truncate)


truncate = False
a = mpimg.imread("%sPin12_mole1.JPG" % path)
b = mpimg.imread("%sPin13_mole1.JPG" % path)
aW = mpimg.imread("%sPin12_White1.JPG" % path)
bW = mpimg.imread("%sPin13_White1.JPG" % path)
aBalanced = white_balance(a, aW)
bBalalced = white_balance(b, bW)
diff_colors(aBalanced,bBalalced,'1_Balanced', truncate)
diff_colors(a,b,'1_raw', truncate)
diff_colors(aW,bW,'1_white', truncate)


a = mpimg.imread("%sPin12_mole2.JPG" % path)
b = mpimg.imread("%sPin13_mole2.JPG" % path)
aW = mpimg.imread("%sPin12_White2.JPG" % path)
bW = mpimg.imread("%sPin13_White2.JPG" % path)
aBalanced = white_balance(a, aW)
bBalalced = white_balance(b, bW)
diff_colors(aBalanced,bBalalced,'2_Balanced', truncate)
diff_colors(a,b,'2_raw', truncate)
diff_colors(aW,bW,'2_white', truncate)


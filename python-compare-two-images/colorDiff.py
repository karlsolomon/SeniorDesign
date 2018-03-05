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
wideSpread = False
path = "images/3.4/"
file = open("output.txt", "w")

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
		if wideSpread:
			c[c>mid+acceptableRange] = 255
			c[c<mid-acceptableRange] = 0
		else:
			c[c>mid+acceptableRange] = mid + acceptableRange
			c[c<mid-acceptableRange] = mid - acceptableRange
	else:
		c[0:2] = 0
		c[0:1] = 255
	c = np.uint8(c)
	file.write("\trange %s\tmean %s\tstdev %s\tmax %s\t min%s\n" % (maximum - minimum, mean - scalar, stdev, maximum - scalar, minimum - scalar))
	plt.close()
	cmap = cm.RdBu
	plt.imshow(c, cmap)
	plt.colorbar()
	if truncate:
		if wideSpread:
			plt.savefig("%struncateWide/%s_%s.png" % (path, str(i), color))
		else:
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
file.write('\ncontrol_1\n')
a = mpimg.imread("%sAF_none1.JPG" % path)
b = mpimg.imread("%sAF_none2.JPG" % path)
diff_colors(a,b,'10mA_Control_1', truncate)

file.write('\ncontrol_2\n')
a = mpimg.imread("%sIMG_8249.JPG" % path)
b = mpimg.imread("%sIMG_8250.JPG" % path)
diff_colors(a,b,'10mA_Control_2', truncate)

file.write('\n10mA\n')
a = mpimg.imread("%sAF_none1.JPG" % path)
b = mpimg.imread("%sIMG_8249.JPG" % path)
diff_colors(a,b,'10mA', truncate)

file.write('\n9mA\n')
a = mpimg.imread("%sAF_Rex150.JPG" % path)
b = mpimg.imread("%sIMG_8251.JPG" % path)
diff_colors(a,b,'9mA', truncate)

file.write('\n8mA\n')
a = mpimg.imread("%sAF_Rex68.JPG" % path)
b = mpimg.imread("%sIMG_8252.JPG" % path)
diff_colors(a,b,'8mA', truncate)

file.write('\n7mA\n')
a = mpimg.imread("%sAF_Rex56.JPG" % path)
b = mpimg.imread("%sIMG_8253.JPG" % path)
diff_colors(a,b,'7mA', truncate)

file.write('\n6mA\n')
a = mpimg.imread("%sAF_Rex39.JPG" % path)
b = mpimg.imread("%sIMG_8254.JPG" % path)
diff_colors(a,b,'6mA', truncate)

file.write('\ndelta1mA\n')
a = mpimg.imread("%sAF_Rex150.JPG" % path)
b = mpimg.imread("%sAF_Rex68.JPG" % path)
diff_colors(a,b,'delta1mA', truncate)

file.write('\ndelta2mA\n')
a = mpimg.imread("%sAF_Rex150.JPG" % path)
b = mpimg.imread("%sAF_Rex56.JPG" % path)
diff_colors(a,b,'delta2mA', truncate)

file.write('\ndelta3mA\n')
a = mpimg.imread("%sAF_Rex150.JPG" % path)
b = mpimg.imread("%sAF_Rex39.JPG" % path)
diff_colors(a,b,'delta3mA', truncate)

file.close()


# aW = mpimg.imread("%sPin12_White1.JPG" % path)
# bW = mpimg.imread("%sPin13_White1.JPG" % path)
# aBalanced = white_balance(a, aW)
# bBalalced = white_balance(b, bW)
# file.write('\n1_balanced\n')
# diff_colors(aBalanced,bBalalced,'1_Balanced', truncate)
# diff_colors(a,b,'1_raw', truncate)
# diff_colors(aW,bW,'1_white', truncate)

# a = mpimg.imread("%sPin12_mole2.JPG" % path)
# b = mpimg.imread("%sPin13_mole2.JPG" % path)
# aW = mpimg.imread("%sPin12_White2.JPG" % path)
# bW = mpimg.imread("%sPin13_White2.JPG" % path)
# aBalanced = white_balance(a, aW)
# bBalalced = white_balance(b, bW)
# diff_colors(aBalanced,bBalalced,'2_Balanced', truncate)
# diff_colors(a,b,'2_raw', truncate)
# diff_colors(aW,bW,'2_white', truncate)


# truncate = False
# a = mpimg.imread("%sPin12_mole1.JPG" % path)
# b = mpimg.imread("%sPin13_mole1.JPG" % path)
# aW = mpimg.imread("%sPin12_White1.JPG" % path)
# bW = mpimg.imread("%sPin13_White1.JPG" % path)
# aBalanced = white_balance(a, aW)
# bBalalced = white_balance(b, bW)
# diff_colors(aBalanced,bBalalced,'1_Balanced', truncate)
# diff_colors(a,b,'1_raw', truncate)
# diff_colors(aW,bW,'1_white', truncate)


# a = mpimg.imread("%sPin12_mole2.JPG" % path)
# b = mpimg.imread("%sPin13_mole2.JPG" % path)
# aW = mpimg.imread("%sPin12_White2.JPG" % path)
# bW = mpimg.imread("%sPin13_White2.JPG" % path)
# aBalanced = white_balance(a, aW)
# bBalalced = white_balance(b, bW)
# diff_colors(aBalanced,bBalalced,'2_Balanced', truncate)
# diff_colors(a,b,'2_raw', truncate)
# diff_colors(aW,bW,'2_white', truncate)


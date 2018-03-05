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
import scipy
from scipy import ndimage

path = "images/3.1/"

def saveFig(a,i,j):
	plt.imshow(a)
	#plt.axis('off')
	plt.colorbar()
	plt.savefig("%s%s_%s" %(path, i, j), bbox_inches='tight')
	plt.close()

def splitImage(a,i):
	a[1,0] = [128,128,128]
	a[0,1] = [255,255,255]

	blue = a[:,:,0]
	green = a[:,:,1]
	red = a[:,:,2]
	saveFig(blue, i, 'blue')
	# saveFig(green, i, 'green')
	# saveFig(red, i, 'red')
	# saveFig(a, i, 'all')

a = mpimg.imread("%sMolescope2-zoomed.JPG" % path)
splitImage(a, 'molescope')

# path = "images/3.4/"

# a = mpimg.imread("%sIMG_8249.JPG" % path)
# splitImage(a, '2_10mA')
# a = mpimg.imread("%sIMG_8251.JPG" % path)
# splitImage(a, '2_9mA')
# a = mpimg.imread("%sIMG_8252.JPG" % path)
# splitImage(a, '2_8mA')
# a = mpimg.imread("%sIMG_8253.JPG" % path)
# splitImage(a, '2_7mA')
# a = mpimg.imread("%sIMG_8254.JPG" % path)
# splitImage(a, '2_6mA')


# a = mpimg.imread("%sAF_none1.JPG" % path)
# splitImage(a, '1_10mA')
# a = mpimg.imread("%sAF_Rex150.JPG" % path)
# splitImage(a, '1_9mA')
# a = mpimg.imread("%sAF_Rex68.JPG" % path)
# splitImage(a, '1_8mA')
# a = mpimg.imread("%sAF_Rex56.JPG" % path)
# splitImage(a, '1_7mA')
# a = mpimg.imread("%sAF_Rex39.JPG" % path)
# splitImage(a, '1_6mA')


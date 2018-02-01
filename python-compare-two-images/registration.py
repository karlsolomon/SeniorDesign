# USAGE
# python compare_all.py

# import the necessary packages
from skimage.measure import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import copy
from skimage import measure
import math

def writeWarpMatrix(im1,im2,path,i):
    im1_gray = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY)
    im2_gray = cv2.cvtColor(im2,cv2.COLOR_BGR2GRAY)
    # Find size of image1
    sz = im1.shape
    #2D transformations Only: Translation/Rotation/Scale
    warp_mode = cv2.MOTION_TRANSLATION
    warp_matrix = np.eye(2, 3, dtype=np.float32)
    number_of_iterations = 1000;
    termination_eps = 1e-10;
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations,  termination_eps)
    (cc, warp_matrix) = cv2.findTransformECC(im1_gray,im2_gray,warp_matrix, warp_mode, criteria)  
    x = warp_matrix[0][2]
    y = warp_matrix[1][2]
    z = math.sqrt(math.pow(x,2) + math.pow(y,2))
    file.write("x:%.f\ty:%.f\tz:%.f\n" % (x, y, z))
    file.write("%.3f\n" % z)
    im2_aligned = cv2.warpAffine(im2, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
    saveWarpImages(im1,im2,im2_aligned,path,i)
    
def saveWarpImages(im1,im2,im3,path,i):
    b1,g1,r1 = cv2.split(im1)
    b2,g2,r2 = cv2.split(im2)
    b3,g3,r3 = cv2.split(im3)
    merge1 = cv2.merge((b1,g2,r1))
    merge2 = cv2.merge((b1,g3,r1))
    cv2.imwrite("%sframe%da.jpg" % (path, i), merge1)    # save frame as JPEG file
    cv2.imwrite("%sframe%db.jpg" % (path, i), merge2)    # save frame as JPEG file
	#cv2.imwrite(path + str(i) + "_" +str(i+1) + "preWarp.jpg", merge1)
	#cv2.imwrite("%s%s_%spostWarp.jpg" % (path, str(i), str(i + 1)), merge2)


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

def print_results(a, b):
	a = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
	b = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
	m = mse(a, b)
	file.write("MSE:%.2f\n" % m)


def diff_polarize(a,b,i):
	a = cv2.cvtColor(a,cv2.COLOR_BGR2GRAY)
	b = cv2.cvtColor(b,cv2.COLOR_BGR2GRAY)
	c = cv2.copyMakeBorder(a,0,0,0,0,cv2.BORDER_REPLICATE)
	a = np.float32(a)
	a = a*(1.0/255)
	b = np.float32(b)
	b = b*(1.0/255)
	c = (a[::] - b[::])
	c = (c*127) + 127	
	c = np.uint8(c)
	d = c*0;
	d = d + 127;
	print("\trange %s\tmean %s\tstdev %s\tmax %s\t min%s\t" % (np.max(c) - np.min(c), np.mean(c) - 127, np.std(c), np.max(c) - 127, np.min(c) - 127))
	cv2.imwrite("images/1.26/diff%s.jpeg" % (str(i)), c) #Write image to file
	cv2.imwrite("images/1.26/diffControl.jpeg", d)
	white_balance_simple(c, a, b, i)


def white_balance_simple(white, a, b, i):
	avg = np.mean(white)
	diff = cv2.copyMakeBorder(a,0,0,0,0,cv2.BORDER_REPLICATE)
	balanced = cv2.copyMakeBorder(a,0,0,0,0,cv2.BORDER_REPLICATE)
	a = np.float32(a)
	b = np.float32(b)
	diff = (a[::] - b[::])
	diff = diff + 127	
	diff = np.uint8(diff)
	balanced = (avg - white[::]) # px = 100 avg = 50, balanced = -50 (immediate scale) 
	balanced = balanced + diff
	balanced = np.uint8(balanced)
	cv2.imwrite("images/1.26/balanceSimple%s.jpeg" % (str(i)), balanced) #Write image to file
	print("B:\trange %s\tmean %s\tstdev %s\tmax %s\t min%s\t" % (np.max(balanced) - np.min(balanced), np.mean(balanced) - 127, np.std(balanced), np.max(balanced) - 127, np.min(balanced) - 127))


def white_balance_complex()



path = "images/1.26/"
file = open("compareAll.txt", "w")
file.write("outer\n")
a = cv2.imread("images/1.26/IMG_8049.JPG")
b = cv2.imread("images/1.26/IMG_8050.JPG")
print_results(a,b)
diff_polarize(a,b,0)

file.write("inner\n")
a = cv2.imread("images/1.26/IMG_8074.JPG")
b = cv2.imread("images/1.26/IMG_8075.JPG")
print_results(a,b)
diff_polarize(a,b,1)

#writeWarpMatrix(a,b,path,0)

#writeWarpMatrix(a,b,path,1)

# file.write("12_shakeA\n")
# a = cv2.imread("images/1.21/12_Shake/A/IMG_0009.JPG")
# for i in my_range(10,13,1):
# 	b = cv2.imread("images/1.21/12_Shake/A/IMG_00%s.JPG" % (str(i)))
# 	print_results(a,b)
# 	diff_polarize(a,b,i-8)
# 	#writeWarpMatrix(a,b,path,i)

# file.write("12_shakeB\n")
# a = cv2.imread("images/1.21/12_Shake/B/IMG_0014.JPG")
# for i in my_range(15,18,1):
# 	b = cv2.imread("images/1.21/12_Shake/B/IMG_00%s.JPG" % (str(i)))
# 	print_results(a,b)
# 	diff_polarize(a,b,i-8)
# 	#writeWarpMatrix(a,b,path,i)

# file.write("9_shakeA\n")
# a = cv2.imread("images/1.21/9_Shake/A/IMG_0019.JPG")
# for i in my_range(20,23,1):
# 	b = cv2.imread("images/1.21/9_Shake/A/IMG_00%s.JPG" % (str(i)))
# 	print_results(a,b)
# 	diff_polarize(a,b,i-8)
# 	#writeWarpMatrix(a,b,path,i)

# file.write("9_shakeB\n")
# a = cv2.imread("images/1.21/9_Shake/B/IMG_0024.JPG")
# for i in my_range(25,28,1):
# 	b = cv2.imread("images/1.21/9_Shake/B/IMG_00%s.JPG" % (str(i)))
# 	print_results(a,b)
# 	diff_polarize(a,b,i-8)
# 	#writeWarpMatrix(a,b,path,i)

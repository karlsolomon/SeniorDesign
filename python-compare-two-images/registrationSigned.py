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
	c = (c*127) + 128	
	c = np.uint8(c)
	# d = c*0;
	# d = d + 127;
	print("\trange %s\tmean %s\tstdev %s\tmax %s\t min%s\t" % (np.max(c) - np.min(c), np.mean(c) - 127, np.std(c), np.max(c) - 127, np.min(c) - 127))
	cv2.imwrite("images/2.5/diff%s.jpeg" % (str(i)), c) #Write image to file
	#cv2.imwrite("images/2.5/diffControl.jpeg", d)
	#white_balance_simple(c, a, b, i)


#basically shifts every pixel by the average pixel value to accomplish an average of 0 
def white_balance_simple(white, a, b, i):
	avg = np.mean(white)
	diff = cv2.copyMakeBorder(a,0,0,0,0,cv2.BORDER_REPLICATE)
	balanced = cv2.copyMakeBorder(a,0,0,0,0,cv2.BORDER_REPLICATE)
	a = np.float32(a)
	b = np.float32(b)
	diff = (a[::] - b[::])
	diff = diff + 128	
	diff = np.uint8(diff)
	balanced = (avg - white[::]) # px = 100 avg = 50, balanced = -50 (immediate scale) 
	balanced = balanced + diff
	balanced = np.uint8(balanced)
	cv2.imwrite("images/2.5/balanceSimple%s.jpeg" % (str(i)), balanced) #Write image to file
	print("B:\trange %s\tmean %s\tstdev %s\tmax %s\t min%s\t" % (np.max(balanced) - np.min(balanced), np.mean(balanced) - 127, np.std(balanced), np.max(balanced) - 127, np.min(balanced) - 127))

# requires white balance images under both illumation methods
def white_balance_pixel(whiteA, whiteB, a, b, i):
	diff = cv2.copyMakeBorder(a,0,0,0,0,cv2.BORDER_REPLICATE)

	aB, aG, aR = cv2.split(a)
	bB, bG, bR = cv2.split(b)
	aB_W, aG_W, aR_W = cv2.split(whiteA)
	bB_W, bG_W, bR_W = cv2.split(whiteB)
	
	avgAB_W = np.mean(aB_W)
	avgAG_W = np.mean(aG_W)
	avgAR_W = np.mean(aR_W)

	avgBB_W = np.mean(bB_W)
	avgBG_W = np.mean(bG_W)
	avgBR_W = np.mean(bR_W)

	deltaAB = aB - avgAB_W
	deltaAG = aG - avgAG_W
	deltaAR = aR - avgAR_W

	deltaBB = bB - avgBB_W
	deltaBG = bG - avgBG_W
	deltaBR = bR - avgBR_W

	a = cv2.merge((np.uint8(-1*np.min(deltaAB) + deltaAB), np.uint8(-1*np.min(deltaAG)  + deltaAG), np.uint8(-1*np.min(deltaAR)  + deltaAR)))
	b = cv2.merge((np.uint8(-1*np.min(deltaBB) + deltaBB), np.uint8(-1*np.min(deltaBG)  + deltaBG), np.uint8(-1*np.min(deltaBR)  + deltaBR)))

	cv2.imwrite("images/2.5/balancePixelWiseA%s.jpeg" % (str(i)), np.uint8(a)) #Write image to file
	cv2.imwrite("images/2.5/balancePixelWiseB%s.jpeg" % (str(i)), np.uint8(b)) #Write image to file
	diff = (a[::] - b[::])
	diff = diff + 128	
	diff = np.uint8(diff)
	cv2.imwrite("images/2.5/balancePixelWise%s.jpeg" % (str(i)), diff) #Write image to file
	print("BC:\trange %s\tmean %s\tstdev %s\tmax %s\t min%s\t" % (np.max(diff) - np.min(diff), np.mean(diff) - 127, np.std(diff), np.max(diff) - 127, np.min(diff) - 127))
	return (a,b)

def white_balance_will(darkA, whiteA, a, darkB, whiteB, b, i):
	diff = cv2.copyMakeBorder(a,0,0,0,0,cv2.BORDER_REPLICATE)


def white_balance_color_single(a, whiteA, i):
	B, G, R = cv2.split(whiteA)
	B1, G1, R1 = cv2.split(a)

	R1 = R1.astype(np.float64)
	G1 = G1.astype(np.float64)
	B1 = B1.astype(np.float64)

	BMax = float(np.max(B))
	GMax = float(np.max(G))
	RMax = float(np.max(R))
	BMod = True
	GMod = True
	RMod = True
	Max = max(BMax, GMax, RMax)
	print("%s %s %s\n" % (RMax, GMax, BMax))
	B1 *= Max/BMax
	G1 *= Max/GMax
	R1 *= Max/RMax
	R1 = R1.astype(np.uint8)
	G1 = G1.astype(np.uint8)
	B1 = B1.astype(np.uint8)

	BMax = np.max(B1)
	GMax = np.max(G1)
	RMax = np.max(R1)
	image = cv2.merge((B1,G1,R1))
	cv2.imwrite("images/2.5/whiteBalanced%s.jpeg" % (str(i)), image) #Write image to file
	return image

def white_balance_color(whiteA, whiteB, a, b):
	a = white_balance_color_single(a, whiteA, 0)
	b = white_balance_color_single(b, whiteB, 1)
	return (a,b)



path = "images/2.5/"
file = open("compareAll.txt", "w")
file.write("outer\n")

whiteA = cv2.imread("images/2.5/IMG_8093.JPG")
a = cv2.imread("images/2.5/IMG_8094.JPG")
whiteB = cv2.imread("images/2.5/IMG_8095.JPG")
b = cv2.imread("images/2.5/IMG_8096.JPG")

print_results(a,b)
diff_polarize(a,b,0)
(aPixel, bPixel) = white_balance_pixel(whiteA, whiteB, a, b, 8)
diff_polarize(aPixel,bPixel,8)
(a,b) = white_balance_color(whiteA, whiteB, a, b)
diff_polarize(a,b,1)

# file.write("inner\n")
# a = cv2.imread("images/2.5/IMG_8074.JPG")
# b = cv2.imread("images/2.5/IMG_8075.JPG")
# print_results(a,b)
# diff_polarize(a,b,2)
# (a,b) = white_balance_color(a,b)
# diff_polarize(a,b,3)

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

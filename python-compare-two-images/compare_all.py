# USAGE
# python compare_all.py

# import the necessary packages
from skimage.measure import structural_similarity as ssim
from skimage import measure
import matplotlib.pyplot as plt
import numpy as np
import cv2
import copy
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
    #x = warp_matrix[0][2]
    #y = warp_matrix[1][2]
    #z = math.sqrt(math.pow(x,2) + math.pow(y,2))
    #file.write("x:%.f\ty:%.f\tz:%.f\n" % (x, y, z))
    #file.write("%.3f\n" % z)
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

def print_results(a, b, i):
	agray = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
	bgray = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
	m = mse(agray, bgray)
	file.write("MSE:%.2f\n" % m)
	#score = ssim(agray, bgray)
	#print("ssim done: %s" % str(i))
	#(score,diff) = measure.compare_ssim(a, b, full=True)  #trying to calculate this causes what appears to be inf loop. Basically games my CPU...
	#diff = (diff*255).astype("uint8")
	#file.write("%s\tMSE:%.2f\tSSIM:%.6f\n" % (str(i+1),m,score))
	#cv2.imshow("Diff", diff)
	#cv2.waitKey(0)

def diff_polarize(a,b,i):
	c = cv2.copyMakeBorder(a,0,0,0,0,cv2.BORDER_REPLICATE)
	a = np.float32(a)
	a = a*(1.0/255)
	b = np.float32(b)
	b = b*(1.0/255)
	c = (a[::] - b[::])# / (a[::] + b[::])
	c[c < 0] = c*-1
	#normalize
	scale = 255/max(c) 
	print(scale)
	c = c*255*scale # fit to 8bit
	c = np.uint8(c)
	c = 255-c
	cv2.imwrite("images/will/diff%s.jpeg" % (str(i)), c) #Write image to file

minNum = 1


#for i in my_range(minNum,maxNum,1):
#	a = cv2.imread("images/will/Co%s.jpeg" % (str(i)))
#	b = cv2.imread("images/will/Cross%s.jpeg" % (str(i)))
#	diff_polarize(a,b,i)

pathStart = "images/speed/Dustin2/"
maxNum = 29
resolution = "4k/Dustin/"
path = "%s%s" % (pathStart, resolution)
#file = open("compareAll2.txt", "a")
#a = cv2.imread("%sframe%s.jpg" % (path, str(minNum)))
#file.write("%s\n" % path)
a = cv2.imread("%sframe0001.jpg" % path)
for i in my_range(minNum, maxNum, 1):
	if(i < 10):
		b = cv2.imread("%sframe000%s.jpg" % (path, str(i)))
	elif (i < 100):
		b = cv2.imread("%sframe00%s.jpg" % (path, str(i)))
	elif(i < 1000):
		b = cv2.imread("%sframe0%s.jpg" % (path, str(i)))
	else:
		b = cv2.imread("%sframe%s.jpg" % (path, str(i)))
	writeWarpMatrix(a,b,path,i)
	#print_results(a,b,i)
#file.close()


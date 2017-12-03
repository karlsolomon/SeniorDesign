# USAGE
# python compare_all.py

# import the necessary packages
from skimage.measure import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os

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
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def print_results(a, b, i):
	a = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
	b = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
	m = mse(a, b)
	s = ssim(a, b)
	file.write("%s\tMSE:%.2f\tSSIM:%.6f\n" % (str(i+1),m,s))



# load all images in the images/ directory and compare each a & b versions of the files
#path, dirs, files = os.walk("images").next()
#file_count = len(files)
#file_count = file_count / 2 #a and b for each image
file = open("comparison.txt", "w")
minNum = 702
maxNum = 710
for i in my_range(minNum,maxNum,2):
	print(i)
	if(i < 9):
		a = cv2.imread("images/IMG_0%s.JPG" % (str(i)))
		b = cv2.imread("images/IMG_0%s.JPG" % (str(i+1)))
		print_results(a,b,i)
	else:
		a = cv2.imread("images/IMG_0%s.JPG" % (str(i)))
		b = cv2.imread("images/IMG_0%s.JPG" % (str(i+1)))
		print_results(a,b,i)
file.close()



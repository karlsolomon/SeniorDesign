# USAGE
# python untitled.py

# import the necessary packages
from skimage.measure import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def print_difference(imageA, imageB):
	m = mse(imageA, imageB)
	s = ssim(imageA, imageB)
	print("MSE:%.2f\tSSI%.2f" % (m,s))

# load the images -- the original, the original + contrast,
# and the original + photoshop

path, dirs, files = os.walk("images").next()
file_count = len(files)
file_count = file_count / 2
for i in range(file_count):
	a = cv2.imread("images/%sa.png" % (str(i+1)))
	b = cv2.imread("images/%sb.png" % (str(i+1)))
	a = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
	b = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
	print_difference(a, b)

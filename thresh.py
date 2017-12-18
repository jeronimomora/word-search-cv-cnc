# import the necessary packages
import numpy as np
import argparse
import cv2
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image file")
args = vars(ap.parse_args())
 
# load the image from disk
image = cv2.imread(args["image"])

# convert the image to grayscale and flip the foreground
# and background to ensure foreground is now "white" and
# the background is "black"
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bitwise_not(gray)
 
# threshold the image, setting all foreground pixels to
# 255 and all background pixels to 0
image = cv2.threshold(gray, 100, 255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	
element = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
image = cv2.erode(image, element, iterations = 2)

new_name = args["image"].split('.')[0] + '_erode.png'
cv2.imwrite(new_name,image)
cv2.waitKey(0)
import cv2
import numpy as np
import queue
from ctypes import *
import os
import math

def fit_2_hsv(hsv_color):
    return (hsv_color[0]/2,  math.floor((hsv_color[1]/100)*255), math.floor((hsv_color[2]/100)*255))

def find_rectangles_by_color(frame,hsv_color_low_limit,hsv_color_high_limit,row_threshold,column_threshold):    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    low_limit = fit_2_hsv(hsv_color_low_limit)
    high_limit = fit_2_hsv(hsv_color_high_limit)
    mask = cv2.inRange(hsv, low_limit, high_limit)
    output = cv2.bitwise_and(frame,frame, mask= mask)
    h, s, v1 = cv2.split(output)
    rectangles,size = find_rects(h)
    if rectangles is None:
        return None
    
    results = []
    for rect_idx in rectangles:
        if  not ((rect_idx[2] - rect_idx[0] <= row_threshold) or (rect_idx[3] - rect_idx[1] <= column_threshold)):
           results.append(rect_idx) 
    
    return results

def find_rects(image):
    c_file = os.path.join(os.path.dirname(__file__),'detect_rectangles.so')# get the c_file
    testso = CDLL(c_file)
    testarray1 = np.fromstring(image, np.uint8) 
    testarray2 = np.reshape(testarray1, (len(image), len(image[0]), 1))
    framearray = testarray2.tostring()
    testso.detect_rectangles.argtypes = c_char_p, c_int, c_int,POINTER(c_int), POINTER(c_int),POINTER(c_int),POINTER(c_int)
    l_limit = c_int(5)
    h_limit = c_int(5)
    size = c_int(50000)
    output = (c_int*size.value)()
    rows = c_int(len(image))
    cols = c_int(len(image[0]))
    testso.detect_rectangles(framearray, rows, cols,byref(l_limit), byref(h_limit), output, byref(size))
    
    # q = queue.Queue()
    # size_of_array = len(image)
    # output = []
    # for i in range(0,size_of_array):
    #     for j in range(0, len(image[0])):
    #         if image[i][j] != 0:                
    #             q.put([i,j])
    #             min_r = i
    #             min_c = j
    #             max_r = i
    #             max_c = j
    #             while not q.empty():
    #                 arr = q.get()
    #                 if  (arr[0] < 0 or arr[1] < 0 or arr[0] >  len(image)-1 or arr[1] >  len(image[0]) - 1  ) or image[arr[0]][arr[1]] == 0:
    #                     continue
    #                 image[arr[0]][arr[1]] = 0
    #                 if min_r > arr[0]:
    #                     min_r = arr[0]
    #                 if max_r < arr[0]:
    #                     max_r = arr[0]
    #                 if min_c > arr[1]:
    #                     min_c = arr[1]
    #                 if max_c < arr[1]:
    #                     max_c = arr[1]

    #                 q.put([arr[0]+1,arr[1]])
    #                 q.put([arr[0]-1,arr[1]])
    #                 q.put([arr[0],arr[1]+1])
    #                 q.put([arr[0],arr[1]-1])
                                          
    #             output.append([min_r,min_c, max_r, max_c])

    out = []
    for i in range(0,size.value,4):
        out.append([output[i] , output[i+1],output[i+2],output[i+3]])
    return out,size.value


def findend(i,j,a,output,index):
	x = len(a)
	y = len(a[0])

	# flag to check column edge case,
	# initializing with 0
	flagc = 0

	# flag to check row edge case,
	# initializing with 0
	flagr = 0

	for m in range(i,x):

		# loop breaks where first 1 encounters
		if a[m][j] == 0:
			flagr = 1 # set the flag
			break

		# pass because already processed
		if a[m][j] == -1:
			pass

		for n in range(j, y):

			# loop breaks where first 1 encounters
			if a[m][n] == 0:
				flagc = 1 # set the flag
				break

			# fill rectangle elements with any
			# number so that we can exclude
			# next time
			a[m][n] = -1

	if flagr == 1:
		output[index].append( m-1)
	else:
		# when end point touch the boundary
		output[index].append(m)

	if flagc == 1:
		output[index].append(n-1)
	else:
		# when end point touch the boundary
		output[index].append(n)


def get_rectangle_coordinates(a,low_limit,high_limit):

	# retrieving the column size of array
	size_of_array = len(a)

	# output array where we are going
	# to store our output
	output = []

	# It will be used for storing start
	# and end location in the same index
	index = -1

	for i in range(0,size_of_array):
		for j in range(0, len(a[0])):
			if a[i][j] >= low_limit and a[i][j] <= high_limit:

				# storing initial position
				# of rectangle
				output.append([i, j])

				# will be used for the
				# last position
				index = index + 1	
				findend(i, j, a, output, index)


	return output

# imports
from matplotlib.image import imread
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from piece import *
from PIL import Image

'''
This function simply loads in and returns an image given a path
'''
def get_image(path):
	return imread(path)

'''
Takes in an image with the top left pixel as "background" then cuts up the image
into smaller pieces that don't contain that background in an array. Finally, this func
normalizes the images of those smaller pieces.
'''
def cut_image(image, normalized_size):

	# 1. get mask
	image = np.copy(image) # prevents read-only error
	avg_color = image[0].mean(axis=0) # gets avg color of top row
	mask = loose_mask(image, avg_color, 70) # can be improved

	# 2. get continuous pieces
	blobs, number_of_blobs = ndimage.label(~mask)
	pieces = []
	square_size = 0
	for i in range(1, number_of_blobs):
		# 2a. find a true piece
		points = np.argwhere(blobs == i)
		# somewhat arbitrary method to remove small blobs
		if points.shape[0] < 3000:
			continue
		# create piece object and save it
		piece = Piece(points)
		pieces.append(piece)
		# 2b. find size of minimum rectangle to contain continuous piece
		x_range, y_range = piece.get_xy_range()
		max_range = max(x_range, y_range)
		if square_size < max_range:
			square_size = max_range

	avg_color = avg_color.astype(int)
	# 2c. collect continuous piece
	for piece in pieces:
		piece.gather_pixel_data(image, square_size, avg_color)
		# 2d. normalize size of all pieces
		piece.pixel_data = normalize(piece.pixel_data, normalized_size)

	return pieces

'''
Returns a true false np array with true where the input image is not the same as color
'''
def loose_mask(image, color, plus_minus=10):
	color = np.array(color)
	c_min = color - plus_minus
	c_max = color + plus_minus
	less_than = np.all(image[:,:,:] >= c_min, axis=2)
	grtr_than = np.all(image[:,:,:] <= c_max, axis=2)
	mask = (less_than & grtr_than)
	return mask

'''
Use flood fill algorithm to mask out background of image
Takes in a np array of the image
Returns a mask of the image with background pixels labeled as True
'''
def flood_fill(matrix_of_image):
	COLOR_RANGE = 8
	width = len(matrix)
	height = len(matrix[0])
	mask = np.zeros((matrix.shape[0], matrix.shape[1]), dtype=bool)
	visited = np.zeros((matrix.shape[0], matrix.shape[1]), dtype=bool)
	queue = []

	start_x = 0
	start_y = 0
	start_color = matrix[start_x][start_y]
	queue.append((start_x, start_y, start_color))

	while len(queue) > 0 :
		current_tuple = queue.pop(0)
		x = current_tuple[0]
		y = current_tuple[1]
		prev_color = current_tuple[2]

		#set COLOR_RANGE
		max = prev_color + COLOR_RANGE #NEED TO UPDATE START COLOR WITHIN THE LOOP
		min = prev_color - COLOR_RANGE

		visited[x][y] = True

		if not (np.all(min<matrix[x][y]) and np.all(matrix[x][y]<max)):
			#print("color not approved")
			pass

		# keep crawling
		else:
			# update the mask
			mask[x][y] = True #LABELS BACKGROUND AS TRUE
			prev_color = matrix[x][y] #UPDATING PREVIOUS COLOR
			# get neighboring pixels and call on those
			neighbors = [(x-1,y),(x+1,y),(x-1,y-1),(x+1,y+1),(x-1,y+1),(x+1,y-1),(x,y-1),(x,y+1)]
			neighbors = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
			# call on each neighbor
			for n in neighbors:
				# if in range of image
				if (0 <= n[0] <= width-1 and 0 <= n[1] <= height-1):
					if visited[n[0]][n[1]] == False :
						visited[n[0]][n[1]] = True
						queue.append((n[0], n[1], prev_color))
	return mask



'''
This function will normalize our pieces matrices
Takes in an np array representing a puzzle piece
Converts array to an Image --> found that PIL functions were better suited to scaling images than trying to mess with the image as an arrays.
Resizes image using PIL library functions
Converts scaled image back to a np array
Returns new array
'''
def normalize(piece, output_size):
	image = Image.fromarray(piece.astype(np.uint8))
	#image.show()
	scaled_image = image.resize((output_size, output_size))
	#scaled_image.show()
	scaled_array = np.array(scaled_image)
	return scaled_array

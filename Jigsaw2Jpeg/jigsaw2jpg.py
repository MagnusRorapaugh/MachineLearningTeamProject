# imports
from matplotlib.image import imread
import numpy as np
import matplotlib.pyplot as plt

'''
This function simply loads in and returns an image given a path
'''
def get_image(path):
	return imread(path)
'''
Takes in an image with the top left pixel as "background" then cuts up the image
into smaller pieces that don't contain that background in an array
'''
def cut_image(image):
	
	# 1. get mask
	
	plt.imshow(image)
	plt.show()
	
	color = image[0].mean(axis=0) # gets avg color of top row
	mask = loose_mask(image, color, 50)
	image[mask] = [255,150,255] # replace background
	
	plt.imshow(image)
	plt.show()
	
	# TODO
	# 2. get continuous pieces 
	pieces = []
	while ~mask.any():
		break
		# 2a. find a true piece
		# 2b. find size of minimum rectangle to contain continuous piece
		# 2c. collect continuous piece
		
	# TODO
	# 3. normalize size of all pieces
	normalize(pieces)
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
This function will normalize our pieces matrices
'''
def normalize(pieces):
	pass



im = get_image("puzzle2.jpg")
cut_image(im)


'''
DEBUGGING CODE:
fake_image = np.array(
	[
		[[1,2,3], [4,5,3], [1,2,3]],
		[[10,20,30], [1,2,3], [10,20,30]],
		[[10,20,30], [10,-20,30], [1,3,3]]
	]
)

plt.loose_mask(fake_image, [1,2,3])
'''
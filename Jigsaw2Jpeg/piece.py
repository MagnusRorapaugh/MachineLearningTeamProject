import numpy as np

class Piece:

	def __init__(self, points):
		self.points = points
		self.x_min = points[:,0].min() # x
		self.y_min = points[:,1].min() # y
		self.x_max = points[:,0].max() # x
		self.y_max = points[:,1].max() # y
		self.pixel_data = None

	'''
	Returns the list of 4 corners of a box that would fit over the whole piece.
	The box is (roughly) centered on the piece
	If the given size is not big enough, this function returns None.
	'''
	def get_box(self, size): # TODO
		x_range, y_range = self.get_xy_range()
		# return None if the box is too small
		if size < x_range or x < y_range:
			return None
		# calculate the midpoint for mins and maxs
		x_mid = self.x_min + int(x_range/2) # INT ROUNDS DOWN FROM 0.5
		y_mid = self.y_min + int(y_range/2)

	'''
	Returns the the length of the range of x and y which this shape occupies
	in the form of the tuple (x,y)
	'''
	def get_xy_range(self):
		return self.x_max - self.x_min + 1, self.y_max - self.y_min + 1

	'''
	Gathers pixel data from given image. Assumes that the image given is the
	image from which the piece was originally created. Saves the pixel data in
	a size by size matrix where untouched pixels are set to the background color
	'''
	def gather_pixel_data(self, image, size, background=[0,0,0]): # TODO
        # 1. create array of only background colors
        #
		pass

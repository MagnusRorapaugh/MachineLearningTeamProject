import numpy as np
import joblib
from jigsaw2jpg import *
from matplotlib.image import imread

'''
This function creates a numpy array that can easily be converted into a dataset for the
predictive model. It takes in an input file name of a full puzzle, an output file name
to save the data to, a row length with which the puzzle has been laid out, and an image
size (length) for all images to be scales to (images are square). 
It returns None.

Output File Numpy Format:
# first index is puzzle num
# row
# col
# length
# length
# color
'''
def jpg_to_np_dataset(infile, outfile, row_len, im_size):
	# load image
	im = imread(infile)
	# split image
	pieces = cut_image(im, im_size)
	# create empty array
	data = np.zeros((1, row_len, int(len(pieces)/row_len), im_size, im_size, 3))
	
	for puzz_idx in range(data.shape[0]):
		for row in range(data.shape[1]):
			for col in range(data.shape[2]):
				data[puzz_idx][row][col] = pieces[row * row_len + col].pixel_data
	
	print("Data shape:", data.shape)
	# save file
	joblib.dump(data, outfile)

def main():
	inf = "puzzle.jpg"
	outf = "datatime!"
	print("Saving Data from %s to %s!" % (inf, outf))
	jpg_to_np_dataset(inf, outf, 1, 200)

if __name__ == "__main__":
	main()
	
	
	
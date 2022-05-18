import joblib
from MachineLearningTeamProject.Jigsaw2Jpeg.jigsaw2jpg import *
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
def jpg_to_np_dataset(infile, outfile, im_size=20):
	# load image
	im = imread(infile)
	# split image
	pieces = cut_image(im, 500, im_size)
	# create empty array
	data = np.zeros((len(pieces), im_size, im_size, 3))
	for i in range(len(pieces)):
		data[i] = pieces[i].pixel_data / 255
	print("Data shape:", data.shape)
	# save file
	if not (outfile is None):
		joblib.dump(data, outfile)
	return data

def main():
	inf = "puzwhite.jpg"
	outf = "puzzle.np"
	print("Saving Data from %s to %s!" % (inf, outf))
	jpg_to_np_dataset(inf, outf, 20)

if __name__ == "__main__":
	main()
	
	
	
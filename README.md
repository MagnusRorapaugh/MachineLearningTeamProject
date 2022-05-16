# MachineLearningTeamProject


## Model Group

### Input
 Our neural network takes as input a nd array with shape (N,l,w,6) where:
 * N = number of pairs of puzzle pieces
 * l = length of each puzzle piece image in pixels
 * w  = width of each puzzle piece image in pixels (this should be a square)
 * 6 the number of color channels, where we assume that each pair of puzzle piece images has RGB channels and the two image are 'stacked'

### Output

 * Our trained model will output a np array with shape (5,) each value in the output will correspond to a binary prediction corresponding to the predicted direction that the two input pieces connect, or if we predict that there is no connection between input pieces. [N, S, E, W, Not Adjacent]
 * EX: [0,1,0,0,0] indicates that the second piece connects to the first piece's south face.

#### Notes:
 * the size of a given puzzle piece is set in stone once the model is trained. As of now, we are planning on training with puzzle pieces that are 200x200. This will size will need to be the same for any input that the model receives. 


## Connection Algorithm Group/Visualization Group

### Input
 We take in:
 * dimention of the puzzle
 * 5-tuples of [N, S, E, W, Not Adjacent] probablilities (0-1) for each peice
 * 3D RGB numpy array of pixels for fragmented image pieces

### Output

 * Visualization window of the images as they are placed into the puzzle board array



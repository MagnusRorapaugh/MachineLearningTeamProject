# DOWNLOAD THE NEW DATA SET!!!
import numpy as np
from PIL import Image
import os
import time as tm

# trims the image to a certain size, with a certain number of pieces in a row, the returns a numpy array where [0][0] is a piece, and 
# contains each pixel in the pieces rgb value. Recommend using a standardized value for dimensions_of_pixels and pieces_in_row so all 
# pieces are the same size and square. dimensions_of_pixels=1000 and pieces_in_row=10 seems to work well, leaves each piece with 
# 100x100 pixels (with 3 rgb values) in a puzzle with 100 pieces, 10x10.
def processImage(name, dimensions_of_pixels, pieces_in_row, pixels_per_piece):
    image = Image.open(name)
    image = image.resize((dimensions_of_pixels,dimensions_of_pixels))
    arr = np.asarray(image)
    
    tiles = np.full((pieces_in_row,pieces_in_row,pixels_per_piece,pixels_per_piece,3),0)
    a = np.split(arr,pieces_in_row,axis=0) #splits image into the appropriately shaped rows
    a = np.array(a)
    for i in range(len(a)):
        tiles[i]=np.split(a[i],pieces_in_row,axis=1) #splits and saves the rows into appropriately shaped columns
    return tiles.astype(np.uint8) #must be type uint8 to show image
    
# runs the methods to gather all the data to train on, for however many sample there are. Make sure the location of the images is in the same 
# place as this program so os.listdir() can grab it. Returns nothing as all puzzle pieces are stored in a directory.
def getSamplePieces():
    dimensions_of_pixels = 1000 #normal example
    pieces_in_row = 5 #normal example
    
    pixels_per_piece = int(dimensions_of_pixels/pieces_in_row)
    path = "Sample_Images/"
    
    files = os.listdir(path)
    for i in files:
        if ".jpeg" not in i and ".jpg" not in i:
            files.remove(i)
    all_images = np.full((len(files), pieces_in_row, pieces_in_row, pixels_per_piece, pixels_per_piece, 3), 0)

    # runs all the images and saves them, this is about 3000 images, so will take a few minutes
    for i in range(len(files)):
        tiles = processImage(path + files[i], dimensions_of_pixels, pieces_in_row, pixels_per_piece)
        all_images[i]=tiles
    return all_images.astype(np.uint8) #must be type uint8 to show image

start_time = tm.time()
all_images= getSamplePieces()
t = tm.time()-start_time
print("Took", int(t/60), "minutes and", "{:.2f}".format(t - 60*int(t/60)), "seconds to gather the training data")

# sample code for getting a specific piece
# print("Puzzle 0, piece in the second row and third column is at all_images[0][1][2], and looks like:")
# image = Image.fromarray(all_images[0][1][2]) 
# image.show()

# Testing code used by the algorithm team
# image = processImage("Model/sample.jpg", 200, 2)
# print(image.reshape((200,200,3)).shape)
# image  = image.reshape((200,200,3))
# image = Image.fromarray(image, 'RGB')
# image.show()


#This function takes as input the coordinates of the two images. 
#It may be decided that we want to extract the coordinates from 
#the filenames in this function instead.
#The function outputs one-hot encodings which are the labels for training.
#Encoding key: [NORTH, SOUTH, EAST, WEST, NOT_ADJACENT]
def labelMaker(img1_X, img1_Y, img2_X, img2_Y):

    #there is an adjacency if side by side but not corner on corner

    #NORTH and SOUTH
    if (img1_X == img2_X):
        if (img1_Y == (img2_Y + 1)):
            #img2 is NORTH of img1
            return [1, 0, 0, 0, 0]
        elif (img1_Y == (img2_Y - 1)):
            #img2 is SOUTH if img1
            return [0, 1, 0, 0, 0]
        elif (img1_Y == img2_Y):
            #ERROR these are equal coordinates
            return Exception
        else:
            #img2 not adjacent to img1 but in same column
            return [0, 0, 0, 0, 1]

    #EAST and WEST
    elif (img1_Y == img2_Y):
        if (img1_X == (img2_X - 1)):
            #img2 is EAST of img1
            return [0, 0, 1, 0, 0]
        elif (img1_X == (img2_X + 1)):
            #img2 is WEST of img1
            return [0, 0, 0, 1, 0]
        else:
            #img2 not adjacent to img1 but in same row
            return [0, 0, 0, 0, 1]

    #not adjacent
    else:
        return [0, 0, 0, 0, 1]

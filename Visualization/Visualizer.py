from PIL import Image
import numpy as np
import cv2
from queue import Queue
import time


class Visualizer:
    def __init__(self):
        # Intializes the data
        self.data = None
        self.piece_shape = None
        self.num_pieces = None
        self.canvas = None
        self.render_dict = None
        self.to_render = Queue()

    # Takes the pieces out from the matrix passed in and adds its image into the render dictionary with its location
    # as key
    def extract_pieces(self):
        # Finds the dimension of the puzzle
        dim1 = self.data.shape[0]
        dim2 = self.data.shape[1]
        # Sets a temporary dictionary for data
        data_dict = {}
        # Loops through the data to get each piece
        for i in range(dim1):
            for j in range(dim2):
                if np.any(self.data[i][j] != 0):
                    data_dict[(i, j)] = self.data[i][j]
        # Sets the render dict with the data gathered
        self.render_dict = data_dict

    # Converts the data into actual images that binds them together
    def gen_photo(self):
        # Generates each photo from render dict
        for pos in self.render_dict:
            # Takes the photo and converts into the right data type
            piece_to_render = self.render_dict[pos]
            piece_to_render = Image.fromarray(piece_to_render.astype(np.uint8))
            # Adds it onto the canvas with its position
            self.canvas.paste(piece_to_render, (int(pos[1] * self.piece_shape), int(pos[0] * self.piece_shape)))
            # Copies the current state of the canvas and adds it to render order
            temp = self.canvas.copy()
            self.to_render.put(temp)

    # Renders the images for visualization
    def render(self):
        # Goes through the rendering list
        while not self.to_render.empty():
            # adds a wait time
            time.sleep(0.5)
            # Gets the image
            img_to_show = self.to_render.get()
            # Uses open CV to show the image
            opencv_image = cv2.cvtColor(np.array(img_to_show), cv2.COLOR_RGB2BGR)
            cv2.imshow("image", opencv_image)
            # keeps the window open until all operations are done by giving a wait time before closing
            k = cv2.waitKey(1000) & 0XFF
            if k == 27:
                break
        # Closes the window
        cv2.destroyAllWindows()
        # resets the canvas
        self.canvas = Image.new('RGB', (
            int(self.piece_shape * self.data.shape[0]), int(self.piece_shape * self.data.shape[1])))

    # Updates the window to reflect the data given
    # Matrix of puzzle pieces is passed in with a size n times 2 plus 1
    def update(self, data):
        # Sets the data
        self.data = data
        # Sets the size of each piece
        self.piece_shape = data.shape[2]
        # Finds the number of pieces
        self.num_pieces = (data.shape[0] + 1) / 2
        # sets the image to be painted
        self.canvas = Image.new('RGB', (
            int(self.piece_shape * self.data.shape[0]), int(self.piece_shape * self.data.shape[1])))
        # Extract pieces function
        self.extract_pieces()
        # Generate photos function
        self.gen_photo()
        # Render function
        self.render()


if __name__ == '__main__':
    # Imports mock data
    mock_data = np.zeros((3, 3, 100, 100, 3))
    mock_data[0, 0] = Image.open('./img1.png')
    mock_data[0, 1] = Image.open('./img2.png')
    mock_data[1, 0] = Image.open('./img3.png')
    mock_data[1, 1] = Image.open('./img4.png')
    mock_data2 = np.zeros((3, 3, 100, 100, 3))
    mock_data2[1, 1] = Image.open('./img1.png')
    mock_data2[2, 2] = Image.open('./img2.png')
    mock_data2[1, 0] = Image.open('./img3.png')
    mock_data2[0, 0] = Image.open('./img4.png')
    vis = Visualizer()
    vis.update(mock_data)
    vis.update(mock_data2)
    for i in range(10):
        if i % 2 == 0:
            vis.update(mock_data)
        else:
            vis.update(mock_data2)

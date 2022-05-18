from PIL import Image, ImageDraw
import numpy as np
import cv2
from queue import Queue
import time


class Visualizer:
    # Initialization
    def __init__(self):
        self.data = None
        self.piece_shape = None
        self.num_pieces = None
        self.canvas = None
        self.render_dict = None
        self.to_render = Queue()
        self.confidence = None

    # Puts each piece into a rendering dictionary
    def extract_pieces(self):
        # Finds the size of the puzzle dimensions
        dim1 = self.data.shape[0]
        dim2 = self.data.shape[1]
        # Temp data
        data_dict = {}
        # Iterates through matrix and adds its position and data into dict
        for i in range(dim1):
            for j in range(dim2):
                if np.any(self.data[i][j] != 0):
                    data_dict[(i, j)] = self.data[i][j]
        self.render_dict = data_dict

    # Generate pictures from render dict and puts it into the queue
    def gen_photo(self):
        for pos in self.render_dict:
            piece_to_render = self.render_dict[pos]
            # Converts array into image
            piece_to_render = Image.fromarray(piece_to_render.astype(np.uint8))
            # Adds the image to canvas
            self.canvas.paste(piece_to_render, (int(pos[1] * self.piece_shape), int(pos[0] * self.piece_shape)))
            draw = ImageDraw.Draw(self.canvas)
            # Adds confidence
            draw.text((int(pos[1] * self.piece_shape) + int(self.piece_shape)-10, int(pos[0] * self.piece_shape)),
                      str(self.confidence[pos[0]][pos[1]]), fill=(255, 0, 0))
            # copies the canvas and puts the copy into a render list
            temp = self.canvas.copy()
            self.to_render.put(temp)

    # Show the updates to the canvas in a new window
    def render(self):
        while not self.to_render.empty():
            # Adds pause
            time.sleep(1)
            img_to_show = self.to_render.get()
            opencv_image = cv2.cvtColor(np.array(img_to_show), cv2.COLOR_RGB2BGR)
            cv2.imshow("image", opencv_image)
            # Make sure all updates are finished
            k = cv2.waitKey(1000) & 0XFF
            if k == 27:
                break

    # code to be called for visualization
    def update(self, data, confidence):
        self.data = data
        self.confidence = confidence
        self.piece_shape = data.shape[2]
        self.num_pieces = (data.shape[0] + 1) / 2
        # generates a new canvas with the right size
        self.canvas = Image.new('RGB', (
            int(self.piece_shape * self.data.shape[0]), int(self.piece_shape * self.data.shape[1])))
        self.extract_pieces()
        self.gen_photo()
        self.render()


if __name__ == '__main__':
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
    confidence = np.array([
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ])
    vis = Visualizer()
    for i in range(2):
        if i % 2 == 0:
            vis.update(mock_data, confidence)
        else:
            vis.update(mock_data2, confidence)

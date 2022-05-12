from PIL import Image
import numpy as np


class Visualizer:
    def __init__(self, data):
        self.data = data
        self.piece_shape = data.shape[2]
        self.num_pieces = (data.shape[0] + 1) / 2
        self.canvas = Image.new('RGB', (
        int(self.piece_shape * self.data.shape[0]), int(self.piece_shape * self.data.shape[1])))
        self.to_render = None

    def extract_pieces(self):
        dim1 = self.data.shape[0]
        dim2 = self.data.shape[1]
        data_dict = {}
        for i in range(dim1):
            for j in range(dim2):
                if np.any(self.data[i][j] != 0):
                    data_dict[(i, j)] = self.data[i][j]
        self.to_render = data_dict

    def render(self):
        for pos in self.to_render:
            piece_to_render = self.to_render[pos]
            piece_to_render = Image.fromarray((piece_to_render * 255).astype(np.uint8))
            print(pos)
            self.canvas.paste(piece_to_render, (int(pos[1] * self.piece_shape), int(pos[0] * self.piece_shape)))
            self.canvas.show()


if __name__ == '__main__':
    mock_data = np.zeros((3, 3, 100, 100, 3))
    mock_data[0, 0] = Image.open('./img1.png')
    mock_data[0, 1] = Image.open('./img2.png')
    mock_data[1, 0] = Image.open('./img3.png')
    mock_data[1, 1] = Image.open('./img4.png')
    vis = Visualizer(mock_data)
    vis.extract_pieces()
    vis.render()

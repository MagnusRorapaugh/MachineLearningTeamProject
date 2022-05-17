from Visualization.Visualizer import Visualizer
import numpy as np
import queue
from piece import Piece
from Model.makePieceNoCSV import processImage
from Model.labelMaker import labelMaker

class PuzzleBuilder:

    def __init__(self):

        # Generate array of pieces

        puzzle_matrix = processImage("../Visualization/1000.jpg", 200, 4, 50)
        self.PUZZLE_WIDTH = 4
        self.PUZZLE_HEIGHT = 4
        self.PIECES = []
        self.vis = Visualizer()

        for i in range(len(puzzle_matrix)):
            for j in range(len(puzzle_matrix[0])):
                new_piece = Piece(puzzle_matrix[i][j], i, j)
                self.PIECES.append(new_piece)

        self.PIECES_IN_PUZZLE_IDX = []  # keep track of pieces in puzzle we build
        self.pieces_to_check_idx = queue.PriorityQueue()  # keep track of pieces we need to check neighbors of
        self.PUZZLE = np.empty((self.PUZZLE_WIDTH * 2, self.PUZZLE_HEIGHT * 2))  # keeps state of puzzle (where each # entry is the index in self.PIECES)
        self.CONFIDENCE = np.full_like(self.PUZZLE)
        for i in range(len(self.PUZZLE)):
            for j in range(len(self.PUZZLE[0])):
                self.PUZZLE[i][j] = -1

    # Implemented by visualization team, called when a new piece is added to the puzzle, sends confidence level too
    def visualize_progress(self):
        self.vis.update(self.get_rgb_state(), self.CONFIDENCE)

    # Neural network simulation
    def nn_compare(self, piece_1, piece_2):
        # Stack pieces into a 200x200x6 numpy array, return a 5-element numpy array
        # stacked_pieces = np.dstack((piece, self.PIECES[i]))

        piece_1_x = piece_1.column_idx
        piece_1_y = piece_1.row_idx
        piece_2_x = piece_2.column_idx
        piece_2_y = piece_2.row_idx
        return labelMaker(piece_1_x, piece_1_y, piece_2_x, piece_2_y)

    # Compares piece to all other pieces and returns a probability table
    def get_probability_table(self, piece):

        # Build comparison table
        table = []
        table_idx = []
        for i in range(len(self.PIECES)):
            if i not in self.PIECES_IN_PUZZLE_IDX:
                # Get results
                results = self.nn_compare(piece, self.PIECES[i])
                table.append(results)
                table_idx.append(i)
        table = np.array(table)
        table_idx = np.array(table_idx)

        return table, table_idx

    # Compare piece to all pieces in puzzle, if neighbor add to puzzle and to queue
    def put_piece_neighbors(self, next_piece_puzzle_idx):

        popped_piece_row_idx = next_piece_puzzle_idx[0]
        popped_piece_column_idx = next_piece_puzzle_idx[1]
        popped_piece_idx = self.PUZZLE[popped_piece_row_idx][popped_piece_column_idx]
        popped_piece = self.PIECES[int(popped_piece_idx)]

        piece_rgb = popped_piece.colors

        # Get maximum probabilities
        probability_table, probability_table_idx = self.get_probability_table(popped_piece)
        max_vals_row_idx = np.argmax(probability_table, axis=0)

        # Highest probability values and associated pieces
        north_max_probability = probability_table[max_vals_row_idx[0]][0]
        north_max_piece_idx = probability_table_idx[max_vals_row_idx[0]]
        north_max_piece = self.PIECES[north_max_piece_idx]

        east_max_probability = probability_table[max_vals_row_idx[2]][2]
        east_max_piece_idx = probability_table_idx[max_vals_row_idx[2]]
        east_max_piece = self.PIECES[east_max_piece_idx]

        south_max_probability = probability_table[max_vals_row_idx[1]][1]
        south_max_piece_idx = probability_table_idx[max_vals_row_idx[1]]
        south_max_piece = self.PIECES[south_max_piece_idx]

        west_max_probability = probability_table[max_vals_row_idx[3]][3]
        west_max_piece_idx = probability_table_idx[max_vals_row_idx[3]]
        west_max_piece = self.PIECES[west_max_piece_idx]

        # If piece passes threshold, add to puzzle
        threshold = 0.8
        row_idx = popped_piece_row_idx
        column_idx = popped_piece_column_idx
        change_made = False
        if north_max_probability > threshold:
            self.PUZZLE[row_idx - 1][column_idx] = north_max_piece_idx
            self.CONFIDENCE[row_idx - 1][column_idx] = north_max_probability
            self.PIECES_IN_PUZZLE_IDX.append(north_max_piece_idx)
            self.pieces_to_check_idx.put((north_max_probability, (row_idx - 1, column_idx)))
            change_made = True
        if east_max_probability > threshold:
            self.PUZZLE[row_idx][column_idx + 1] = east_max_piece_idx
            self.CONFIDENCE[row_idx][column_idx + 1] = east_max_probability
            self.PIECES_IN_PUZZLE_IDX.append(east_max_piece_idx)
            self.pieces_to_check_idx.put((east_max_probability, (row_idx, column_idx + 1)))
            change_made = True
        if south_max_probability > threshold:
            self.PUZZLE[row_idx + 1][column_idx] = south_max_piece_idx
            self.CONFIDENCE[row_idx + 1][column_idx] = south_max_probability
            self.PIECES_IN_PUZZLE_IDX.append(south_max_piece_idx)
            self.pieces_to_check_idx.put((south_max_probability, (row_idx + 1, column_idx)))
            change_made = True
        if west_max_probability > threshold:
            self.PUZZLE[row_idx][column_idx - 1] = west_max_piece_idx
            self.CONFIDENCE[row_idx][column_idx - 1] = west_max_probability
            self.PIECES_IN_PUZZLE_IDX.append(west_max_piece_idx)
            self.pieces_to_check_idx.put((west_max_probability, (row_idx, column_idx - 1)))
            change_made = True

        # If puzzle changed, update visuals
        if change_made:
            self.visualize_progress()

    def solve_puzzle(self):
        rand_idx = np.random.randint(0, len(self.PIECES))  # get random piece
        self.PUZZLE[self.PUZZLE_WIDTH][self.PUZZLE_HEIGHT] = rand_idx  # put in middle of puzzle
        self.CONFIDENCE[self.PUZZLE_WIDTH][self.PUZZLE_HEIGHT] = 1
        self.PIECES_IN_PUZZLE_IDX.append(rand_idx)  # add to list of pieces in puzzle
        self.pieces_to_check_idx.put((0, (self.PUZZLE_WIDTH, self.PUZZLE_HEIGHT)))  # add to queue of pieces to check neighbors

        # work through queue
        while not self.pieces_to_check_idx.empty() and len(self.PIECES_IN_PUZZLE_IDX) < len(self.PIECES):
            pq_output = self.pieces_to_check_idx.get()
            probability = pq_output[0]
            next_piece_puzzle_idx = pq_output[1]
            self.put_piece_neighbors(next_piece_puzzle_idx)
            print(self.get_rgb_state())

        print(self.PUZZLE)

    def get_rgb_state(self):
        # convert state to rgb
        state = []
        for i in range(len(self.PUZZLE)):
            row = []
            for j in range(len(self.PUZZLE)):
                piece_idx = int(self.PUZZLE[i][j])
                if piece_idx != -1:
                    row.append(self.PIECES[piece_idx].colors)
                else:
                    row.append(np.zeros(self.PIECES[0].colors.shape))
            # if len(row) > 0:
            #     state.append(row)
            state.append(row)
        state = np.array(state)
        return state


pb = PuzzleBuilder()
pb.solve_puzzle()
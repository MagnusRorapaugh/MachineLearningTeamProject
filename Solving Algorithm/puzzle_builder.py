
import numpy as np
import queue
from piece import Piece


class PuzzleBuilder:

    def __init__(self):

        self.PUZZLE_WIDTH = 3
        self.PUZZLE_HEIGHT = 4

        # Sample input of shuffled puzzle pieces
        self.PIECES = [[[[50, 50, 50], [10, 10, 10], [200, 200, 200]],
                        [[50, 50, 50], [10, 10, 10], [200, 200, 200]]],  # piece 1
                       [[[75, 75, 75], [15, 15, 15], [225, 225, 225]],
                        [[75, 75, 75], [15, 15, 15], [225, 225, 225]]],  # piece 2
                       [[[25, 25, 25], [100, 100, 100], [40, 40, 40]],
                        [[25, 25, 25], [100, 100, 100], [40, 40, 40]]],  # piece 3
                       [[[40, 40, 40], [90, 90, 90], [100, 100, 100]],
                        [[40, 40, 40], [90, 90, 90], [100, 100, 100]]]]  # piece 4
        self.PIECES = np.array(self.PIECES)

        self.PIECES_IN_PUZZLE_IDX = []  # keep track of pieces in puzzle we build
        self.pieces_to_check_idx = queue.PriorityQueue()  # keep track of pieces we need to check neighbors of
        self.PUZZLE = np.empty((self.PUZZLE_WIDTH * 2, self.PUZZLE_HEIGHT * 2))  # keeps state of puzzle (where each # entry is the index in self.PIECES)

    # Implemented by visualization team, called when a new piece is added to the puzzle
    def visualize_progress(self):
        return

    # Compares piece to all other pieces and returns a probability table
    def get_probability_table(self, piece):

        # Build comparison table
        table = []
        table_idx = []
        for i in range(len(self.PIECES)):
            if i not in self.PIECES_IN_PUZZLE_IDX:
                results = nn.compare(piece, self.PIECES[i])  # where nn is the neural network, results is the probability vector
                table.append(results)
                table_idx.append(i)

        return table, table_idx

    # Compare piece to all pieces in puzzle, if neighbor add to puzzle and to queue
    def put_piece_neighbors(self, p):

        # Get maximum probabilities
        probability_table, probability_table_idx = self.get_probability_table(p.colors)
        max_vals_row_idx = np.argmax(probability_table, axis=0)

        # Highest probability values and associated pieces
        north_max_probability = probability_table[max_vals_row_idx[0]][0]
        north_max_piece_idx = probability_table_idx[max_vals_row_idx[0]]
        north_max_piece = self.PIECES[north_max_piece_idx]
        east_max_probability = probability_table[max_vals_row_idx[1]][1]
        east_max_piece_idx = probability_table_idx[max_vals_row_idx[1]]
        east_max_piece = self.PIECES[east_max_piece_idx]
        south_max_probability = probability_table[max_vals_row_idx[2]][2]
        south_max_piece_idx = probability_table_idx[max_vals_row_idx[2]]
        south_max_piece = self.PIECES[south_max_piece_idx]
        west_max_probability = probability_table[max_vals_row_idx[3]][3]
        west_max_piece_idx = probability_table_idx[max_vals_row_idx[3]]
        west_max_piece = self.PIECES[west_max_piece_idx]

        # If piece passes threshold, add to puzzle
        threshold = 0.8
        row_idx = p.row_idx
        column_idx = p.column_idx
        change_made = False
        if north_max_probability > threshold:
            self.PUZZLE[row_idx + 1][column_idx] = north_max_piece_idx
            self.PIECES_IN_PUZZLE_IDX.append(north_max_piece_idx)
            self.pieces_to_check_idx.put((north_max_probability, Piece(north_max_piece, row_idx + 1, column_idx)))
            change_made = True
        if east_max_probability > threshold:
            self.PUZZLE[row_idx + 1][column_idx] = east_max_piece_idx
            self.PIECES_IN_PUZZLE_IDX.append(east_max_piece_idx)
            self.pieces_to_check_idx.put((east_max_probability, Piece(east_max_piece, row_idx + 1, column_idx)))
            change_made = True
        if south_max_probability > threshold:
            self.PUZZLE[row_idx + 1][column_idx] = south_max_piece_idx
            self.PIECES_IN_PUZZLE_IDX.append(south_max_piece_idx)
            self.pieces_to_check_idx.put((south_max_probability, Piece(south_max_piece, row_idx + 1, column_idx)))
            change_made = True
        if west_max_probability > threshold:
            self.PUZZLE[row_idx + 1][column_idx] = west_max_piece_idx
            self.PIECES_IN_PUZZLE_IDX.append(west_max_piece_idx)
            self.pieces_to_check_idx.put((west_max_probability, Piece(west_max_piece, row_idx + 1, column_idx)))
            change_made = True

        # If puzzle changed, update visuals
        if change_made:
            self.visualize_progress()

    def solve_puzzle(self):
        rand_idx = np.random.randint(0, len(self.PIECES))  # get random piece
        self.PUZZLE[self.PUZZLE_WIDTH][self.PUZZLE_HEIGHT] = rand_idx  # put in middle of puzzle
        self.PIECES_IN_PUZZLE_IDX.append(rand_idx)  # add to list of pieces in puzzle
        self.pieces_to_check_idx.put((0, Piece(self.PIECES[rand_idx], self.PUZZLE_WIDTH, self.PUZZLE_HEIGHT)))  # add to queue of pieces to check neighbors

        # work through queue
        while not self.pieces_to_check_idx.empty():
            next_piece = self.pieces_to_check_idx.get()
            self.put_piece_neighbors(next_piece)


pb = PuzzleBuilder()
pb.solve_puzzle()

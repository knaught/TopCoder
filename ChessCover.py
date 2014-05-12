"""
Author: Kevin Owens
Date: 12 May 2014
Class: Checkers

Problem description summary (from TopCoder Tournament Inv 2001 Semi A+B 1000/362):  Given a chess board with occupied
spaces, identify how many of the spaces are safe from attack.  The board is of size r x c as defined by an array of
equal-length strings, each string representing a row from top-to-bottom.  Each position in a row can be either U for
unoccupied, or one of the chess pieces Q, R, B, K, and P, with K being the knight; there are no kings.  A piece can
appear more than once.  All pieces move in the standard configuration with the exception of the pawn, which can move
one step in any of the four diagonals.

Algorithm:
Iterate over each row and col
    For each unoccupied space
        Travel from piece in authorized manner
        Record each space the piece can legally move to as unsafe
Return count of safe spaces
"""


class ChessCover:

    # Define moves for each piece.  These are given as (x,y) pairs, with x=col, and y=row.
    # The initial True/False value indicates whether the piece can move in a continuous path; False means one step.
    _move_info = {'Q': (True, (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)),
                  'R': (True, (1, 0), (0, -1), (-1, 0), (0, 1)),
                  'B': (True, (1, -1), (-1, -1), (-1, 1), (1, 1)),
                  'K': (False, (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1)),
                  'P': (False, (1, -1), (-1, -1), (-1, 1), (1, 1))}

    def getSafe(self, board):

        """
        The one method required by TopCoder that returns a count of the number of safe spaces on the given board.
        :param board: array of equi-length strings, each string representing a row (top to bottom), each position
            in the row a 'U' for unoccupied or one of the tokens given for each piece (QRBKP).
        :return: the number of spaces on the board that none of the identified pieces can move to
        """

        self._board = board
        self._num_rows = len(board)
        self._num_cols = len(board[0])  # each row is guaranteed to be of the same length
        self._unsafes = {}  # holds positions determined to be unsafe
        num_empty = 0  # count of empty positions determined while traversing the board

        for r in range(self._num_rows):
            for c in range(self._num_cols):

                piece = board[r][c]

                if piece == 'U':
                    num_empty += 1
                    continue

                self._mark_unsafe(piece, (r, c))

        return num_empty - len(self._unsafes)

    def _mark_unsafe(self, piece, pos):

        """
        Marks all positions originating at pos to which piece can move as unsafe by adding them to self._unsafes{}
        :param piece: the piece for which moves are to be checked; piece is a key in self._move_info
        :param pos: the (row, col) of the piece for which moves are being evaluated
        """

        move_info = self._move_info[piece]
        continuous, moves = move_info[0], move_info[1:]

        for move in moves:

            # reset starting position from which to explore moves
            pos_new = pos

            # while the piece can still move
            while pos_new:

                # get its next position given the current move direction
                pos_new = self._next_pos(pos_new, move)

                # if a valid move, then the position is unsafe
                if pos_new:
                    self._unsafes[pos_new] = True

                # if this is a move-once piece, don't move any further in this direction
                if not continuous:
                    break

    def _next_pos(self, pos, move):

        """
        Returns the next position from pos in direction move, or False if the piece can't be moved in the direction.
        :param pos: the (row,col) from which a move is being attempted
        :param move: the (x,y) direction of the move, where x=col, y=row
        :return: the (row,col) of the next position, or False if that position is blocked or out-of-bounds
        """

        # calc new position, translating x-y to y-x
        pos_new = pos[0] + move[1], pos[1] + move[0]

        # out-of-bounds
        if pos_new[0] not in range(self._num_rows) or pos_new[1] not in range(self._num_cols):
            return False

        # unoccupied
        if self._board[pos_new[0]][pos_new[1]] != 'U':
            return False

        # good-to-go
        return pos_new


if __name__ == '__main__':

    boards = (('UU', 'UU'), ('UUUUU', 'UQUQU', 'UUUUUU'), ('UUU', 'UPU', 'UUU'), ('UUUU', 'UUUU', 'QUUU', 'UUUU'),
              ('UUUUUQ', 'UUUUUU', 'BURUUU', 'UUKUUU', 'UUUUUU'), ('UBUKUUUBUU', 'UUUUBUUQUR'))

    cc = ChessCover()

    for board in boards:
        print(cc.getSafe(board), 'safe squares', board)
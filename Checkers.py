"""
Author: Kevin Owens
Date: 10 May 2014
Class: Checkers

Problem description summary (from TopCoder):  Implement a class Checkers with a method compute(pos, positions) that
returns either the cost of moving a red checker piece from a specified position to the other side of the board while
jumping or being blocked by the black pieces at their specified positions, or -1 if the other side is not reachable.
Standard rules for checkers applies.  Red position is specified as an "x,y" coordinate string and black positions are
a collection of "x,y" coordinate strings.  "0,0" is the lower-left corner of the board.  The "other side" of the board
is at row 7.

Implementation notes.  This uses a recursive approach, which isn't terribly efficient as it's written.  But hey, it's
recursive, and everyone likes recursion.
"""


class Checkers:
    _LEFT, _RIGHT = -1, 1  # for readability; used to modify x-coordinate in single-space moves left and right
    _MAX_COST = 7 + 1  # the cost of a blocked or illegal move is given as 1 beyond the max number of moves,
    # guaranteeing it won't be chosen in a min() comparison
    _pos_blacks = ()  # collection of x-y integer coordinate tuples representing positions of black checker pieces

    def compute(self, pos_red, pos_blacks) -> int:

        """
        Using a checker board coordinate system, lower left being (0,0), calculates the fewest number of moves it
        would take to move a red piece from pos_red to the opposite side of the board (:,7), jumping or blocked by
        the black pieces as per the standard rules for checkers.  No other red pieces are specified.

        :param str pos_red: a x-y coord string in the format "x,y" representing the red position
        :param {str} pos_blacks: a collection of x-y coord strings, as in { "x,y", "x,y", "x,y" }, representing black positions
        :return int: fewest number of moves it would take to get from red position to opposite end of board,
                or -1 if the piece is prevented from moving to the last row
        """

        # convert string coords into int coord tuples
        pos_red = tuple([int(xy) for xy in pos_red.split(',')])
        self._pos_blacks = tuple([tuple([int(xy) for xy in coord.split(',')]) for coord in pos_blacks])

        # find the quickest path
        cost = min(self._cost(pos_red, self._LEFT), self._cost(pos_red, self._RIGHT))
        if cost == self._MAX_COST:
            return -1
        else:
            return cost

    def _cost(self, pos, direction, jump=False) -> int:

        """
        Calculates the total cost of moving one step in the specified direction, summing the cost of the one step and
        the minimum cost associated with traversing either left or right from that position.  A sequence of pieces
        that can be jumped in one move has a cost of 1.  Out-of-bounds or blocked moves have a max cost that will lose
        on any min() comparison.

        This is a recursive function that has three base-case conditions causing recursion to stop:
        1. Piece is at the opposite side of the board
        2. Piece is out-of-bounds
        3. Piece is blocked

        Recursion continues by returning the minimum of costs for moving left and right.

        Traversal is left-right.  While not efficient, nodes are revisited and re-costed because their cost depends on
        where the piece came from and where it's going (i.e., the cost of stepping to a pos is different than jumping
        there).

        :param (int) pos: red piece position (x,y) from which left/right moves are being evaluated
        :param (int) direction: direction piece is to move (left = -1; right = 1); added to x-coord
        :param bool jump: true if jumped last move; enables multiple jumps to be treated as a single move
        :return int: minimum cost of moving left or right, or max cost if blocked or out-of-bounds
        """

        # unpack position coords from string to int tuple
        x, y = pos[0], pos[1]
        pos_next = x_next, y_next = x + direction, y + 1

        # at finish: no cost unless last move was a jump
        if y == 7: return jump  # as an int

        # out of bounds: max cost
        if x_next < 0 or x_next > 7: return self._MAX_COST

        # next empty: cost 1 for the step + 1 if terminating jump + min cost of moves left and right
        if pos_next not in self._pos_blacks:
            return 1 + jump + min(self._cost(pos_next, self._LEFT), self._cost(pos_next, self._RIGHT))

        # next occupied: no cost for non-terminal jump + min cost of moves left and right (max cost if blocked)
        else:
            pos_next = x_next + direction, y_next + 1
            if pos_next in self._pos_blacks: return 8  # 2 consecutive blacks (blocked)
            return 0 + min(self._cost(pos_next, self._LEFT, True), self._cost(pos_next, self._RIGHT, True))


if __name__ == '__main__':
    def test(start_pos, pieces):
        print('start_pos:', start_pos, '\npieces:', pieces)
        hops = c.compute(start_pos, pieces)
        print('hops:', hops, '\n')

    c = Checkers()
    test("1,0", {"2,1", "0,3", "4,3", "5,6", "4,2"})  # answer = 3
    test("4,4", {})  # answer = 3
    test("4,4", {"6,6", "5,5", "3,5", "2,6"})  # answer = -1
    test("4,1", {"2,4", "3,4", "4,4", "5,4", "2,6", "3,6", "4,6", "5,6"})  # answer = 3
    test("7,0", {"6,1", "4,3", "2,5"})


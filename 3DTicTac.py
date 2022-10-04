"""
Basic 3D Tic Tac Toe with Minimax and Alpha-Beta pruning, using a simple
heuristic to check for possible winning moves or blocking moves if no better
alternative exists.
"""
from Utils import *

from ast import While
from shutil import move
from colorama import Back, Style, Fore
import numpy as np

class TicTacToe3D(object):
    """3D TTT logic and underlying game state object.

    Attributes:
        board (np.ndarray)3D array for board state.
        difficulty (int): Ply; number of moves to look ahead.
        depth_count (int): Used in conjunction with ply to control depth.

    Args:
        player (str): Player that makes the first move.
        player_1 (Optional[str]): player_1's character.
        player_2 (Optional[str]): player_2's character.
        ply (Optional[int]): Number of moves to look ahead.
    """

   

    def __init__(self, board = None, player=-1, player_1=-1, player_2=1, ply=3):
        if board is not None:
            assert type(board) == np.ndarray, "Board must be a numpy array"
            assert board.shape == (3,3,3), "Board must be 3x3x3"
            self.np_board = board
        else:
            self.np_board = self.create_board()
        self.map_seq_to_ind, self.map_ind_to_seq = self.create_map()
        self.allowed_moves = list(range(pow(3, 3)))
        self.difficulty = ply # steps looking ahead
        self.depth_count = 0
        if player == player_1:
            self.player_1_turn = True
        else:
            self.player_1_turn = False
        self.player_1 = player_1
        self.player_2 = player_2
        self.players = (self.player_1, self.player_2)
        # self.is_terminate = False

    def create_map(self):
        """Create a mapping between index of 3D array and list of sequence, and vice-versa.

        Args: None

        Returns:
            map_seq_to_ind (dict): key: index , value: board coordinate
            map_ind_to_seq (dict): key: board coordinate , value: index
        """
        a = np.hstack((np.zeros(9),np.ones(9),np.ones(9)*2))
        a = a.astype(int)
        b = np.hstack((np.zeros(3),np.ones(3),np.ones(3)*2))
        b = np.hstack((b,b,b))
        b = b.astype(int)
        c = np.array([0,1,2],dtype=int)
        c = np.tile(c,9)
        mat = np.transpose(np.vstack((a,b,c)))
        ind = np.linspace(0,26,27).astype(int)
        map_seq_to_ind = {}
        map_ind_to_seq = {}
        for i in ind:
            map_seq_to_ind[i] = (mat[i][0],mat[i][1],mat[i][2])
            map_ind_to_seq[(mat[i][0],mat[i][1],mat[i][2])] = i
        return map_seq_to_ind, map_ind_to_seq 
    
    def reset(self):
        """Reset the game state."""
        self.allowed_moves = list(range(pow(3, 3)))
        self.np_board = self.create_board()
        self.depth_count = 0

    def max(self):
        maxv = -2
        px = None
        py = None
        pz = None
        result = is_terminate(self.np_board)
        if result is None: #Draw
            return (0,0,0,0)
        elif result == 1:
            return (1,0,0,0)
        elif result == -1:
            return (-1,0,0,0)
        
        player = self.player_2 #1 
        if self.player_1_turn:
            player = self.player_1 #-1
        for i in range(self.np_board.shape[0]):
            for j in range(self.np_board.shape[1]):
                for k in range(self.np_board.shape[2]):
                    if self.np_board[i,j,k] == 0:
                        self.np_board[i,j,k] = player
                        self.player_1_turn = ~self.player_1_turn
                        m,px,py,pz = self.min()
                        if m > maxv:
                            maxv = m
                            px,py,pz = i,j,k
                        self.np_board[i,j,k] = 0

        return maxv,px,py,pz

                        
        
    def min(self):
        minv = 2
        px = None
        py = None
        pz = None
        result = is_terminate(self.np_board)
        if result is None: #Draw
            return (0,0,0,0)
        elif result == 1:
            return (1,0,0,0)
        elif result == -1:
            return (-1,0,0,0)
        
        player = self.player_2 #1 
        if self.player_1_turn:
            player = self.player_1 #-1

        for i in range(self.np_board.shape[0]):
            for j in range(self.np_board.shape[1]):
                for k in range(self.np_board.shape[2]):
                    if self.np_board[i,j,k] == 0:
                        self.np_board[i,j,k] = player
                        m,px,py,pz = self.min()

                        if m < minv:
                            minv = m
                            px,py,pz = i,j,k
                        self.np_board[i,j,k] = 0

        return minv,px,py,pz
            

    @staticmethod
    def create_board():
        """Create the board with appropriate positions and the like

        Returns:
            np_board (numpy.ndarray):3D array with zeros for each position.
        """
        np_board = np.zeros((3,3,3), dtype=int)
        return np_board

    def play_game(self):
        """Primary game loop.

        Until the game is complete we will alternate between computer and
        player turns while printing the current game state.
        """
        while True:
            

            try:
                return self.np_board, self.player_1
            except KeyboardInterrupt:
                print('\n ctrl-c detected, exiting')



if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        '--player', dest='player', help='Player that plays first, 1 or -1',\
                type=int, default=-1, choices=[1,-1]
    )
    parser.add_argument(
        '--ply', dest='ply', help='Number of moves to look ahead', \
                type=int, default=6
    )
    args = parser.parse_args()
    brd,winner = TicTacToe3D(player=args.player, ply=args.ply).play_game()
    print("final board: \n{}".format(brd))
    print("winner: player {}".format(winner))
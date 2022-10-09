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

    def max(self,recursive_count,alpha, beta):
        # print(recursive_count)
        maxv = -2
        px = None
        py = None
        pz = None
        result = is_terminate(self.np_board)
        if recursive_count < self.difficulty:

            if self.player_1_turn:
                player = self.player_1
            else:
                player = self.player_2

            if (result is None): # Tie
                return (0,0,0,0)
            elif result == player:
                return (1,0,0,0)
            elif result == -player:
                return (-1,0,0,0)
                
            # if return is 0, return the maxv
            for i in range(self.np_board.shape[0]):
                for j in range(self.np_board.shape[1]):
                    for k in range(self.np_board.shape[2]):
                        if self.np_board[i,j,k] == 0:
                            self.np_board[i,j,k] = player
                            m,minx,miny,minz = self.min(recursive_count + 1, alpha, beta)
                            if m > maxv:
                                maxv = m
                                px,py,pz = i,j,k
                            self.np_board[i,j,k] = 0

                            if maxv >= beta:
                                return maxv,px,py,pz
                            if maxv > alpha:
                                alpha = maxv 
        
        return maxv,px,py,pz

                        
        
    def min(self,recursive_count,alpha, beta):
        minv = 2
        qx = None
        qy = None
        qz = None
        result = is_terminate(self.np_board)
        if recursive_count < self.difficulty:
            if self.player_1_turn:
                player = self.player_1
            else:
                player = self.player_2

            if result is None: #Tie
                return (0,0,0,0)
            elif result == player:
                return (1,0,0,0)
            elif result == -player:
                return (-1,0,0,0)
            
            for i in range(self.np_board.shape[0]):
                for j in range(self.np_board.shape[1]):
                    for k in range(self.np_board.shape[2]):
                        
                        if self.np_board[i,j,k] == 0:
                            self.np_board[i,j,k] = -player
                            m,maxx,maxy,maxz = self.max(recursive_count + 1,alpha, beta)
                            if m < minv:
                                
                                minv = m
                                qx,qy,qz = i,j,k
                            self.np_board[i,j,k] = 0

                            if minv <= alpha:
                                return minv,qx,qy,qz
                            if minv < beta:
                                alpha = minv 
        return minv,qx,qy,qz
            

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
        Round = 0
        while True:
            
            flag = is_terminate(self.np_board)

            if flag is None:
                print("Draw!!")
                break
            if flag == self.player_1:
                print("Player1 Win")
                return self.np_board, self.player_1
                 
            if flag == self.player_2:
                print("Player2 Win")
                return self.np_board, self.player_2
                
            if self.player_1_turn:
                print('Round',Round,'Player1')
                print(self.np_board)
                Round += 1 
                # player1's turn
                (m, px, py, pz) = self.max(0,-2, 2)
                self.np_board[px, py, pz] = self.player_1
                self.player_1_turn = not self.player_1_turn
                
            else:
                # player2's turn
                print('Round',Round,'Player2')
                print(self.np_board)
                (m, px, py, pz) = self.max(0,-2,2)
                self.np_board[px, py, pz] = self.player_2
                self.player_1_turn = not self.player_1_turn




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
    brd,winner = TicTacToe3D(player=args.player, ply=7).play_game()
    print("final board: \n{}".format(brd))
    print("winner: player {}".format(winner))
from sre_parse import fix_flags
import numpy as np 

def if_line_win(test_line):
    if ((test_line == -1).sum() == test_line.shape[0]):
        return -1 
    elif ((test_line == 1).sum() == test_line.shape[0]):
        return 1
    return 0

def if_plane_win(test_plane):
    # Horizontal Win 
    for row in range(test_plane.shape[0]): 
        test_line = test_plane[row,:]
        flag = if_line_win(test_line)
        if flag != 0:
            return flag
    # Vertical Win 
    for col in range(test_plane.shape[1]): 
        test_line = test_plane[:,col]
        flag = if_line_win(test_line)
        if flag != 0:
            return flag
    # Diagonal Win #1 
    test_line = test_plane[np.arange(test_plane.shape[0]),np.arange(test_plane.shape[0])]
    flag = if_line_win(test_line)
    if flag != 0:
        return flag
    # Diagonal Win #2
    test_line = test_plane[np.arange(test_plane.shape[0]),np.arange(np_board.shape[0])[::-1]]
    flag = if_line_win(test_line)
    if flag != 0:
        return flag
    return 0
               
def is_terminate(board_state):
    # Test three dimensional planes
    if (board_state != 0).sum() == 27:
        return 0
    for i in range(board_state.shape[0]):
        test_plane = board_state[i,:,:]
        flag = if_plane_win(test_plane)
        if flag != 0:
            return flag
    for i in range(board_state.shape[0]):
        test_plane = board_state[:,i,:]
        flag = if_plane_win(test_plane)
        if flag != 0:
            return flag    
    for i in range(board_state.shape[0]):
        test_plane = board_state[:,:,i]
        flag = if_plane_win(test_plane)
        if flag != 0:
            return flag     
    # Test 3D diagonals 4 in total
    test_line = board_state[np.arange(test_plane.shape[0]),np.arange(test_plane.shape[0]),np.arange(test_plane.shape[0])]
    flag = if_line_win(test_line)
    if flag != 0:
        return flag
    test_line = board_state[np.arange(test_plane.shape[0])[::-1],np.arange(test_plane.shape[0]),np.arange(test_plane.shape[0])]
    flag = if_line_win(test_line)
    if flag != 0:
        return flag
    test_line = board_state[np.arange(test_plane.shape[0]),np.arange(test_plane.shape[0])[::-1],np.arange(test_plane.shape[0])]
    flag = if_line_win(test_line)
    if flag != 0:
        return flag
    test_line = board_state[np.arange(test_plane.shape[0]),np.arange(test_plane.shape[0]),np.arange(test_plane.shape[0])[::-1]]
    flag = if_line_win(test_line)
    if flag != 0:
        return flag
    return None   #draw
    
        
        
                    

if __name__ == '__main__':
    # test_plane = np.zeros((3,3), dtype=int)
    # test_plane[0,0] = -1
    # test_plane[2,2] = -1
    # test_plane[0,1] = 1
    # test_plane[1,1] = 1
    # test_plane[2,1] = 1
    np_board = np.zeros((3,3,3), dtype=int)
    np_board[0,0,0] = -1
    np_board[1,1,1] = -1
    np_board[2,2,2] = -1
    print(is_terminate(np_board))
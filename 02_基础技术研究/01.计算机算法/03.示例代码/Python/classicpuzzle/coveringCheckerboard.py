'''
    Created on 2014-1-23

    @author: lingjie
    @name:   covering checkerboard
'''
import sys
import cProfile

def cover(board, lab=1, top=0, left=0, side=None):
    if side is None: side = len(board) 
 
    # Side length of subboard:
    s = side // 2 
 
    # Offsets for outer/inner squares of subboards:
    offsets = (0, -1), (side-1, 0) 
    for dy_outer, dy_inner in offsets:
        for dx_outer, dx_inner in offsets:
            # If the outer corner is not set... 
            if not board[top+dy_outer][left+dx_outer]: 
                # ... label the inner corner: 
                board[top+s+dy_inner][left+s+dx_inner] = lab 
 
    # Next label: 
    lab += 1
    if s > 1:
        for dy in [0, s]:
            for dx in [0, s]: 
                # Recursive calls, if s is at least 2: 
                lab = cover(board, lab, top+dy, left+dx, s) 
 
    # Return the next available label:
    return lab 

def main():
    board = [[0]*8 for i in range(8)] # Eight by eight checkerboard 
    board[7][7] = -1                  # Missing corner 
    cover(board) 
    for row in board:
        print((" %2i"*8) % tuple(row)) 

if(__name__ == "__main__"):
    main()
    cProfile.run("main")
    

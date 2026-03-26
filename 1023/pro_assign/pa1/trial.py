import random
def p():
    
    print(x)
x=2
p()

def check(game_board):
    for i in range(20):
        for j in range(5):
            if game_board[i][j] and i<5:
                return 'Lose'
            if game_board[i][j]==1023 and i>=5:
                return 'Win'
    return'Playing'         


def gravity_and_merge(game_board):
    """
    # Task 8: Gravity and Merge
    # You have to implement the gravity and merging of the blocks on the game board
    # The gravity moves the blocks down as far as possible and works on each individual block by turn, not the entire piece at the same time
    # The merging merges the blocks that have the same value and are stacking vertically
    # Keep the process until no more merging can be done, and no more blocks are floating in the air
    # Keep merging the bottommost pair of blocks with the same value, that is to say, begin merging checks from bottom up, not top down
    """
    ### TASK 8 STARTS HERE ###
    #for each column, we loop through the rows vertically


    def has_duplicates(game_board,col):
        for row in range(19):
            if game_board[row][col]==game_board[row+1][col]:
                return False
        return True
    def gravity(game_board,col):
        for row in range(19,0,-1):
            if not game_board[row][col]:
                game_board[row][col]=game_board[row-1][col]

    def merge(game_board,col):
        for row in range(19,0,-1):
            if game_board[row][col]==game_board[row-1][col]:
                new_value=game_board[row][col]*2+1
                game_board[row][col]=new_value
                game_board[row-1][col]=0

    for col in range(6):
        while(has_duplicates(game_board,col)):
            gravity(game_board,col)
            merge(game_board,col)
   

def gravity(game_board,col):
    #given certain column, we start from the bottom
    bottom=19
    #skip the elements already at the botttom
    while game_board[bottom][col]:
        bottom+=1

    j=bottom
    for i in range(bottom,-1,-1):
        if game_board[i][col]:
            game_board[j][col]=game_board[i][col]
            j-=1
            #since we are going up,we need to minus one


    ### TASK 8 ENDS HERE ###
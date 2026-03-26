import re
"""
COMP 1023 Lab 8: Maze Pathfinding
Student Implementation File

Instructions:
- Implement the three TODO functions below
- DO NOT modify function signatures
- You may add helper functions if needed
- Test your code using maze_tester.py (GUI)
"""

# Direction for reference
DIRECTIONS = ['R', 'L', 'U', 'D']
DELTA = [[1, 0], [-1, 0], [0, -1], [0, 1]]

def parse_maze(maze):
    '''
    Task 1: Parse the maze to extract start, end, and teleporter pairs.
    
    Parameters:
        maze: 2D list of single characters
    
    Returns:
        tuple: (start, end, teleport_info)
            - start: list [x, y] coordinate of 'S'
            - end: list [x, y] coordinate of 'E'  
            - teleport_info: list of information list of paired teleporters, within the format:
                [ ['A', [x1, y1], [x2, y2]], ['B', [x3, y3], [x4, y4]], ...]

    Example:
        maze = [
            ['#', '#', '#', '#'],
            ['#', 'S', 'A', '#'],
            ['#', '1', '2', '#'],
            ['#', 'A', 'E', '#'],
            ['#', '#', '#', '#']
        ]
        Returns: ([1, 1], [2, 3], [['A', [2, 1], [1, 3]]])
    '''
    # TODO: Implement this function
    start=[]
    result=[]
    temp={}
    end=[]
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            cur=maze[i][j]
            if cur=='S':
                start=[i,j]
            elif re.fullmatch('[^SE]',cur):
                if cur in temp:
                    #valid teleport has to appear twice
                    result.append([cur,temp[cur],[i,j]])
                else:
                    temp[cur]=[i,j]
            elif cur=='E':
                end=[i,j]

    return start,end,result
    

def dfs_helper_shortest(maze, end, teleport_info, height, width,
                        current_pos, current_path, visited):
    """
    Task 2: DFS helper recursive function for finding the Shortest Path.

    Parameters:
        maze: 2D list of characters
        end: list [x, y] target position
        teleport_info: [['A', [x1, y1], [x2, y2]], ...]
        height, width: maze dimensions
        current_pos: list [x, y]
        current_path: list of direction chars
        visited: list of positions [x, y] that have been visited

    Return:
        - best_path: list of direction chars for the best path (with lowest steps)
                     that could lead to the end position found in this branch,
                     or empty list if path has not been found
        - example: ['R', 'D', 'L', ...]      
    """

    # Base case: in this branch, we have reached the end position
    # this path is apparently the best path found in this branch
    
    if current_pos == end:
        return current_path[:]

    best_path = []
        
    for direction in DIRECTIONS:
        next_pos = None
        delta = DELTA[DIRECTIONS.index(direction)]

        # TODO: Calculate next_pos using delta
        # ------- Modify the line below -------
        curx,cury=current_pos
        dx,dy=delta
        next_pos=[curx+dx,cury+dy]
        
        # ------- Modify the line above -------

        # TODO: Validate if next_pos is within bounds, not a wall, and not visited
        # ------- Modify the line below -------
        next_x,next_y=next_pos
        if next_x<0 or next_x>=width or next_y<0 or next_y>=height:
            break
        if next_pos in visited or maze[next_x][next_y]=='#':
            break

        # ------- Modify the line above -------

        # TODO: Handle teleporter if next_pos is a teleporter, update next_pos accordingly
        #       and validate if the teleported position is visited again if teleported
        # ------- Modify the line below -------
        ''' teleport_info: [['A', [x1, y1], [x2, y2]], ...] looks like this'''
        for t in teleport_info:
            for i,position in enumerate(t):
                if position==next_pos:
                    if not t[i+1]in visited:
                        next_pos=t[i+1]
                        break
        # ------- Modify the line above ---------

        # TODO: Update visited and current_path, prepare for recursive call
        # ------- Modify the line below -------
        current_path.append(direction)
        visited.append(next_pos)
        # ------- Modify the line above -------

        path = dfs_helper_shortest(maze, end, teleport_info, height, width, 
                                   next_pos, current_path, visited)
        
        if path:
            if (not best_path) or (len(path) < len(best_path)):
                best_path = path

        # TODO: Backtrack - undo changes to visited and current_path
        # ------- Modify the line below -------
        else:
            return None
        # ------- Modify the line above -------

    return best_path

def dfs_helper_max_score(maze, end, teleport_info, height, width,
                         current_pos, current_path, current_score, visited):
    """
    Task 3: DFS helper recursive function for finding the Maximum Score.

    Parameters:
        maze: 2D list of characters
        end: list [x, y] target position
        teleport_info: [['A', [x1, y1], [x2, y2]], ...]
        height, width: maze dimensions
        current_pos: list [x, y]
        current_path: list of direction chars
        current_score: integer, total score accumulated so far
        visited: list of positions [x, y] that have been visited
    
    Return:
        tuple (best_path, max_score):
        - best_path: list of direction chars for the best path (with maximum score)
                     that could lead to the end position found in this branch,
                     or empty list if path has not been found
            - example: ['R', 'D', 'L', ...]
        - max_score: integer, total score of the best_path found,
                     or 0 if no path has been found

    Since the structure is similar to Task 2, we will not provide detailed comments here.
    """

    # TODO: Handle the base case of this function
    # ------- Modify the line below -------
    if current_pos==end:
        return current_path,current_score

    # ------- Modify the line above -------

    best_path = []
    max_score = 0
        
    for direction in DIRECTIONS:
        # TODO: Calculate and validate next_pos
        # ------- Modify the line below -------
        next_pos=None
        delta=delta[DIRECTIONS.index(direction)]
        dx,dy=delta
        curx,cury=current_pos
        next_pos=[curx+dx,cury+dy]
        next_x,next_y=next_pos

        if next_x<0 or next_x>width or next_y<0 or next_y>height:
            break
        if next_pos in visited or maze[next_x][next_y]=='#':
            break

        # ------- Modify the line above -------

        # TODO: Update parameters, do recursive call
        # ------- Modify the line below -------
        
        for t in teleport_info:
            for i,position in enumerate(t):
                if position==next_pos:
                    if not t[i+1]in visited:
                        next_pos=t[i+1]
                        break
                    
        #check if the final position is a digit
        if maze[next_pos[0]][next_pos[1]].isdigit():
            add=int(maze[next_pos[0]][next_pos[1]])
            current_score=current_score+add
       
        current_path.append(direction)
        visited.append(next_pos)
        # ------- Modify the line above -------

        # TODO: Update the best path and maximum score, and do the backtracking
        # ------- Modify the line below -------
        pass
        # ------- Modify the line above -------

    return best_path, max_score

def find_shortest_path_dfs(maze, start, end, teleport_info):
    '''
    Utilize your implemented function to find the shortest path from start to end.
    Already implemented, no need to modify.
    '''
    
    height = len(maze)
    width = len(maze[0])
    
    initial_visited = [start]
    best_solution = dfs_helper_shortest(maze, end, teleport_info, height, width,
                                        start, [], initial_visited)

    if best_solution:
        return (True, best_solution, len(best_solution))
    else:
        return (False, [], None)

def find_max_score_path(maze, start, end, teleport_info):
    '''
    Utilize your implemented function to find the maximum score path from start to end.
    Already implemented, no need to modify.
    '''

    height = len(maze)
    width = len(maze[0])
    
    initial_visited = [start]
    best_solution, max_score = dfs_helper_max_score(maze, end, teleport_info, height, width,
                                                    start, [], 0, initial_visited)
    
    found = bool(best_solution)
    return (found, best_solution, max_score)
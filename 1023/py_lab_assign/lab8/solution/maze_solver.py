"""
COMP 1023 Lab 8: Maze Pathfinding
Sample Solution

This is a reference implementation for all three tasks.
Study this code to understand the concepts, but try to implement
your own solution first!
"""

# Direction mappings for reference
DIRECTIONS = ['R', 'L', 'U', 'D']
DELTA = [[1, 0], [-1, 0], [0, -1], [0, 1]]

def parse_maze(maze):
    '''
    Task 1: Parse the maze to extract start, end, and teleporter pairs.
    
    Strategy:
    1. Scan through all cells to find 'S', 'E', and uppercase letters
    2. Collect all positions for each letter
    3. Create List of teleporter pairs
    '''
    height = len(maze)
    width = len(maze[0])
    
    start = None
    end = None
    teleport_info = []

    # Scan the entire maze
    for y in range(height):
        for x in range(width):
            cell = maze[y][x]
            
            if cell == 'S':
                start = (x, y)
            elif cell == 'E':
                end = (x, y)
            elif cell.isupper() and 'A' <= cell <= 'Z':
                for pair in teleport_info:
                    if pair[0] == cell:
                        pair.append((x, y))
                        break
                else:
                    teleport_info.append([cell, (x, y)])
    
    return (start, end, teleport_info)

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

    if current_pos == end:
        return current_path[:]

    best_path = []
        
    for direction in DIRECTIONS:
        next_pos = None
        delta = DELTA[DIRECTIONS.index(direction)]

        # TODO: Calculate next_pos using delta
        # ------- Modify the line below -------
        dx, dy = delta
        x, y = current_pos
        next_x, next_y = x + dx, y + dy
        next_pos = (next_x, next_y)
        # ------- Modify the line above -------

        # TODO: Validate if next_pos is within bounds, not a wall, and not visited
        # ------- Modify the line below -------
        if (not (0 <= next_y < height and 0 <= next_x < width)) or maze[next_y][next_x] == '#':
            continue
        if next_pos in visited:
            continue
        # ------- Modify the line above -------

        # TODO: Handle teleporter if next_pos is a teleporter, update next_pos accordingly
        #       and validate if the teleported position is visited again if teleported
        # ------- Modify the line below -------
        for pair in teleport_info:
            if next_pos in pair[1:]:
                next_pos = pair[2] if next_pos == pair[1] else pair[1]
                break
        if next_pos in visited:
            continue
        # ------- Modify the line above ---------
        
        # TODO: Update visited and current_path, prepare for recursive call
        # ------- Modify the line below -------
        if next_pos in visited:
            continue
        visited.append(next_pos)
        current_path.append(direction)
        # ------- Modify the line above -------

        path = dfs_helper_shortest(maze, end, teleport_info, height, width, 
                                   next_pos, current_path, visited)
        
        if path:
            if (not best_path) or (len(path) < len(best_path)):
                best_path = path

        # TODO: Backtrack - undo changes to visited and current_path
        # ------- Modify the line below -------
        visited.remove(next_pos)
        current_path.pop()
        # ------- Modify the line above -------

    return best_path

def dfs_helper_max_score(maze, end, teleport_info, height, width,
                         current_pos, current_path, current_score, visited):
    """
    Task 3: DFS helper recursive function for finding the Maximum Score.
    """

    # TODO: Handle the base case of this function
    # ------- Modify the line below -------
    if current_pos == end:
        return current_path[:], current_score # make sure to return a copy
    # ------- Modify the line above -------

    best_path = []
    max_score = 0
        
    for direction in DIRECTIONS:
        # TODO: Calculate and validate next_pos
        # ------- Modify the line below -------
        dx, dy = DELTA[DIRECTIONS.index(direction)]
        x, y = current_pos
        next_x, next_y = x + dx, y + dy
        next_pos = (next_x, next_y)

        if (not (0 <= next_y < height and 0 <= next_x < width)) or maze[next_y][next_x] == '#':
            continue

        if next_pos in visited:
            continue

        for pair in teleport_info:
            if next_pos in pair[1:]:
                next_pos = pair[2] if next_pos == pair[1] else pair[1]
                break
        
        if next_pos in visited:
            continue
        # ------- Modify the line above -------

        # TODO: Update parameters, do recursive call
        # ------- Modify the line below -------
        visited.append(next_pos)
        current_path.append(direction)
        score = int(maze[next_y][next_x]) if maze[next_y][next_x].isdigit() else 0
        new_score = current_score + score

        new_path, new_score = dfs_helper_max_score(maze, end, teleport_info, height, width,
                                       next_pos, current_path, new_score, visited)
        # ------- Modify the line above -------

        # TODO: Update the best path and maximum score, and do the backtracking
        # ------- Modify the line below -------
        if new_path and new_score >= max_score:
            best_path = new_path
            max_score = new_score

        current_path.pop()
        visited.pop()
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
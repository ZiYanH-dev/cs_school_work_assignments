"""
COMP 1023 Lab 8: Maze Core Utilities
Helper functions for maze operations.

Notes:
- Stepping onto a teleporter (A-Z, excluding 'S' and 'E') immediately teleports to its paired cell.
- A valid teleporter letter must appear exactly twice in the maze to form a pair.
- Teleporting does not add an extra step.
"""

# Test mazes with expected solutions
TEST_MAZES = {
    'easy': {
        'maze': """###
#SE#
###""",
        'shortest_length': 1,
        'max_score': 0,
        'name': 'Easy (3×3)'
    },
    
    'medium': {
        'maze': """#####
#S1A#
#2#3#
#A4E#
#####""",
        'shortest_length': 4,
        'max_score': 5,
        'name': 'Medium (5×5)'
    },
    
    'hard': {
        'maze': """#######
#S12#E#
#3#456#
#678#9#
#######""",
        'shortest_length': 6,
        'max_score': 39,
        'name': 'Hard (7×5)'
    },
    
    'complex': {
        'maze': """###########
#S23A4567E#
#1#2##8#90#
#345#67#12#
#89A12#456#
###########""",
        'shortest_length': 10,
        'max_score': 100,
        'name': 'Complex (11×6)'
    },
    
    'no_path': {
        'maze': """#####
#S#E#
#####""",
        'shortest_length': None,
        'max_score': 0,
        'name': 'No Path Test'
    },

    'teleport_fest': {
        'maze': """###########
#S1A2B3C4E#
#1#2##8#90#
#D45#67#1C#
#9B0A1#2D6#
###########""",
        'shortest_length': 6,
        'max_score': 54,
        'name': 'Teleport Fest (11×6, many portals)'
    },

    'labyrinth_xl': {
        'maze': """#######################
#S1A2#34#5B6#798#9D0#E#
#1#2##3#4#25#6##7#8##9#
#A9#8#7#6#5#4#3#2#1#02#
#2#3##4#5#26#7##8#9##1#
#3#4##5#63#7#8##9#1##2#
#9#8##7#6##5#4##3#2##1#
#C1D#2#3##4053625728#9#
#9#1#2##3#4#5##6#7#8#B#
#5#4#3##2#1#0##9#8#7##6#
#6#5#4##3#211#00#938##7#
#1#2##3#4##5#6##7#8##9#
#9#C##7#6##5#4##3#2##1#
#######################""",
        'shortest_length': 38,
        'max_score': 216,
        'name': 'Labyrinth XL'
    }
}

DELTA = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, -1),
    'D': (0, 1)
}


def load_maze_from_string(s):
    """Convert string maze to a rectangular 2D list."""
    lines = s.strip('\n').split('\n')
    rect_lines = [list(line) for line in lines]
    return rect_lines


def get_test_maze(maze_name):
    """Get a test maze by name."""
    if maze_name not in TEST_MAZES:
        raise ValueError(f"Unknown maze: {maze_name}")
    
    data = TEST_MAZES[maze_name]
    maze = load_maze_from_string(data['maze'])
    return maze, data


def validate_path(maze, start, end, teleport_info, path):
    if not path:
        return {
            'valid': start == end,
            'reached_end': start == end,
            'length': 0,
            'score': 0,
            'error': None if start == end else "Empty path"
        }
    
    height = len(maze)
    width = len(maze[0])
    visited = set([tuple(start)])
    pos = start
    score = 0
    
    for i, direction in enumerate(path):
        if direction not in DELTA:
            return {
                'valid': False,
                'reached_end': False,
                'length': i,
                'score': score,
                'error': f"Invalid direction '{direction}' at step {i}"
            }
        
        dx, dy = DELTA[direction]
        x, y = pos
        next_x, next_y = x + dx, y + dy
        
        # Check bounds
        if not (0 <= next_y < height and 0 <= next_x < width):
            return {
                'valid': False,
                'reached_end': False,
                'length': i,
                'score': score,
                'error': f"Move out of bounds at step {i}"
            }
        
        # Check wall
        if maze[next_y][next_x] == '#':
            return {
                'valid': False,
                'reached_end': False,
                'length': i,
                'score': score,
                'error': f"Hit wall at step {i}"
            }
        
        # Apply teleporter
        final_pos = [next_x, next_y]
        for pair in teleport_info:
            if final_pos in pair[1:]:
                final_pos = pair[2] if final_pos == pair[1] else pair[1]
                break
        
        # Check revisit
        if tuple(final_pos) in visited:
            return {
                'valid': False,
                'reached_end': False,
                'length': i,
                'score': score,
                'error': f"Revisited cell {final_pos} at step {i}"
            }
        
        visited.add(tuple(final_pos))
        
        # Update score
        fx, fy = final_pos
        cell = maze[fy][fx]
        if cell.isdigit():
            score += int(cell)
        
        pos = final_pos

    reached_end = (tuple(pos) == tuple(end))

    return {
        'valid': reached_end,
        'reached_end': reached_end,
        'length': len(path),
        'score': score,
        'error': None if reached_end else f"Path ends at {pos}, not at goal {end}"
    }

def apply_move(pos, direction, maze, teleport_info):
    """
    Apply a single move and return new position.
    Returns None if move is invalid.
    """
    if direction not in DELTA:
        return None
    
    dx, dy = DELTA[direction]
    x, y = pos
    nx, ny = x + dx, y + dy
    
    height = len(maze)
    width = len(maze[0])
    
    if not (0 <= ny < height and 0 <= nx < width):
        return None
    
    if maze[ny][nx] == '#':
        return None
    
    final_pos = [nx, ny]
    for pair in teleport_info:
        if final_pos in pair[1:]:
            final_pos = pair[2] if final_pos == pair[1] else pair[1]
            break
    
    return final_pos
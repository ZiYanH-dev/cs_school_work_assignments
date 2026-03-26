# student_code.py

# Available actions:
# 'R' - Move right
# 'L' - Move left  
# 'U' - Move up
# 'D' - Move down


# width,height = 5,5 # Example width and height, will be replaced with actual values as needed

def solve_level_one():
    """
    Level 1: Linear Traversal 
    
    
    Returns: A string containing movement actions like "RRRR"
    
    Strategy: Move right across the single row to visit all positions
    """
    actions = "" # this is the string containing all the movements of the hunter
                 # We will use this string to check the correctness of your code
    
    # --- TODO below ---
    # Hint: When the hunter starts, you're already at the first position (index 0)
    # You need to use a for loop to move.
    # Add the actions to the "actions" string 
    # Only use Move Right action: 'R'
    # to add a single "move right action" to the string, you can use actions = actions + "R"
    # assume that "width" and "height" variables are automatically filled out with the 
    # "width" and the "height" of the map by main_game.py. You can use it/them here.
    # ~5 lines of code should be sufficient.
    pass # REMOVE THIS LINE, WHEN YOU WRITE YOUR CODE

    # --- TODO above ---

    return actions  # return the resulting actions to main_game.py. Don't modify this line



def solve_level_two():
    """
    Level 2: S-Pattern Traversal 
    
    Returns: A string containing movement actions like "RRRRRDLLLLDRRRR"
    
    Strategy: Alternate between right and left movement for each row
    """
    actions = ""

    # --- TODO below ---  
    # Hint: You'll need nested loops and conditional logic
    # Add the actions to the "actions" string 
    # Three possible actions: 'R', 'L', 'D' will be needed.
    # assume that "width" and "height" variables are automatically filled out with the 
    # "width" and the "height" of the map by main_game.py. You can use it/them here.
    # ~15 lines of code should be sufficient.
    pass # REMOVE THIS LINE, WHEN YOU WRITE YOUR CODE
    
    # --- TODO above ---

    return actions # return the resulting actions to main_game.py. Don't modify this line



def solve_level_three():
    """
    Level 3: Spiral Traversal  (Advanced)
    
    Returns: A string containing movement actions in a spiral pattern
    
    Strategy: Process spiral layers from outside to inside using direction tracking
    """
    actions = ""

    # --- TODO below ---    
    # Hint, you'll need to manage boundaries and directions carefully. while loops might be useful.
    # assume that "width" and "height" variables are automatically filled out with the 
    # "width" and the "height" of the map by main_game.py. You can use it/them here.
    # about 30-40 lines of code should be sufficient.
    # Initialize boundaries for the spiral
    pass # REMOVE THIS LINE, WHEN YOU WRITE YOUR CODE

    # --- TODO above ---

    return actions # return the resulting actions to main_game.py. Don't modify this line
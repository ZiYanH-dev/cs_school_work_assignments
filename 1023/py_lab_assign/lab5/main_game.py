# main_game.py
# Main entry point and framework code for the game. Students run this file to start the game.
# Do not modify this file.

import tkinter as tk
import time
import sys
import os
from tkinter import messagebox

import student_code
from student_code import solve_level_one, solve_level_two, solve_level_three

# Anti-cheating: Check if student_code tries to import main_game
def check_for_cheating():
    """Check if student_code.py contains forbidden imports"""
    try:
        with open('student_code.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for forbidden imports
        forbidden_patterns = [
            'import main_game',
            'from main_game',
            '__import__("main_game")',
            '__import__(\'main_game\')',
        ]
        
        for pattern in forbidden_patterns:
            if pattern in content and not content.split(pattern)[0].strip().endswith('#'):
                return f"Forbidden import detected: {pattern}"
        
        return None
    except Exception as e:
        return f"Error checking file: {e}"

# Check for cheating before importing student code
cheat_check = check_for_cheating()
if cheat_check:
    print(f" CHEATING DETECTED: {cheat_check}")
    print("Please remove forbidden imports from student_code.py")
    sys.exit(1)

# --- Color scheme and global settings ---
CELL_SIZE = 80
BG_COLOR = "#5D5252"
GRID_LINE_COLOR = "#A9A9A9"
EMPTY_CELL_COLOR = "#E0E0E0"
PLAYER_COLOR = "#6CAEDD"
TREASURE_COLOR = "#F2CC62"
DUG_CELL_COLOR = "#C75D4E"
TREASURE_TEXT_COLOR = "#363636"
FONT_STYLE = ("Arial", 16, "bold")

# Utility functions
def read_level_data(filename):
    """Read level data from file and return height, width, expected_actions"""
    with open(filename, 'r') as f:
        first_line = f.readline().strip()
        height, width = map(int, first_line.split())
        expected_actions = f.readline().strip()
        return height, width, expected_actions

def is_valid_position(x, y, width, height):
    """Check if position is within bounds"""
    return 0 <= x < width and 0 <= y < height

# --- Level configuration ---
LEVELS = {
    1: {
        "title": "Level 1",
        "gui_file": "data/level1.txt",
        "test_files": ["data/level1_1.txt", "data/level1_2.txt", "data/level1_3.txt", "data/level1_4.txt"],
        "solution_func": solve_level_one
    },
    2: {
        "title": "Level 2", 
        "gui_file": "data/level2.txt",
        "test_files": ["data/level2_1.txt", "data/level2_2.txt", "data/level2_3.txt", "data/level2_4.txt"],
        "solution_func": solve_level_two
    },
    3: {
        "title": "Level 3",
        "gui_file": "data/level3.txt",
        "test_files": ["data/level3_1.txt", "data/level3_2.txt", "data/level3_3.txt", "data/level3_4.txt"],
        "solution_func": solve_level_three
    },
}

class GameTester:
    """Non-GUI version for testing student solutions"""
    def __init__(self, level, test_file):
        self.level_config = LEVELS[level]
        self.level = level
        self.test_file = test_file
        # Load level data from file
        self.load_level_data(test_file)
        
        self.player_pos = [0, 0]
        self.dug_cells = set()
        self.moves_log = []
        self.digs_log = []
    
    def load_level_data(self,test_file):
        """Load level data from Non GUI file."""
        student_code.height, student_code.width, self.correct_action_string = read_level_data(test_file)
        
        self.map_height = student_code.height
        self.map_width = student_code.width
         

    def move_player(self, dx, dy):
        new_x, new_y = self.player_pos[0] + dx, self.player_pos[1] + dy
        if is_valid_position(new_x, new_y, student_code.width, student_code.height):
            self.player_pos = [new_x, new_y]
            self.moves_log.append(f"Moved to ({new_x}, {new_y})")
        else:
            print(f"  Warning: Tried to move out of bounds to ({new_x}, {new_y})")

    def dig_at_current_location(self):
        x, y = self.player_pos
        if (x, y) not in self.dug_cells:
            self.dug_cells.add((x, y))
            self.digs_log.append(f"Dug at ({x}, {y})")
            return True
        return False

    def test_student_code(self, verbose=False):
        """Test student code without GUI"""
        #print(f"\n Testing {self.level_config['title']}...")
        print(f"   Map size: {student_code.height}×{student_code.width}")
        
        # Reset state
        self.player_pos = [0, 0]
        self.dug_cells.clear()
        self.moves_log.clear()
        self.digs_log.clear()

        # Create API instance (not used in string-based approach)
        student_func = self.level_config["solution_func"]
        
        # Set global variable for current data file
        test_files = self.level_config["test_files"]
        student_code.current_data_file = self.test_file
        
        try:
            student_result = student_func()
            
            # Validate result
            result = self.validate_result(student_result, verbose)
            return result
            
        except Exception as e:
            print(f" Error: An error occurred while running your code: {e}")
            return False

    def validate_result(self, student_result, verbose=False):
        """Validate student result by comparing action strings"""
        if verbose:
            print(f"   Execution Log:")
            print(f"   Student returned: '{student_result}'")
            print(f"   Expected: '{self.correct_action_string}'")
        
   
        
        # Compare student result with correct action string
        if student_result == self.correct_action_string:
            print(f"   SUCCESS: Action string matches expected result!")
            return True
        else:
            print(f"   FAILED: Action string does not match.")
            
            # Provide helpful debugging info
            if len(student_result) != len(self.correct_action_string):
                print(f"   Length mismatch: got {len(student_result)}, expected {len(self.correct_action_string)}")
            else:
                # Find first difference
                for i, (got, expected) in enumerate(zip(student_result, self.correct_action_string)):
                    if got != expected:
                        print(f"   First difference at position {i}: got '{got}', expected '{expected}'")
                        break
            return False


class Game:
    """Universal game logic class that can be initialized based on level configuration."""
    def __init__(self, parent_window, level):
        self.parent_window = parent_window
        self.level_config = LEVELS[level]
        self.level = level
        
        # Load level data from file
        self.load_level_data()
        
        # Create a top-level window for the game
        self.window = tk.Toplevel(parent_window)
        self.window.title(f"Treasure Hunt - {self.level_config['title']}")

        self.player_pos = [0, 0]
        self.dug_cells = set()
        
        canvas_width = student_code.width * CELL_SIZE
        canvas_height = student_code.height * CELL_SIZE
        self.canvas = tk.Canvas(self.window, width=canvas_width, height=canvas_height, bg=BG_COLOR)
        self.canvas.pack(pady=20, padx=20)
        
        # Control frame for buttons and speed control
        control_frame = tk.Frame(self.window)
        control_frame.pack(pady=10)
        
        self.run_button = tk.Button(control_frame, text="Run My Code", font=FONT_STYLE, command=self.run_student_code)
        self.run_button.pack(side=tk.LEFT, padx=5)
        
        # Animation speed control
        speed_frame = tk.Frame(control_frame)
        speed_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(speed_frame, text="Animation Speed:", font=("Arial", 10)).pack(side=tk.LEFT)
        self.speed_var = tk.StringVar(value="Normal")
        speed_options = ["Slow", "Normal", "Fast"]
        self.speed_menu = tk.OptionMenu(speed_frame, self.speed_var, *speed_options)
        self.speed_menu.config(font=("Arial", 9))
        self.speed_menu.pack(side=tk.LEFT, padx=5)

        self.draw_grid()
        self.draw_player()
    
    def load_level_data(self):
        """Load level data from the GUI level file."""
        filename = self.level_config["gui_file"]
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                
                # First line: height and width
                h, w = map(int, lines[0].strip().split())
                student_code.height = h
                student_code.width = w                
                # Second line: correct action string
                self.correct_action_string = lines[1].strip()
                
        except FileNotFoundError:
            print(f"Error: {filename} not found.")
           
          
    

    def draw_grid(self):
        self.canvas.delete("all")
        for y in range(student_code.height):
            for x in range(student_code.width):
                x0, y0 = x * CELL_SIZE, y * CELL_SIZE
                x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE
                fill_color = DUG_CELL_COLOR if (x, y) in self.dug_cells else EMPTY_CELL_COLOR
                self.canvas.create_rectangle(x0, y0, x1, y1, outline=GRID_LINE_COLOR, fill=fill_color)
        self.draw_player()

    def draw_player(self):
        self.canvas.delete("player")
        x, y = self.player_pos
        x0, y0 = x * CELL_SIZE + 0.1 * CELL_SIZE, y * CELL_SIZE + 0.1 * CELL_SIZE
        x1, y1 = x0 + 0.8 * CELL_SIZE, y0 + 0.8 * CELL_SIZE
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=PLAYER_COLOR, tags="player", outline=BG_COLOR, width=2)
        self.window.update()

    def move_player(self, dx, dy):
        new_x, new_y = self.player_pos[0] + dx, self.player_pos[1] + dy
        if is_valid_position(new_x, new_y, student_code.width, student_code.height):
            self.player_pos = [new_x, new_y]
            self.draw_player()
            time.sleep(0.1)

    def dig_at_current_location(self):
        x, y = self.player_pos
        # Visual feedback for digging (no treasure value displayed)
        x0, y0 = x * CELL_SIZE, y * CELL_SIZE
        x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE
        dig_rect = self.canvas.create_rectangle(x0, y0, x1, y1, fill=TREASURE_COLOR, outline=GRID_LINE_COLOR)
        self.window.update()
        time.sleep(0.1)
        
        self.canvas.delete(dig_rect)
        self.dug_cells.add((x, y))
        self.draw_grid()
        return True

    def run_student_code(self):
        self.run_button.config(state=tk.DISABLED)
        self.player_pos = [0, 0]
        self.dug_cells.clear()
        self.draw_grid()
        time.sleep(0.1)

        student_func = self.level_config["solution_func"]
        
        # Set global variable for current data file  
        student_code.current_data_file = self.level_config["gui_file"]
        
        try:
            student_result = student_func()  # No parameters needed
            
            # Show what the student returned
            print(f"Student returned action string: '{student_result}'")
            
            self.validate_result(student_result)
        except Exception as e:
            messagebox.showerror("Code Error!", f"An error occurred while running your code:\n{e}", parent=self.window)
        
        self.run_button.config(state=tk.NORMAL)

    def validate_result(self, student_result):
        # First animate the execution of student's action string
        self.animate_action_string(student_result)
        
        # Then check if student result matches expected action string
        if student_result == self.correct_action_string:
            messagebox.showinfo("Congratulations!", 
                f"Challenge successful! Your action string is correct!\n"
                f"Expected: {self.correct_action_string}\n"
                f"Your result: {student_result}")
        else:
            messagebox.showwarning("Try Again", 
                f"Action string is incorrect.\n"
                f"Expected: {self.correct_action_string}\n"
                f"Your result: {student_result}\n"
                f"Length - Expected: {len(self.correct_action_string)}, Yours: {len(student_result)}")
    
    def get_animation_delay(self):
        """Get the delay in milliseconds based on selected speed"""
        speed = self.speed_var.get()
        if speed == "Slow":
            return 0.5
        elif speed == "Fast":
            return 0.1
        else:  # Normal
            return 0.3
    
    def animate_action_string(self, action_string):
        """Animate the execution of the action string step by step"""
        # Reset position and state
        self.player_pos = [0, 0]
        self.dug_cells.clear()
        self.draw_grid()
        
        # Show starting message
        original_title = self.window.title()
        self.window.title("Treasure Hunt - Starting at position (0,0)...")
        
        # Mark starting position as visited
        self.dig_at_current_location()
        time.sleep(0.1)  # Pause to show starting position
        
        self.window.title("Treasure Hunt - Executing your code...")
        time.sleep(0.1)  # Pause before starting
        
        # Execute each action with animation
        animation_delay = self.get_animation_delay()
        for i, action in enumerate(action_string):
            # Show current step
            self.window.title(f"Treasure Hunt - Step {i+1}/{len(action_string)}: Moving '{action}'")
            
            # Execute the action
            moved = False
            if action == 'R':
                moved = self.move_player_animated(1, 0, "RIGHT")
            elif action == 'L':
                moved = self.move_player_animated(-1, 0, "LEFT")
            elif action == 'D':
                moved = self.move_player_animated(0, 1, "DOWN")
            elif action == 'U':
                moved = self.move_player_animated(0, -1, "UP")
            else:
                # Invalid action, show warning but continue
                print(f"Warning: Invalid action '{action}' at position {i}")
                self.window.title(f"Treasure Hunt - Step {i+1}/{len(action_string)}: Invalid action '{action}'")
                time.sleep(animation_delay)
                continue
            
            # Dig at current location after moving
            if moved:
                self.window.title(f"Treasure Hunt - Step {i+1}/{len(action_string)}: Digging...")
                self.dig_at_current_location()
                time.sleep(animation_delay)
        
        # Show completion message
        self.window.title("Treasure Hunt - Execution completed!")
        time.sleep(0.1)  # Final pause
        self.window.title(original_title)  # Reset title
    
    def move_player_animated(self, dx, dy, direction_name):
        """Move player with better animation and boundary checking"""
        new_x, new_y = self.player_pos[0] + dx, self.player_pos[1] + dy
        
        if is_valid_position(new_x, new_y, student_code.width, student_code.height):
            self.player_pos = [new_x, new_y]
            self.draw_player()
            time.sleep(0.1)  # Pause after movement
            return True
        else:
            # Hit boundary - show warning
            print(f"Warning: Cannot move {direction_name} - hit boundary at ({self.player_pos[0]}, {self.player_pos[1]})")
            # Visual feedback for hitting boundary
            self.canvas.create_text(self.map_width * CELL_SIZE // 2, 10, 
                                  text=f"Hit boundary!", 
                                  fill="red", font=("Arial", 12, "bold"), tags="warning")
            self.window.update()
            time.sleep(0.1)
            self.canvas.delete("warning")
            return False

class MainMenu:
    """Enhanced main menu window for level selection with beautiful UI."""
    def __init__(self, root):
        self.root = root
        self.root.title("Treasure Hunt - Level Selection")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Set background color
        self.root.configure(bg="#1a1a2e")
        
        # Create main frame
        main_frame = tk.Frame(root, bg="#1a1a2e")
        main_frame.pack(expand=True, fill="both", padx=30, pady=20)
        
        # Title section with treasure icon
        title_frame = tk.Frame(main_frame, bg="#1a1a2e")
        title_frame.pack(pady=(20, 30))
        
        # Main title with gradient-like effect using multiple labels
        title_label = tk.Label(title_frame, text=" TREASURE HUNT ", 
                              font=("Arial", 28, "bold"), 
                              fg="#ffd700", bg="#1a1a2e")
        title_label.pack(pady=(40, 40))
        # Subtitle
        subtitle_label = tk.Label(title_frame, 
                                 text="Master Loop Patterns & Algorithms", 
                                 font=("Arial", 16, "italic"), 
                                 fg="#87ceeb", bg="#1a1a2e")
        subtitle_label.pack(pady=(1, 20))
        
        # Level buttons container
        buttons_frame = tk.Frame(main_frame, bg="#1a1a2e")
        buttons_frame.pack(expand=True)
        
        # Level button configurations
        level_configs = [
            (1, "Level 1", "#4CAF50", "#45a049"),
            (2, "Level 2", "#2196F3", "#1976D2"),
            (3, "Level 3", "#FF9800", "#F57C00")
        ]
        
        # Create buttons for each level
        self.buttons = {}
        for level_id, title, color, hover_color in level_configs:
            button_container = tk.Frame(buttons_frame, bg="#1a1a2e")
            button_container.pack(pady=8, padx=20, fill="x")
            
            level_button = tk.Button(
                button_container,
                text=title,
                font=("Arial", 14, "bold"),
                fg="black", bg=color,
                activebackground=hover_color,
                activeforeground="black",
                relief="flat", bd=0, height=2,
                cursor="hand2",
                command=lambda l=level_id: self.start_game(l)
            )
            level_button.pack(fill="x", pady=(0, 2))

            # Store button reference and bind events
            self.buttons[level_id] = {
                'button': level_button,
                'normal_color': color,
                'hover_color': hover_color
            }
            level_button.bind("<Enter>", lambda e, lid=level_id: self.on_hover(lid))
            level_button.bind("<Leave>", lambda e, lid=level_id: self.on_leave(lid))
        
    
        # Add a subtle separator line
        separator = tk.Frame(main_frame, height=2, bg="#333366")
        separator.pack(fill="x", pady=(10, 0))
    
    def on_hover(self, level_id):
        """Handle button hover effect"""
        button_info = self.buttons[level_id]
        button_info['button'].configure(bg=button_info['hover_color'])
    
    def on_leave(self, level_id):
        """Handle button leave effect"""
        button_info = self.buttons[level_id]
        button_info['button'].configure(bg=button_info['normal_color'])

    def start_game(self, level):
        Game(self.root, level)


def run_tests(verbose=False):
    """Run all level tests without GUI using multiple test files"""
    print("Running Treasure Hunt Tests (No GUI Mode)")
    print("=" * 50)
    
    all_passed = True
    results = {}
    
    for level_id in sorted(LEVELS.keys()):
        level_config = LEVELS[level_id]
        test_files = level_config["test_files"]
        level_passed = True
        
        print(f"\nLevel {level_id} Testing.",end=" ")
        print(f"running {len(test_files)} test cases...")
        
        for i, test_file in enumerate(test_files):
            print(f"\n   Test Case {i+1}: {test_file}")
            tester = GameTester(level_id, test_file)
            success = tester.test_student_code(verbose)
            level_passed = level_passed and success
            
        results[level_id] = level_passed
        all_passed = all_passed and level_passed
        
        level_status = " PASS" if level_passed else " FAIL"
        print(f"   Level {level_id} Overall: {level_status}")
    
    print("\n" + "=" * 50)
    print(" Final Test Summary:")
    for level_id, success in results.items():
        status = " PASS" if success else " FAIL"
        print(f"   Level {level_id}: {status}")
    
    overall = " ALL TESTS PASSED" if all_passed else " SOME TESTS FAILED"
    print(f"\n Overall Result: {overall}")
    
    return all_passed


if __name__ == "__main__":
    print("Welcome to Treasure Hunt!")
    print("This game will test your loop programming skills.")
    print()
    
    # User mode selection
    while True:
        try:
            mode = input("Select mode:\n1. Text mode (text-based testing)\n2. GUI mode (visual interface)\nEnter 1 or 2: ")
            if mode == "1":
                success = run_tests(verbose=True)
                sys.exit(0 if success else 1)
                break
            elif mode == "2":
                root = tk.Tk()
                app = MainMenu(root)
                root.mainloop()
                break
            else:
                print("Invalid input. Please enter 1 or 2.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}. Please try again.")

# Anti-cheating: Hide classes from module-level access
__all__ = []  # Hide all names from 'from main_game import *'

# Additional protection: Make Game class harder to access
def __getattr__(name):
    if name == 'Game':
        raise AttributeError(" Access to Game class is forbidden for students!")
    raise AttributeError(f"module 'main_game' has no attribute '{name}'")
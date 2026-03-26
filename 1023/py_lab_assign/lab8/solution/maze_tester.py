"""
COMP 1023 Lab 8: Maze Tester GUI
Interactive GUI for testing students' maze solver implementations.

Behavior:
- Single button "Test Your Solution": runs the student's function, reports feedback,
  and ALWAYS animates the returned path (even if wrong or empty).
- During animation:
  * If a move hits a wall/out-of-bounds → show error and stop.
  * If a move revisits a previously visited cell → show error and stop.
  * If the player reaches the goal (E) → compare steps/score with expected if available.
- The header shows expected shortest length and max score on a new line (N/A if not provided).
"""

import tkinter as tk
from tkinter import ttk, messagebox

import maze_core
import maze_solver

# Colors
COLOR_WALL = "#2c3e50"
COLOR_OPEN = "#ecf0f1"
COLOR_START = "#27ae60"
COLOR_END = "#e74c3c"
COLOR_TELEPORT = "#3498db"      # base teleporter color
COLOR_TP_FROM = "#8e44ad"       # highlight for teleporter source (where you step on)
COLOR_TP_TO = "#16a085"         # highlight for teleporter destination (where you appear)
COLOR_VISITED = "#f39c12"
COLOR_PLAYER = "#9b59b6"
COLOR_DIGIT = "#34495e"

CELL_SIZE = 48
PADDING = 18
FONT_CELL = ("Consolas", 16, "bold")
FONT_UI = ("Segoe UI", 10)
ANIM_INTERVAL_MS = 260


class MazeTesterGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("COMP1023 Lab 8 - Maze Pathfinding Tester")
        self.resizable(False, False)

        # State
        self.current_maze_name = 'easy'
        self.current_mode = 'shortest'  # 'shortest' or 'max_score'
        self.maze = None
        self.maze_data = None
        self.start = None
        self.end = None
        self.teleport_info = []
        self.player_pos = None
        self.visited = set()
        self.path = []
        self.path_index = 0
        self.executed_steps = 0
        self.is_animating = False
        self.current_score = 0

        # Teleporter highlights (persist across the whole animation)
        self.tp_from_used = set()
        self.tp_to_used = set()

        # Last test meta (for end-of-animation messaging)
        self.last_found = None  # bool | None

        # UI
        self._build_ui()
        self._load_maze()

    # ---------------- UI ----------------

    def _build_ui(self):
        control = tk.Frame(self, bg="#ecf0f1")
        control.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Mode
        tk.Label(control, text="Mode:", font=FONT_UI, bg="#ecf0f1").grid(row=0, column=0, padx=5, sticky="w")
        self.mode_var = tk.StringVar(value=self.current_mode)
        mode_frame = tk.Frame(control, bg="#ecf0f1")
        mode_frame.grid(row=0, column=1, padx=5, sticky="w")
        tk.Radiobutton(mode_frame, text="Part A: Shortest Path", value='shortest',
                       variable=self.mode_var, command=self._on_mode_change,
                       font=FONT_UI, bg="#ecf0f1").pack(side=tk.LEFT)
        tk.Radiobutton(mode_frame, text="Part B: Max Score", value='max_score',
                       variable=self.mode_var, command=self._on_mode_change,
                       font=FONT_UI, bg="#ecf0f1").pack(side=tk.LEFT, padx=10)

        # Maze select
        tk.Label(control, text="Maze:", font=FONT_UI, bg="#ecf0f1").grid(row=1, column=0, padx=5, pady=6, sticky="w")
        self.maze_var = tk.StringVar(value=self.current_maze_name)
        self.maze_combo = ttk.Combobox(control, textvariable=self.maze_var,
                                       values=list(maze_core.TEST_MAZES.keys()),
                                       state='readonly', width=20, font=FONT_UI)
        self.maze_combo.grid(row=1, column=1, padx=5, pady=6, sticky="w")
        self.maze_combo.bind('<<ComboboxSelected>>', lambda _e: self._load_maze())

        # Buttons (single action)
        btns = tk.Frame(control, bg="#ecf0f1")
        btns.grid(row=2, column=0, columnspan=2, pady=8)
        tk.Button(btns, text="Test Your Solution", width=18, font=FONT_UI, bg="#3498db", fg="white",
                  command=self._on_test_and_visualize).pack(side=tk.LEFT, padx=6)
        tk.Button(btns, text="Reset", width=12, font=FONT_UI, bg="#95a5a6", fg="white",
                  command=self._reset_visualization).pack(side=tk.LEFT, padx=6)

        # Info + canvas + status
        self.info_var = tk.StringVar(value="Select mode and maze, then click 'Test Your Solution'")
        tk.Label(self, textvariable=self.info_var, font=FONT_UI, fg="#2c3e50",
                 bg="white", wraplength=900, justify="left").pack(fill=tk.X, padx=10, pady=(2, 6))

        self.canvas_frame = tk.Frame(self, bg="white")
        self.canvas_frame.pack(padx=10, pady=10)
        self.canvas = None

        self.status_var = tk.StringVar(value="Position: - | Score: - | Steps: -")
        tk.Label(self, textvariable=self.status_var, font=FONT_UI,
                 fg="#7f8c8d", bg="white").pack(padx=10, pady=(0, 10))

    # --------------- Maze load/render ---------------

    def _load_maze(self):
        """Load and render the selected maze; parse S/E/teleport using student code."""
        self.current_maze_name = self.maze_var.get()
        try:
            self.maze, self.maze_data = maze_core.get_test_maze(self.current_maze_name)
        except Exception as e:
            messagebox.showerror("Load Maze Error", f"Failed to load maze '{self.current_maze_name}':\n{e}")
            return

        # Parse using student's parser
        try:
            parsed = maze_solver.parse_maze(self.maze)
            if not isinstance(parsed, tuple) or len(parsed) != 3:
                raise ValueError("parse_maze must return (start, end, teleport_info)")
            self.start, self.end, self.teleport_info = parsed
        except Exception as e:
            messagebox.showerror("Parse Error", f"Error in parse_maze:\n{type(e).__name__}: {e}")
            return

        self._reset_visualization()
        self._create_canvas()
        self._render_maze()

        # Show expected metrics on a new line
        exp_len = self.maze_data.get('shortest_length')
        exp_score = self.maze_data.get('max_score')
        len_str = "N/A" if exp_len is None else str(exp_len)
        score_str = "N/A" if exp_score is None else str(exp_score)
        mode_name = "Shortest Path" if self.current_mode == 'shortest' else "Maximum Score"
        self.info_var.set(
            f"Loaded: {self.maze_data['name']} | Mode: {mode_name}\n"
            f"Expected length: {len_str} | Expected score: {score_str}. "
            f"Click 'Test Your Solution'."
        )

    def _create_canvas(self):
        if self.canvas:
            self.canvas.destroy()
        h = len(self.maze)
        w = len(self.maze[0])
        cw = w * CELL_SIZE + 2 * PADDING
        ch = h * CELL_SIZE + 2 * PADDING
        self.canvas = tk.Canvas(self.canvas_frame, width=cw, height=ch, bg="white", highlightthickness=0)
        self.canvas.pack()

    def _render_maze(self):
        if not self.canvas or not self.maze:
            return
        self.canvas.delete("all")
        h = len(self.maze)
        w = len(self.maze[0])

        for y in range(h):
            for x in range(w):
                x0 = PADDING + x * CELL_SIZE
                y0 = PADDING + y * CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE
                cell = self.maze[y][x]

                # base color
                if cell == '#':
                    color = COLOR_WALL
                elif cell == 'S':
                    color = COLOR_START
                elif cell == 'E':
                    color = COLOR_END
                elif cell.isupper() and cell not in ('S', 'E'):
                    color = COLOR_TELEPORT
                else:
                    color = COLOR_OPEN

                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="#bdc3c7", width=2)

                # visited overlay
                if (x, y) in self.visited and (x, y) not in [self.start, self.end]:
                    self.canvas.create_rectangle(x0 + 3, y0 + 3, x1 - 3, y1 - 3,
                                                 fill=COLOR_VISITED, outline="", stipple="gray50")

                # persistent teleporter highlights
                if (x, y) in self.tp_from_used:
                    self.canvas.create_rectangle(x0 + 4, y0 + 4, x1 - 4, y1 - 4,
                                                 outline=COLOR_TP_FROM, width=4)
                if (x, y) in self.tp_to_used:
                    self.canvas.create_rectangle(x0 + 6, y0 + 6, x1 - 6, y1 - 6,
                                                 outline=COLOR_TP_TO, width=4)

                # text
                if cell.isdigit():
                    self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2,
                                            text=cell, font=FONT_CELL, fill=COLOR_DIGIT)
                elif cell.isupper():
                    self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2,
                                            text=cell, font=FONT_CELL, fill="white")

        # player
        if self.player_pos:
            px, py = self.player_pos
            px0 = PADDING + px * CELL_SIZE + 10
            py0 = PADDING + py * CELL_SIZE + 10
            px1 = px0 + CELL_SIZE - 20
            py1 = py0 + CELL_SIZE - 20
            self.canvas.create_oval(px0, py0, px1, py1, fill=COLOR_PLAYER, outline="white", width=3)

        steps = len([p for p in self.visited if p != self.start])
        self.status_var.set(f"Position: {self.player_pos or '-'} | Score: {self.current_score} | Steps: {steps}")

    # --------------- Events ---------------

    def _on_mode_change(self):
        self.current_mode = self.mode_var.get()
        self._load_maze()

    def _on_test_and_visualize(self):
        """Run student's function and always animate the returned path."""
        if not self.maze:
            return
        self._reset_visualization()

        try:
            if self.current_mode == 'shortest':
                result = maze_solver.find_shortest_path_dfs(self.maze, self.start, self.end, self.teleport_info)
            else:
                result = maze_solver.find_max_score_path(self.maze, self.start, self.end, self.teleport_info)

            if result is None or len(result) != 3:
                raise ValueError("Function must return (found, path, value)")

            found, path, value = result
            self.last_found = bool(found)
            self.path = list(path or [])

            # Validate for feedback (we will animate regardless)
            validation = maze_core.validate_path(self.maze, self.start, self.end, self.teleport_info, self.path) \
                if self.path else {
                    'valid': (self.start == self.end),
                    'reached_end': (self.start == self.end),
                    'length': 0,
                    'score': 0,
                    'error': None if self.start == self.end else "Empty path"
                }

            # Feedback line
            expected_key = 'shortest_length' if self.current_mode == 'shortest' else 'max_score'
            expected_value = self.maze_data.get(expected_key)
            actual_value = validation['length'] if self.current_mode == 'shortest' else validation['score']
            mode_name = "Shortest Path" if self.current_mode == 'shortest' else "Maximum Score"

            header = f"[Test] Mode: {mode_name}. "
            if not found:
                self.info_var.set(header + "No solution (found=False). Starting animation.")
            else:
                if not validation['valid']:
                    self.info_var.set(header + f"Returned path is invalid: {validation['error']}. Starting animation.")
                else:
                    if expected_value is None:
                        self.info_var.set(header + f"Valid path. Result: {actual_value}. Starting animation.")
                    else:
                        verdict = "Correct" if actual_value == expected_value else "Not optimal"
                        self.info_var.set(header + f"{verdict}. Your: {actual_value}, Expected: {expected_value}. Starting animation.")

            # Start animation
            self.is_animating = True
            if len(self.path) == 0:
                self._finalize_animation(completed=False, reason="Empty path")
                return
            self._animate_step()

        except NotImplementedError:
            task = "find_shortest_path_dfs" if self.current_mode == 'shortest' else "find_max_score_path"
            messagebox.showinfo("Not Implemented", f"{task} is not implemented yet.")
        except Exception as e:
            messagebox.showerror("Error", f"Error during testing:\n{type(e).__name__}: {e}")

    # --------------- Animation ---------------

    def _animate_step(self):
        """Animate one step; stop on error or reaching goal."""
        if self.path_index >= len(self.path):
            self.is_animating = False
            self._finalize_animation(completed=True, reason=None)
            return

        move = self.path[self.path_index]

        # Validate direction token
        if move not in maze_core.DELTA:
            self.is_animating = False
            self._render_maze()
            messagebox.showerror("Invalid Move", f"Invalid direction '{move}' at step {self.path_index}.")
            self.info_var.set(f"Animation stopped: invalid direction at step {self.path_index}.")
            return

        # Compute next step with teleporter awareness (to color from/to)
        dx, dy = maze_core.DELTA[move]
        x, y = self.player_pos
        nx, ny = x + dx, y + dy

        height = len(self.maze)
        width = len(self.maze[0])

        # Bounds and wall checks
        if not (0 <= ny < height and 0 <= nx < width) or self.maze[ny][nx] == '#':
            self.is_animating = False
            self._render_maze()
            messagebox.showerror("Hit Wall", f"Hit wall or out of bounds at step {self.path_index} with move '{move}'.")
            self.info_var.set(f"Animation stopped: hit wall/out of bounds at step {self.path_index}.")
            return

        final_pos = (nx, ny)
        # Teleport highlight if applicable (persist highlight)
        for pair in self.teleport_info:
            if final_pos in pair[1:]:
                src = final_pos
                dst = pair[2] if final_pos == pair[1] else pair[1]
                self.tp_from_used.add(src)
                self.tp_to_used.add(dst)
                final_pos = dst
                break

        # Revisit check
        if final_pos in self.visited:
            self.is_animating = False
            self._render_maze()
            messagebox.showerror("Revisited Cell", f"Revisited cell {final_pos} at step {self.path_index}.")
            self.info_var.set(f"Animation stopped: revisited a previously visited cell at step {self.path_index}.")
            return

        # Apply move
        self.player_pos = final_pos
        self.visited.add(final_pos)
        self.executed_steps += 1
        fx, fy = final_pos
        cell = self.maze[fy][fx]
        if cell.isdigit():
            self.current_score += int(cell)

        self.path_index += 1
        self._render_maze()

        # Stop immediately if reached goal
        if self.player_pos == self.end:
            self.is_animating = False
            self._finalize_animation(completed=True, reason="Reached goal")
            return

        self.after(ANIM_INTERVAL_MS, self._animate_step)

    def _finalize_animation(self, completed: bool, reason: str | None):
        """Finalize: compare results if at goal; otherwise show where it ended."""
        metric_name = "steps" if self.current_mode == 'shortest' else "score"
        actual_steps = self.executed_steps
        actual_value = actual_steps if self.current_mode == 'shortest' else self.current_score

        expected_key = 'shortest_length' if self.current_mode == 'shortest' else 'max_score'
        expected_value = self.maze_data.get(expected_key, None)
        reached_end = (self.player_pos == self.end)

        if reached_end:
            if expected_value is None:
                self.info_var.set(f"Reached goal. Your {metric_name}: {actual_value} (no expected value).")
                messagebox.showinfo("Result",
                                    f"Reached goal.\nYour {metric_name}: {actual_value}\n"
                                    f"No expected value provided for this maze.")
            else:
                if actual_value == expected_value:
                    self.info_var.set(f"Reached goal. Correct {metric_name}: {actual_value}.")
                    messagebox.showinfo("Correct", f"Reached goal. Correct {metric_name}: {actual_value}.")
                else:
                    label = "steps" if self.current_mode == 'shortest' else "points"
                    self.info_var.set(f"Reached goal. Your {label}: {actual_value}, Expected: {expected_value}.")
                    messagebox.showwarning("Not Optimal",
                                           f"Reached goal but not optimal.\n"
                                           f"Your {label}: {actual_value}\nExpected: {expected_value}")
        else:
            # Not at goal (empty path or ended somewhere else)
            if self.last_found is False:
                # Proper "no solution" message instead of an error
                self.info_var.set("No solution (your function returned found=False).")
                messagebox.showinfo("No Solution", "Your function reported: no solution.")
            else:
                end_reason = reason or "Path ended before reaching the goal."
                self.info_var.set(f"{end_reason} Final position: {self.player_pos}, Goal: {self.end}.")
                messagebox.showwarning("Did Not Reach Goal",
                                       f"{end_reason}\nFinal position: {self.player_pos}\nGoal: {self.end}")

        # status refresh
        self._render_maze()

    # --------------- Helpers ---------------

    def _reset_visualization(self, render: bool = True):
        """Reset animation state and (optionally) redraw."""
        self.player_pos = self.start
        self.visited = set([self.start]) if self.start else set()
        self.path_index = 0
        self.executed_steps = 0
        self.is_animating = False
        self.current_score = 0
        self.tp_from_used.clear()
        self.tp_to_used.clear()
        if render and self.canvas:
            self._render_maze()


def main():
    print("=" * 60)
    print("COMP 1023 Lab 8 - Maze Pathfinding Tester")
    print("=" * 60)
    print("Starting GUI...")
    print("Make sure you have implemented parse_maze() first!\n")

    app = MazeTesterGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
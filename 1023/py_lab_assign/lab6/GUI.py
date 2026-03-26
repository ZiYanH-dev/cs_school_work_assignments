# =============================================================================
# COMP 1023 - Lab 6: UST Course Planner
# GUI Wrapper for Student Code
#
# Description:
# This GUI program calls the code completed by students in skeleton files
# Students need to complete the tasks in skeleton/lab6_v4_student_skeleton.py first
# Then they can test their implementation through this GUI interface
# =============================================================================

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sys
import os

# Import lab6 functions
from lab6 import (
    task_1_add_course, 
    task_2_drop_course, 
    task_3_view_slice, 
    create_empty_schedule, 
    get_all_courses,
    course_exists
)


class StudentCodeGUI:
    """
    This GUI wrapper allows students to test their code completed in skeleton
    
    Architecture description:
    - Data structure weekly_schedule is same as in skeleton
    - Core logic calls student-implemented code segments
    - GUI only handles interface display and user interaction
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("HKUST Course Planner")
        self.root.geometry("950x750")
        self.root.resizable(True, True)
        
        # Initialize schedule data structure using lab6_functions
        self.weekly_schedule = create_empty_schedule()
        
        # Define constants (same as in skeleton)
        self.DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        self.TIME_SLOTS = ["Slot 1\n8:30-10:00", "Slot 2\n10:30-12:00", 
                          "Slot 3\n14:00-15:30", "Slot 4\n16:00-17:30"]
        
        # Color configuration
        self.COLORS = {
            'primary': '#1e3a8a',
            'secondary': '#3b82f6',
            'success': '#10b981',
            'danger': '#ef4444',
            'warning': '#f59e0b',
            'empty': '#f3f4f6',
            'occupied': '#dbeafe',
            'border': '#d1d5db',
            'student': '#8b5cf6'
        }
        
        self.setup_ui()
        self.update_schedule_display()
        
        # Show welcome message
        self.show_welcome()
    
    def show_welcome(self):
        """Show welcome and description information"""
        welcome_msg = """
🎓 Welcome to Student Code Tester!

This program will use your code from 
lab6.py to implement features.

Please ensure you have completed:

✓ Task 1B: Add course with conflict detection
✓ Task 2: Drop course logic
✓ Task 3: View slice implementation

Now you can test your code through this GUI!
"""
        messagebox.showinfo("Welcome", welcome_msg)
    
    def setup_ui(self):
        """Setup user interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Title bar
        title_frame = tk.Frame(self.root, bg=self.COLORS['student'], height=90)
        title_frame.pack(fill=tk.X, padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="🎓 UST Course Planner - Student Code Tester",
            font=("Arial", 24, "bold"),
            bg=self.COLORS['student'],
            fg='white',
            justify=tk.CENTER
        )
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(
            title_frame,
            text="Testing your implementation from skeleton file",
            font=("Arial", 14, "italic"),
            bg=self.COLORS['student'],
            fg='#e9d5ff'
        )
        subtitle_label.pack()
        
        # Main content area
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left side: schedule display area
        schedule_frame = tk.LabelFrame(
            main_frame,
            text="📅 Weekly Schedule",
            font=("Arial", 18, "bold"),
            bg='white',
            fg=self.COLORS['student'],
            padx=10,
            pady=10
        )
        schedule_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Create schedule grid
        self.create_schedule_grid(schedule_frame)
        
        # Right side: control panel
        control_frame = tk.LabelFrame(
            main_frame,
            text="⚙️ Function Testing",
            font=("Arial", 18, "bold"),
            bg='white',
            fg=self.COLORS['student'],
            padx=15,
            pady=15
        )
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # Create buttons
        self.create_control_buttons(control_frame)
        
        # Bottom status bar
        status_frame = tk.Frame(self.root, bg=self.COLORS['student'], height=35)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready | Test your code with GUI",
            font=("Arial", 14),
            bg=self.COLORS['student'],
            fg='white',
            anchor=tk.W,
            padx=10
        )
        self.status_label.pack(fill=tk.X)
    
    def create_schedule_grid(self, parent):
        """Create schedule grid"""
        grid_frame = tk.Frame(parent, bg='white')
        grid_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create table header
        tk.Label(
            grid_frame, 
            text="", 
            font=("Arial", 14, "bold"),
            bg='white',
            width=8
        ).grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        
        for col, time_slot in enumerate(self.TIME_SLOTS):
            tk.Label(
                grid_frame,
                text=time_slot,
                font=("Arial", 12, "bold"),
                bg=self.COLORS['student'],
                fg='white',
                relief=tk.RAISED,
                borderwidth=2
            ).grid(row=0, column=col+1, padx=2, pady=2, sticky="nsew")
        
        # Create schedule cells
        self.cells = {}
        for row in range(5):
            day_label = f"{self.DAYS[row]}"
            tk.Label(
                grid_frame,
                text=day_label,
                font=("Arial", 14, "bold"),
                bg=self.COLORS['student'],
                fg='white',
                relief=tk.RAISED,
                borderwidth=2
            ).grid(row=row+1, column=0, padx=2, pady=2, sticky="nsew")
            
            for col in range(4):
                cell = tk.Label(
                    grid_frame,
                    text="---",
                    font=("Arial", 14),
                    bg=self.COLORS['empty'],
                    relief=tk.SUNKEN,
                    borderwidth=2,
                    cursor="hand2"
                )
                cell.grid(row=row+1, column=col+1, padx=2, pady=2, sticky="nsew", ipadx=10, ipady=15)
                cell.bind("<Button-1>", lambda e, r=row, c=col: self.cell_clicked(r, c))
                self.cells[(row, col)] = cell
        
        for i in range(5):
            grid_frame.grid_columnconfigure(i+1, weight=1)
        for i in range(6):
            grid_frame.grid_rowconfigure(i, weight=1)
    
    def create_control_buttons(self, parent):
        """Create control buttons"""
        button_config = {
            'font': ("Arial", 14),
            'width': 22,
            'height': 2,
            'cursor': 'hand2',
            'relief': tk.RAISED,
            'borderwidth': 2
        }
        
        # Description label
        info_label = tk.Label(
            parent,
            text="Test Your Tasks",
            font=("Arial", 16, "bold"),
            fg='black',
            bg='white'
        )
        info_label.pack(pady=(0, 15))
        
        # Task 1: add course button
        add_btn = tk.Button(
            parent,
            text="📝 Task 1B: Add Course ",
            bg=self.COLORS['success'],
            fg='black',
            activebackground='#059669',
            command=self.test_add_course,
            **button_config
        )
        add_btn.pack(pady=8, fill=tk.X)
        
        # Task 2: drop course button
        drop_btn = tk.Button(
            parent,
            text="🗑️ Task 2: Drop Course",
            bg=self.COLORS['danger'],
            fg='black',
            activebackground='#dc2626',
            command=self.test_drop_course,
            **button_config
        )
        drop_btn.pack(pady=8, fill=tk.X)
        
        # Task 3: view slice button
        view_btn = tk.Button(
            parent,
            text="👁️ Task 3: View Slice",
            bg=self.COLORS['warning'],
            fg='black',
            activebackground='#d97706',
            command=self.test_view_slice,
            **button_config
        )
        view_btn.pack(pady=8, fill=tk.X)
        
        # Separator line
        separator = ttk.Separator(parent, orient='horizontal')
        separator.pack(pady=15, fill=tk.X)
        
        # Utility functions
        tk.Label(
            parent,
            text="Utilities",
            font=("Arial", 16, "bold"),
            fg='black',
            bg='white'
        ).pack(pady=(5, 10))
        
        # Clear button
        clear_btn = tk.Button(
            parent,
            text="🔄 Clear Schedule",
            bg='#6b7280',
            fg='black',
            activebackground='#4b5563',
            command=self.clear_schedule,
            **button_config
        )
        clear_btn.pack(pady=5, fill=tk.X)
        
    
    def cell_clicked(self, day, slot):
        """Cell click event"""
        course = self.weekly_schedule[day][slot]
        day_name = f"{self.DAY_NAMES_CN[day]} ({self.DAYS[day]})"
        time_slot = self.TIME_SLOTS[slot]
        
        info = f"Location: {day_name}\nTime: {time_slot}\n\n"
        
        if course:
            info += f"Course: {course}"
            messagebox.showinfo("Course Info", info)
        else:
            info += "Status: Empty"
            messagebox.showinfo("Slot Info", info)
    
    def update_schedule_display(self):
        """Update schedule display"""
        for row in range(5):
            for col in range(4):
                course = self.weekly_schedule[row][col]
                cell = self.cells[(row, col)]
                
                if course is None:
                    cell.config(
                        text="---",
                        bg=self.COLORS['empty'],
                        fg='#9ca3af'
                    )
                else:
                    cell.config(
                        text=course,
                        bg=self.COLORS['occupied'],
                        fg=self.COLORS['primary'],
                        font=("Arial", 14, "bold")
                    )
    
    # ========== uses the functions written by the students
    
    def course_exists(self, course_code):
        """
        Task 1A implementation - wrapper for lab6_functions
        """
        return course_exists(self.weekly_schedule, course_code)
    
    def test_add_course(self):
        """
        Test Task 1B: Add course (with conflict detection)
        This simulates the logic students should implement
        """
        # Get input
        code = simpledialog.askstring("Enter Course Code", "Enter course code:")
        if not code:
            return
        
        code = code.strip().upper()
        
        # Use provided course_exists function to check
        if self.course_exists(code):
            messagebox.showerror(
                "Error",
                f"Error: Course '{code}' already exists in the schedule. Please drop it first."
            )
            return
        
        # Get number of time slots
        num_slots_str = simpledialog.askstring(
            "Number of Time Slots",
            "Enter number of time slots (1 or 2):"
        )
        if not num_slots_str:
            return
        
        try:
            num_slots = int(num_slots_str)
            if num_slots not in [1, 2]:
                raise ValueError()
        except:
            messagebox.showerror("Error", "Invalid input!")
            return
        
        # Collect time slot information
        slots_to_add = []
        for i in range(num_slots):
            day_idx_str = simpledialog.askstring(
                f"Time Slot #{i+1}",
                f"For slot #{i+1}:\nEnter day index (0-4):\n0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri"
            )
            if day_idx_str is None:
                return
            
            slot_idx_str = simpledialog.askstring(
                f"Time Slot #{i+1}",
                f"For slot #{i+1}:\nEnter time slot index (0-3):"
            )
            if slot_idx_str is None:
                return
            
            try:
                day_idx = int(day_idx_str)
                slot_idx = int(slot_idx_str)
                
                if 0 <= day_idx < 5 and 0 <= slot_idx < 4:
                    slots_to_add.append([day_idx, slot_idx])
                else:
                    messagebox.showerror("Error", "Invalid index!")
                    return
            except:
                messagebox.showerror("Error", "Invalid input!")
                return
        
        # ========== Call lab6_functions Task 1B ==========
        # Use the task function from lab6_functions
        success, message, self.weekly_schedule = task_1_add_course(self.weekly_schedule, code, slots_to_add)
        added_successfully = success
        
        # showing the result
        if added_successfully:
            self.update_schedule_display()
            self.update_status(f"✓ Task 1B Test Successful! Course '{code}' added")
            messagebox.showinfo(
                "Success",
                f"{message}\n\n✓ Task 1B Logic Correct!\nCourse '{code}' successfully added."
            )
        else:
            messagebox.showerror(
                "Error",
                f"{message}"
            )
    
    def test_drop_course(self):
        """
        Test Task 2: Drop course
        """
        # Get all courses using lab6_functions
        courses = get_all_courses(self.weekly_schedule)
        
        if not courses:
            messagebox.showinfo("Info", "No courses in schedule.")
            return
        
        # Let user select course to drop
        course_list = "\n".join(courses)
        code_to_drop = simpledialog.askstring(
            "Drop Course",
            f"Available courses:\n\n{course_list}\n\nEnter course code to drop:"
        )
        
        if not code_to_drop:
            return
        
        code_to_drop = code_to_drop.strip().upper()
        
        # ========== Call lab6_functions Task 2 ==========
        # Use the task function from lab6_functions
        found_and_dropped, message, self.weekly_schedule = task_2_drop_course(self.weekly_schedule, code_to_drop)
        
        # showing the result
        if found_and_dropped:
            self.update_schedule_display()
            self.update_status(f"✓ Task 2 Test Successful! Course '{code_to_drop}' dropped")
            messagebox.showinfo(
                "Success",
                f"{message}\n\n✓ Task 2 Logic Correct!\nAll time slots for '{code_to_drop}' have been removed."
            )
        else:
            messagebox.showerror(
                "Error",
                f"{message}"
            )
    
    def test_view_slice(self):
        """
        Testing Task 3
        """
        # get the start day and end day
        start_day_str = simpledialog.askstring(
            "Start Day",
            "Enter start day index (0-4):\n0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri"
        )
        if start_day_str is None:
            return
        
        end_day_str = simpledialog.askstring(
            "End Day",
            "Enter end day index (must be >= start_day, up to 4):"
        )
        if end_day_str is None:
            return
        
        try:
            start_day = int(start_day_str)
            end_day = int(end_day_str)
        except:
            messagebox.showerror("Error", "Invalid input!")
            return
        
        # ========== Call lab6_functions Task 3 ==========
        # Use the task function from lab6_functions
        success, result_text = task_3_view_slice(self.weekly_schedule, start_day, end_day)
        
        if success:
            self.update_status(f"✓ Task 3 Test Successful! Displayed days {start_day} to {end_day-1}")
            messagebox.showinfo(
                "Schedule Slice",
                result_text + "\n✓ Task 3 Logic Correct!"
            )
        else:
            messagebox.showerror(
                "Error",
                result_text
            )
    
    def clear_schedule(self):
        """Clear schedule"""
        result = messagebox.askyesno(
            "Confirm",
            "Clear all courses?"
        )
        if result:
            self.weekly_schedule = create_empty_schedule()
            self.update_schedule_display()
            self.update_status("Schedule cleared")
    
    def update_status(self, message):
        """Update status bar"""
        self.status_label.config(text=message)
        self.root.after(8000, lambda: self.status_label.config(text="Ready"))


def main():
    """Main function"""
    root = tk.Tk()
    app = StudentCodeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()


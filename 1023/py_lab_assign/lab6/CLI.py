# =============================================================================
# COMP 1023 - Lab 6: UST Course Planner - CLI Interface
# 
# Description:
# This file provides a command-line interface for testing the pure functions
# defined in lab6.py
# =============================================================================

from lab6 import (
    print_schedule,
    course_exists,
    create_empty_schedule,
    get_all_courses,
    task_1_add_course,
    task_2_drop_course,
    task_3_view_slice,
    DAYS
)

def main():
    """Main CLI program loop."""
    # Initialize the schedule
    weekly_schedule = create_empty_schedule()
    
    print("=================================================================")
    print("UST Course Planner - CLI Interface")
    print("=================================================================")
    print_schedule(weekly_schedule)
    print()

    while True:
        print("Welcome to the UST Course Planner")
        print("Please choose an option:")
        print("1. Add a Course to Schedule (1-2 slots)")
        print("2. Drop a Course from Schedule")
        print("3. View a Slice of the Week")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            print("--- Add a Course ---")
            code = input("Enter course code: ")
            num_slots = int(input("Enter number of time slots (1 or 2): "))
            
            slots_to_add = []
            is_valid_input = True
            i = 0
            while i < num_slots:
                print(f"For slot #{i + 1}:")
                day_idx = int(input("  Enter day index (0-4): "))
                slot_idx = int(input("  Enter time slot index (0-3): "))
                if 0 <= day_idx < 5 and 0 <= slot_idx < 4:
                    slots_to_add.append([day_idx, slot_idx])
                else:
                    print("Error: Invalid index provided.")
                    is_valid_input = False
                    break
                i = i + 1
            
            if is_valid_input and len(slots_to_add) > 0:
                # Call the pure function
                success, message, updated_schedule = task_1_add_course(weekly_schedule, code, slots_to_add)
                print(message)
                
                if success:
                    weekly_schedule = updated_schedule  # Update the schedule
                    print_schedule(weekly_schedule)
                else:
                    print("Error: Could not add course. Time slot clash or invalid index.")
            else:
                print("Error: Invalid input provided.")
            print()

        elif choice == '2':
            print("--- Drop a Course ---")
            
            # Get all available courses
            available_courses = get_all_courses(weekly_schedule)
            if not available_courses:
                print("No courses in schedule.")
            else:
                print(f"Available courses: {', '.join(available_courses)}")
                code_to_drop = input("Enter course code to drop: ")
                
                # Call the pure function
                success, message, updated_schedule = task_2_drop_course(weekly_schedule, code_to_drop)
                print(message)
                
                if success:
                    weekly_schedule = updated_schedule  # Update the schedule
                    print_schedule(weekly_schedule)
            print()

        elif choice == '3':
            print("--- View a Slice of the Week ---")
            start_day = int(input("Enter start day index (0-4): "))
            #Alex changed to up to 4
            end_day = int(input("Enter end day index (must be > start_day, up to 4): "))
            
            # Call the pure function
            success, result_text = task_3_view_slice(weekly_schedule, start_day, end_day)
            
            if success:
                print(result_text)
            else:
                print(result_text)  # This contains the error message
            print()

        elif choice == '4':
            print("Thank you for using the course planner. Goodbye!")
            break

        else:
            print("Error: Invalid choice. Please enter a number from 1-4.")
            print()


if __name__ == "__main__":
    main()

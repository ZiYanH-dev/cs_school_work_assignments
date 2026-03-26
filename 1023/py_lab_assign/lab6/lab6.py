# =============================================================================
# COMP 1023 - Lab 6: UST Course Planner (Simplified)
# SKELETON FILE
#
# Description:
# This file contains the complete working skeleton for the simplified Lab 6.
# It is intended for teaching staff and for reference purposes.
# =============================================================================

# --- Data Structures ---
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# --- Helper Functions (Provided) ---

def print_schedule(schedule_to_print):
    """Prints the weekly schedule in a readable format."""
    print("--- Current Weekly Schedule ---")
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    i = 0
    while i < len(schedule_to_print):
        day_schedule = schedule_to_print[i]
        display_row = []
        j = 0
        while j < len(day_schedule):
            course = day_schedule[j]
            if course is None:
                display_row.append("---")
            else:
                display_row.append(course)
            j = j + 1

        print(str(day_names[i]) + ": " + str(display_row))
        i = i + 1


# This is a new helper function provided to students.
def course_exists(schedule, course_code):
    """
    Checks if a course code already exists in the schedule.
    Returns True if it exists, False otherwise.
    """
    row = 0
    while row < len(schedule):
        col = 0
        while col < len(schedule[row]):
            if schedule[row][col] == course_code:
                return True  # Found the course, exit immediately
            col = col + 1
        row = row + 1
    return False  # Searched the whole schedule, not found

# Initialize the 2D list for the schedule. It's a list of 5 lists (for 5 days).

def create_empty_schedule():
    """Create an empty weekly schedule (5 days, 4 time slots each)."""
    weekly_schedule = []
    i = 0
    while i < 5:
        # Each inner list represents a day and has 4 time slots, initially empty (None)
        row = [None, None, None, None]
        weekly_schedule.append(row)
        i = i + 1
    return weekly_schedule

def get_all_courses(schedule):
    """Get all unique course codes from the schedule."""
    courses = set()
    for row in range(5):
        for col in range(4):
            if schedule[row][col] is not None:
                courses.add(schedule[row][col])
    return sorted(list(courses))

# --- Your Tasks Here ---

def task_1_add_course(schedule, code, slots_to_add):
    '''
    ## Task 1A (Check for existing course) is done for you by calling the provided helper function.
    # Study the code in the course_exists() function above! It will give you a big hint
    # on how to write the nested loops needed for Task 1B.
    '''
    if course_exists(schedule, code):
        return False, f"Error: Course '{code}' already exists in the schedule. Please drop it first.", schedule
    
    # Validate input slots
    for slot_info in slots_to_add:
        day_idx, slot_idx = slot_info
        if not (0 <= day_idx < 5 and 0 <= slot_idx < 4):
            return False, "Error: Invalid index provided.", schedule
    
    ### START TASK 1B: Check for clashes and add the course ###
    '''
    # Follow the detailed instructions on the lab webpage to complete this task.
    #
    # Your goal: First, check if ALL requested slots are free.
    # Only if they are all free, add the course to them.
    '''
    # Make a copy of the schedule to avoid modifying the original
    # Alex: added the 2 lines below
    # If can't add the course, return unchanged schedule at the end, this is done for you
    # If can add the course, return updated_schedule at the end, this is done for you
    updated_schedule = [row[:] for row in schedule]

    # TODO Pass 1:
    # 1. Pre-check for clashes:
    #    a. Create a flag `all_slots_free = True`.
    #    b. Loop through the `slots_to_add` list. For each `[day, slot]` pair:
    #       - Check if the corresponding slot in `schedule` is NOT None.
    #       - If a slot is taken, set `all_slots_free = False` and break the loop.

    # Start your code here for TODO Pass 1
    all_slots_free=True
    for day,slot in slots_to_add:
        if schedule[day][slot]:
            all_slots_free=False
            break

    # End of your code for TODO Pass 1

    # TODO Pass 2:
    # 2. Commit the change:
    #    a. After the pre-check, if `all_slots_free` is still True, loop through `slots_to_add` again.
    #    Alex: modified the line below from schedule to updated_schedule
    #    b. In this second loop, assign the `code` to each corresponding slot in `updated_schedule`.

    if all_slots_free:
        # Start your code here for TODO Pass 2
        for day ,slot in slots_to_add:
            updated_schedule[day][slot]=code


        # End of your code for TODO Pass 2
        return True, f"Success: Course '{code}' added to the schedule.", updated_schedule
    else:
        return False, f"Error: Could not add course '{code}'. Time slot clash detected.", schedule

    ### END TASK 1B ###

def task_2_drop_course(schedule, code_to_drop):
    
    ### START TASK 2: Find and drop all instances of a course ###
    '''
    # Your goal: Search the entire weekly_schedule for the course code and
    # replace every instance you find with None.
    '''
    
    # Make a copy of the schedule to avoid modifying the original
    # If can't drop the course, return unchanged weekly_schedule at the end, this is done for you
    # If can drop the course, return updated_schedule at the end, this is done for you

    updated_schedule = [row[:] for row in schedule]
    
    found_and_dropped = False

    # TODO:
    # 1. Use nested `while` loops to iterate through every cell of `schedule`.
    #    (Outer loop for days, inner loop for slots).
    # 2. Inside the inner loop, if a cell's value equals `code_to_drop`:
    #    a. Set that cell's value in updated_schedule to `None`.
    #    b. Set the flag `found_and_dropped = True`.
    #
    # Start your code here for TODO
    row=len(schedule)
    col=len(schedule[0])
    for i in range(row):
        for j in range(col):
            if updated_schedule[i][j]==code_to_drop:
                updated_schedule[i][j]=None
                found_and_dropped=True

    # End your code here for TODO
    ### END TASK 2 ###

    if found_and_dropped:
        return True, f"Success: All instances of '{code_to_drop}' removed.", updated_schedule
    else:
        return False, f"Error: Course '{code_to_drop}' not found in schedule.", schedule

def task_3_view_slice(schedule, start_day, end_day):

    #### START TASK 3: Slice the schedule with validation ###
    # Your goal: Validate the user's input and then print only the
    # part of the schedule they requested.
    #
    # TODO:
    # 1. Create a flag `range_is_valid = True`.
    # 2. Write an `if` condition to check for a valid range: `0 <= start_day <= end_day <= 4`.
    # 3. If the range is valid:
    #    a. The flag `range_is_valid` is still True.
    #    a. Use list slicing to get the requested part of the schedule.
    #    b. Write your own loop to print this slice, including the correct day names.
    # 4. If the range is invalid, range_is_valid = False.

    result_text = f"Schedule from day {start_day} to {end_day}:\n"
    result_text += "=" * 50 + "\n"

    # Start your code here for TODO
    # Remember to check if the range is valid.
    #put number and its corresponding day into dict for lookup
    days_info={
        0:'mon',
        1:'tue',
        2:'wed',
        3:'thu',
        4:'fri'
    }
    for key in days_info:
        days_info[key]=days_info[key].capitalize()

    range_is_valid=True
    if 0 <= start_day <= end_day <= 4:
        #get the slicing array
        days=schedule[start_day:end_day+1]
        for i in range(len(days)):
            for j in range(len(days[i])):
                #for each cell of the current row
                #set it to --- if it is none
                if not days[i][j]:
                    days[i][j]='---'
            cur_row=days[i]
            #important to plus startday since i starts at 0
            #but startday my not start at zero
            add=f'{days_info[i+start_day]}: {cur_row}\n'
            result_text+=add
    else:
        range_is_valid=False

    # End your code here for TODO
    if range_is_valid:
        return True, result_text
    else:
        return False, "Error: Invalid day range. Ensure 0 <= start_day <= end_day <= 4."

    ### END TASK 3 ###
#!/usr/bin/env python3

# Script to extract content from temp.txt and combine with template.txt

import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

input_file = os.path.join(script_dir, "temp.txt")
template_file = os.path.join(script_dir, "template.txt")
output_file = os.path.join(script_dir, "final_prompt.txt")

# Read template.txt to get first and last lines
with open(template_file, 'r') as f:
    template_lines = f.readlines()

if len(template_lines) >= 2:
    first_line = template_lines[0]
    last_line = template_lines[-1]
else:
    print("Template file must have at least 2 lines")
    exit(1)

# Read temp.txt and extract content between Tasks and Checking Before Submission
with open(input_file, 'r') as f:
    lines = f.readlines()

start_idx = None
end_idx = None
tasks_count = 0

for i, line in enumerate(lines):
    if 'Tasks' in line.strip():
        tasks_count += 1
        if tasks_count == 2:  # Second occurrence is the actual section
            start_idx = i
    elif 'Checking Before Submission' in line and start_idx is not None:
        end_idx = i
        break

if start_idx is not None and end_idx is not None:
    extracted_content = ''.join(lines[start_idx:end_idx])
    
    # Combine with template lines
    final_content = first_line + '\n' + extracted_content + '\n' + last_line
    
    with open(output_file, 'w') as f:
        f.write(final_content)
    
    print(f"Processed content saved to {output_file}")
    print(f"Extracted content length: {end_idx - start_idx} lines")
else:
    print("Failed to find the required sections in the input file")
#  - start_idx} lines from temp.txt")
    print(f"Added template header and footer")
    print(f"Extracted {end_idx - start_idx} lines from temp.txt")
# else:
#     print("Could not find both 'Tasks' and 'Checking Before Submission' sections")

#!/usr/bin/env python3
"""Remove all lines after app.run in app.py"""

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the line with app.run
app_run_line = -1
for i, line in enumerate(lines):
    if 'app.run(' in line:
        app_run_line = i
        break

if app_run_line != -1:
    # Keep everything up to and including app.run
    clean_lines = lines[:app_run_line+1]
    clean_lines.append('\n')
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.writelines(clean_lines)
    
    print(f"✅ Cleaned: {len(lines)} → {len(clean_lines)} lines")
    print(f"   Removed {len(lines) - len(clean_lines)} lines after app.run")
else:
    print("❌ Could not find app.run line")

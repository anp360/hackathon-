#!/usr/bin/env python3
"""Clean up app.py by removing duplicate SMS/media code"""

with open('d:/crisis_resource_matching/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the line with "}, 500" after the delivery routes endpoint 
# and the line with "if __name__ == '__main__':" followed by "# Create templates"

in_old_code = False
clean_lines = []
found_delivery_end = False
skip_until_main = False

for i, line in enumerate(lines):
    # Check if we've reached the end of the delivery routes endpoint
    if '        }), 500' in line and not found_delivery_end and 'routes' in ''.join(lines[max(0, i-10):i]):
        clean_lines.append(line)
        clean_lines.append('\n')
        found_delivery_end = True
        skip_until_main = True
        continue
    
    # If we're skipping, look for the real main block
    if skip_until_main:
        if "if __name__ == '__main__':" in line and i+1 < len(lines) and '# Create templates' in lines[i+1]:
            skip_until_main = False
            clean_lines.append(line)
        continue
    
    # Normal case - add the line
    clean_lines.append(line)

# Write the cleaned content
with open('d:/crisis_resource_matching/app.py', 'w', encoding='utf-8') as f:
    f.writelines(clean_lines)

print(f"✅ Cleaned app.py: {len(lines)} → {len(clean_lines)} lines")
print(f"   Removed {len(lines) - len(clean_lines)} lines of old code")

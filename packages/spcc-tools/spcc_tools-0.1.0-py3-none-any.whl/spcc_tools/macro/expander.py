"""Implementation of MACRO expansion without arguments.

This module implements:
1. Definition of MACROs without arguments
2. Expansion of MACRO calls
"""

import os
import sys
from collections import defaultdict

def expand_macro(input_file):
    """Expand macros in the input file.
    
    Args:
        input_file (str): Path to the input file containing macro definitions and calls
        
    Returns:
        str: The expanded code with all macro calls replaced by their definitions
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file {input_file} not found")
    
    # Read the input file
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    # Initialize data structures
    macro_defs = {}
    current_macro = None
    macro_body = []
    expanded_lines = []
    in_macro_def = False
    
    # Process each line
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith(';'):  # Skip empty lines and comments
            expanded_lines.append(line)
            continue
        
        # Check for macro definition start
        if line.startswith('MACRO'):
            parts = line.split()
            if len(parts) != 2:
                raise SyntaxError(f"Invalid MACRO definition at line {line_num}: {line}")
            
            current_macro = parts[1]
            in_macro_def = True
            macro_body = []
            continue
        
        # Check for macro definition end
        if line == 'ENDM' and in_macro_def:
            macro_defs[current_macro] = macro_body
            in_macro_def = False
            current_macro = None
            continue
        
        # Inside macro definition
        if in_macro_def:
            macro_body.append(line)
            continue
        
        # Check for macro call
        if line in macro_defs:
            # Expand the macro
            for macro_line in macro_defs[line]:
                expanded_lines.append(macro_line)
        else:
            # Regular line
            expanded_lines.append(line)
    
    # Check if any macro definition was not closed
    if in_macro_def:
        raise SyntaxError(f"Unclosed MACRO definition for {current_macro}")
    
    return '\n'.join(expanded_lines)

def expand_macro_to_file(input_file, output_file=None):
    """Expand macros in the input file and write the result to an output file.
    
    Args:
        input_file (str): Path to the input file containing macro definitions and calls
        output_file (str, optional): Path to the output file. If None, a default name will be used.
        
    Returns:
        str: Path to the output file
    """
    expanded_code = expand_macro(input_file)
    
    if output_file is None:
        base_name, ext = os.path.splitext(input_file)
        output_file = f"{base_name}_expanded{ext}"
    
    with open(output_file, 'w') as f:
        f.write(expanded_code)
    
    return output_file

def main():
    """Main function to run the macro expander from command line."""
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python expander.py <input_file> [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) == 3 else None
    
    try:
        result_file = expand_macro_to_file(input_file, output_file)
        print(f"Macro expansion completed. Output written to {result_file}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
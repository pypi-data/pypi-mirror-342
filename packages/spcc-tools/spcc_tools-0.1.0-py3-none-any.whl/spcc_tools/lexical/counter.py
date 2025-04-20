"""Implementation of lexical analysis counter using LEX (PLY in Python).

This module implements a lexical analyzer that counts:
1. Characters
2. Words
3. Sentences
4. Lines
5. Tabs
6. Numbers
7. Blank spaces
"""

import os
import sys
import re
import ply.lex as lex

# Define token types
tokens = (
    'WORD',
    'NUMBER',
    'SPACE',
    'TAB',
    'NEWLINE',
    'SENTENCE_END',
    'OTHER',
)

# Regular expression rules for tokens
t_WORD = r'[a-zA-Z]+'  # Words (sequences of letters)
t_NUMBER = r'\d+'  # Numbers (sequences of digits)
t_SPACE = r' '  # Space
t_TAB = r'\t'  # Tab
t_NEWLINE = r'\n'  # Newline
t_SENTENCE_END = r'[.!?]'  # Sentence ending punctuation
t_OTHER = r'.'  # Any other character

# Error handling rule
def t_error(t):
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

def count_elements(text):
    """Count various elements in the input text using lexical analysis.
    
    Args:
        text (str): The input text to analyze
        
    Returns:
        dict: A dictionary containing counts of various elements
    """
    # Initialize counters
    counts = {
        'characters': 0,
        'words': 0,
        'sentences': 0,
        'lines': 1,  # Start with 1 for the first line
        'tabs': 0,
        'numbers': 0,
        'spaces': 0,
    }
    
    # Give the input text to the lexer
    lexer.input(text)
    
    # Count tokens
    for tok in lexer:
        counts['characters'] += len(tok.value)
        
        if tok.type == 'WORD':
            counts['words'] += 1
        elif tok.type == 'NUMBER':
            counts['numbers'] += 1
        elif tok.type == 'SPACE':
            counts['spaces'] += 1
        elif tok.type == 'TAB':
            counts['tabs'] += 1
        elif tok.type == 'NEWLINE':
            counts['lines'] += 1
        elif tok.type == 'SENTENCE_END':
            counts['sentences'] += 1
    
    # If there's no sentence ending punctuation, but there is text,
    # count it as one sentence
    if counts['sentences'] == 0 and (counts['words'] > 0 or counts['numbers'] > 0):
        counts['sentences'] = 1
    
    return counts

def count_elements_from_file(file_path):
    """Count various elements in a file using lexical analysis.
    
    Args:
        file_path (str): Path to the input file
        
    Returns:
        dict: A dictionary containing counts of various elements
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file {file_path} not found")
    
    with open(file_path, 'r') as f:
        text = f.read()
    
    return count_elements(text)

def format_output(counts):
    """Format the counts for display.
    
    Args:
        counts (dict): A dictionary containing counts of various elements
        
    Returns:
        str: Formatted output
    """
    output = ["LEXICAL ANALYSIS COUNTS"]
    output.append("-" * 40)
    
    for element, count in counts.items():
        output.append(f"{element.capitalize()}: {count}")
    
    return "\n".join(output)

def main():
    """Main function to run the lexical analysis counter from command line."""
    if len(sys.argv) != 2:
        print("Usage: python counter.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        counts = count_elements_from_file(input_file)
        print(format_output(counts))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
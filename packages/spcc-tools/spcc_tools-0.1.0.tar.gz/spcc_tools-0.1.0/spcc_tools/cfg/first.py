"""Implementation of FIRST set computation for Context-Free Grammars.

This module implements an algorithm to compute FIRST sets for all symbols in a Context-Free Grammar.
"""

import os
import sys
import json
from collections import defaultdict

def is_terminal(symbol):
    """Check if a symbol is a terminal.
    
    Args:
        symbol (str): The symbol to check
        
    Returns:
        bool: True if the symbol is a terminal, False otherwise
    """
    # Terminals are typically lowercase in CFGs
    # This is a simple heuristic; adjust as needed for your grammar notation
    return symbol.islower() or symbol in ['$', 'ε', 'epsilon']

def is_non_terminal(symbol):
    """Check if a symbol is a non-terminal.
    
    Args:
        symbol (str): The symbol to check
        
    Returns:
        bool: True if the symbol is a non-terminal, False otherwise
    """
    # Non-terminals are typically uppercase in CFGs
    # This is a simple heuristic; adjust as needed for your grammar notation
    return symbol.isupper()

def compute_first(grammar):
    """Compute FIRST sets for all symbols in a Context-Free Grammar.
    
    Args:
        grammar (dict): A dictionary representing the grammar, where keys are non-terminals
                       and values are lists of productions
        
    Returns:
        dict: A dictionary mapping each symbol to its FIRST set
    """
    # Initialize FIRST sets
    first = defaultdict(set)
    
    # For all terminals, FIRST(terminal) = {terminal}
    for non_terminal, productions in grammar.items():
        for production in productions:
            for symbol in production:
                if is_terminal(symbol):
                    first[symbol] = {symbol}
    
    # Add epsilon to FIRST set of non-terminals that derive epsilon
    for non_terminal, productions in grammar.items():
        for production in productions:
            if production == 'ε' or production == 'epsilon' or not production:
                first[non_terminal].add('ε')
    
    # Compute FIRST sets for non-terminals
    changed = True
    while changed:
        changed = False
        
        for non_terminal, productions in grammar.items():
            for production in productions:
                # Skip empty productions
                if not production or production == 'ε' or production == 'epsilon':
                    continue
                
                # Get the first symbol of the production
                symbols = list(production)
                
                # Process each symbol in the production
                all_derive_epsilon = True
                for i, symbol in enumerate(symbols):
                    if is_terminal(symbol):
                        # If the symbol is a terminal, add it to FIRST set and break
                        if symbol not in first[non_terminal]:
                            first[non_terminal].add(symbol)
                            changed = True
                        all_derive_epsilon = False
                        break
                    else:
                        # If the symbol is a non-terminal, add its FIRST set (except epsilon)
                        # to the FIRST set of the current non-terminal
                        for terminal in first[symbol] - {'ε'}:
                            if terminal not in first[non_terminal]:
                                first[non_terminal].add(terminal)
                                changed = True
                        
                        # If the symbol doesn't derive epsilon, we're done with this production
                        if 'ε' not in first[symbol]:
                            all_derive_epsilon = False
                            break
                
                # If all symbols in the production can derive epsilon,
                # add epsilon to the FIRST set of the non-terminal
                if all_derive_epsilon and 'ε' not in first[non_terminal]:
                    first[non_terminal].add('ε')
                    changed = True
    
    # Convert sets to sorted lists for consistent output
    return {k: sorted(v) for k, v in first.items()}

def parse_grammar_file(file_path):
    """Parse a grammar file into a dictionary.
    
    The file should have one production per line in the format:
    non_terminal -> production1 | production2 | ...
    
    Args:
        file_path (str): Path to the grammar file
        
    Returns:
        dict: A dictionary representing the grammar
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Grammar file {file_path} not found")
    
    grammar = defaultdict(list)
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Split the line into non-terminal and productions
            parts = line.split('->')
            if len(parts) != 2:
                continue
            
            non_terminal = parts[0].strip()
            productions = parts[1].strip().split('|')
            
            for production in productions:
                production = production.strip()
                if production == 'ε' or production == 'epsilon':
                    grammar[non_terminal].append('ε')
                else:
                    grammar[non_terminal].append(production)
    
    return grammar

def format_output(first_sets):
    """Format the FIRST sets for display.
    
    Args:
        first_sets (dict): A dictionary mapping each symbol to its FIRST set
        
    Returns:
        str: Formatted output
    """
    output = ["FIRST SETS"]
    output.append("-" * 40)
    
    for symbol in sorted(first_sets.keys()):
        first_set = first_sets[symbol]
        output.append(f"FIRST({symbol}) = {{{', '.join(first_set)}}}")
    
    return "\n".join(output)

def main():
    """Main function to run the FIRST set computation from command line."""
    if len(sys.argv) != 2:
        print("Usage: python first.py <grammar_file>")
        sys.exit(1)
    
    grammar_file = sys.argv[1]
    
    try:
        grammar = parse_grammar_file(grammar_file)
        first_sets = compute_first(grammar)
        print(format_output(first_sets))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
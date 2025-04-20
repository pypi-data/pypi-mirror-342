"""Implementation of FOLLOW set computation for Context-Free Grammars.

This module implements an algorithm to compute FOLLOW sets for all non-terminals in a Context-Free Grammar.
"""

import os
import sys
import json
from collections import defaultdict
from .first import compute_first, is_terminal, is_non_terminal, parse_grammar_file

def compute_follow(grammar, start_symbol):
    """Compute FOLLOW sets for all non-terminals in a Context-Free Grammar.
    
    Args:
        grammar (dict): A dictionary representing the grammar, where keys are non-terminals
                       and values are lists of productions
        start_symbol (str): The start symbol of the grammar
        
    Returns:
        dict: A dictionary mapping each non-terminal to its FOLLOW set
    """
    # Compute FIRST sets (needed for FOLLOW computation)
    first = compute_first(grammar)
    
    # Initialize FOLLOW sets
    follow = defaultdict(set)
    
    # Add $ to FOLLOW set of start symbol
    follow[start_symbol].add('$')
    
    # Compute FOLLOW sets
    changed = True
    while changed:
        changed = False
        
        for non_terminal, productions in grammar.items():
            for production in productions:
                # Skip empty productions
                if not production or production == 'ε' or production == 'epsilon':
                    continue
                
                # Process each symbol in the production
                symbols = list(production)
                for i, symbol in enumerate(symbols):
                    # We only compute FOLLOW sets for non-terminals
                    if not is_non_terminal(symbol):
                        continue
                    
                    # If this is the last symbol in the production,
                    # add FOLLOW(non_terminal) to FOLLOW(symbol)
                    if i == len(symbols) - 1:
                        for terminal in follow[non_terminal]:
                            if terminal not in follow[symbol]:
                                follow[symbol].add(terminal)
                                changed = True
                    else:
                        # Get the next symbol
                        next_symbol = symbols[i + 1]
                        
                        # If the next symbol is a terminal,
                        # add it to FOLLOW(symbol)
                        if is_terminal(next_symbol):
                            if next_symbol not in follow[symbol]:
                                follow[symbol].add(next_symbol)
                                changed = True
                        else:
                            # If the next symbol is a non-terminal,
                            # add FIRST(next_symbol) - {ε} to FOLLOW(symbol)
                            for terminal in first[next_symbol]:
                                if terminal != 'ε' and terminal not in follow[symbol]:
                                    follow[symbol].add(terminal)
                                    changed = True
                            
                            # If ε is in FIRST(next_symbol), add FOLLOW(non_terminal) to FOLLOW(symbol)
                            if 'ε' in first[next_symbol]:
                                # Check if this is the last symbol or if all following symbols can derive ε
                                all_derive_epsilon = True
                                for j in range(i + 1, len(symbols)):
                                    if 'ε' not in first[symbols[j]]:
                                        all_derive_epsilon = False
                                        break
                                
                                if all_derive_epsilon:
                                    for terminal in follow[non_terminal]:
                                        if terminal not in follow[symbol]:
                                            follow[symbol].add(terminal)
                                            changed = True
    
    # Convert sets to sorted lists for consistent output
    return {k: sorted(v) for k, v in follow.items()}

def format_output(follow_sets):
    """Format the FOLLOW sets for display.
    
    Args:
        follow_sets (dict): A dictionary mapping each non-terminal to its FOLLOW set
        
    Returns:
        str: Formatted output
    """
    output = ["FOLLOW SETS"]
    output.append("-" * 40)
    
    for symbol in sorted(follow_sets.keys()):
        follow_set = follow_sets[symbol]
        output.append(f"FOLLOW({symbol}) = {{{', '.join(follow_set)}}}")
    
    return "\n".join(output)

def main():
    """Main function to run the FOLLOW set computation from command line."""
    if len(sys.argv) != 3:
        print("Usage: python follow.py <grammar_file> <start_symbol>")
        sys.exit(1)
    
    grammar_file = sys.argv[1]
    start_symbol = sys.argv[2]
    
    try:
        grammar = parse_grammar_file(grammar_file)
        follow_sets = compute_follow(grammar, start_symbol)
        print(format_output(follow_sets))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
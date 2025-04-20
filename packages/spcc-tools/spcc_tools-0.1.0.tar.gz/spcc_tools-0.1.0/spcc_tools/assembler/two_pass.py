"""Implementation of Pass 1 of Two Pass Assembler.

This module implements the first pass of a two-pass assembler which:
1. Assigns addresses to all statements in the program
2. Saves the values assigned to all labels for use in Pass 2
3. Performs some processing of assembler directives
"""

import os
import sys
from collections import namedtuple

# Define a structure for symbol table entries
Symbol = namedtuple('Symbol', ['name', 'address', 'type'])

# Define a structure for literal table entries
Literal = namedtuple('Literal', ['value', 'address'])

# Define opcodes with their machine code and length
OPCODES = {
    'STOP': {'code': '00', 'length': 1},
    'ADD': {'code': '01', 'length': 2},
    'SUB': {'code': '02', 'length': 2},
    'MULT': {'code': '03', 'length': 2},
    'MOVER': {'code': '04', 'length': 2},
    'MOVEM': {'code': '05', 'length': 2},
    'COMP': {'code': '06', 'length': 2},
    'BC': {'code': '07', 'length': 2},
    'DIV': {'code': '08', 'length': 2},
    'READ': {'code': '09', 'length': 2},
    'PRINT': {'code': '10', 'length': 2},
}

# Define assembler directives
DIRECTIVES = ['START', 'END', 'ORIGIN', 'EQU', 'LTORG']

# Define registers
REGISTERS = {
    'AREG': 1,
    'BREG': 2,
    'CREG': 3,
    'DREG': 4,
}

# Define condition codes
CONDITION_CODES = {
    'LT': 1,
    'LE': 2,
    'EQ': 3,
    'GT': 4,
    'GE': 5,
    'ANY': 6,
}

def is_literal(operand):
    """Check if the operand is a literal."""
    return operand.startswith('=')

def is_symbol(operand):
    """Check if the operand is a symbol."""
    return not is_literal(operand) and operand not in REGISTERS

def pass_one(input_file):
    """Implement Pass 1 of Two Pass Assembler.
    
    Args:
        input_file (str): Path to the input assembly file
        
    Returns:
        dict: A dictionary containing symbol table, literal table, and intermediate code
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file {input_file} not found")
    
    # Initialize data structures
    symbol_table = []
    literal_table = []
    intermediate_code = []
    location_counter = 0
    pool_table = [0]  # To keep track of literals
    
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    # First pass
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith(';'):  # Skip empty lines and comments
            continue
        
        # Parse the line
        parts = line.split()
        if len(parts) == 1:  # Only opcode
            label, opcode, operand = None, parts[0], None
        elif len(parts) == 2:  # Opcode and operand
            label, opcode, operand = None, parts[0], parts[1]
        elif len(parts) == 3:  # Label, opcode, and operand
            label, opcode, operand = parts
        else:
            raise SyntaxError(f"Invalid syntax at line {line_num}: {line}")
        
        # Process label if present
        if label:
            # Check if label already exists in symbol table
            if any(symbol.name == label for symbol in symbol_table):
                raise ValueError(f"Duplicate label '{label}' at line {line_num}")
            
            # Add label to symbol table
            symbol_table.append(Symbol(label, location_counter, 'label'))
        
        # Process opcode
        if opcode in OPCODES:
            # Regular instruction
            instruction_length = OPCODES[opcode]['length']
            
            # Process operand if present
            if operand:
                if is_literal(operand):
                    # Add literal to literal table if not already present
                    lit_value = operand[1:]  # Remove '=' prefix
                    if not any(lit.value == lit_value for lit in literal_table):
                        # Address will be assigned later during LTORG or END
                        literal_table.append(Literal(lit_value, None))
                elif is_symbol(operand):
                    # Add symbol to symbol table if not already present
                    if not any(symbol.name == operand for symbol in symbol_table):
                        # Address will be assigned later when symbol is defined
                        symbol_table.append(Symbol(operand, None, 'variable'))
            
            # Add to intermediate code
            intermediate_code.append({
                'line_num': line_num,
                'location': location_counter,
                'label': label,
                'opcode': opcode,
                'operand': operand
            })
            
            # Update location counter
            location_counter += instruction_length
            
        elif opcode in DIRECTIVES:
            # Process assembler directives
            if opcode == 'START':
                if operand and operand.isdigit():
                    location_counter = int(operand)
                else:
                    location_counter = 0
                
                # Add to intermediate code
                intermediate_code.append({
                    'line_num': line_num,
                    'location': location_counter,
                    'label': label,
                    'opcode': opcode,
                    'operand': operand
                })
                
            elif opcode == 'END':
                # Process any pending literals
                if literal_table and any(lit.address is None for lit in literal_table):
                    for i, lit in enumerate(literal_table):
                        if lit.address is None:
                            # Assign address to literal
                            literal_table[i] = Literal(lit.value, location_counter)
                            location_counter += 1
                
                # Add to intermediate code
                intermediate_code.append({
                    'line_num': line_num,
                    'location': location_counter,
                    'label': label,
                    'opcode': opcode,
                    'operand': operand
                })
                
            elif opcode == 'ORIGIN':
                # Change location counter
                if operand:
                    # Parse operand which could be a symbol or expression
                    if '+' in operand:
                        parts = operand.split('+')
                        base = parts[0]
                        offset = int(parts[1])
                        
                        # Find base address from symbol table
                        base_addr = None
                        for symbol in symbol_table:
                            if symbol.name == base:
                                base_addr = symbol.address
                                break
                        
                        if base_addr is not None:
                            location_counter = base_addr + offset
                        else:
                            raise ValueError(f"Undefined symbol '{base}' at line {line_num}")
                    elif '-' in operand:
                        parts = operand.split('-')
                        base = parts[0]
                        offset = int(parts[1])
                        
                        # Find base address from symbol table
                        base_addr = None
                        for symbol in symbol_table:
                            if symbol.name == base:
                                base_addr = symbol.address
                                break
                        
                        if base_addr is not None:
                            location_counter = base_addr - offset
                        else:
                            raise ValueError(f"Undefined symbol '{base}' at line {line_num}")
                    else:
                        # Direct address or symbol
                        if operand.isdigit():
                            location_counter = int(operand)
                        else:
                            # Find address from symbol table
                            addr = None
                            for symbol in symbol_table:
                                if symbol.name == operand:
                                    addr = symbol.address
                                    break
                            
                            if addr is not None:
                                location_counter = addr
                            else:
                                raise ValueError(f"Undefined symbol '{operand}' at line {line_num}")
                
                # Add to intermediate code
                intermediate_code.append({
                    'line_num': line_num,
                    'location': location_counter,
                    'label': label,
                    'opcode': opcode,
                    'operand': operand
                })
                
            elif opcode == 'EQU':
                # Assign value to symbol
                if label and operand:
                    # Parse operand which could be a symbol or expression
                    if '+' in operand:
                        parts = operand.split('+')
                        base = parts[0]
                        offset = int(parts[1])
                        
                        # Find base address from symbol table
                        base_addr = None
                        for symbol in symbol_table:
                            if symbol.name == base:
                                base_addr = symbol.address
                                break
                        
                        if base_addr is not None:
                            addr = base_addr + offset
                        else:
                            raise ValueError(f"Undefined symbol '{base}' at line {line_num}")
                    elif '-' in operand:
                        parts = operand.split('-')
                        base = parts[0]
                        offset = int(parts[1])
                        
                        # Find base address from symbol table
                        base_addr = None
                        for symbol in symbol_table:
                            if symbol.name == base:
                                base_addr = symbol.address
                                break
                        
                        if base_addr is not None:
                            addr = base_addr - offset
                        else:
                            raise ValueError(f"Undefined symbol '{base}' at line {line_num}")
                    else:
                        # Direct address or symbol
                        if operand.isdigit():
                            addr = int(operand)
                        else:
                            # Find address from symbol table
                            addr = None
                            for symbol in symbol_table:
                                if symbol.name == operand:
                                    addr = symbol.address
                                    break
                            
                            if addr is None:
                                raise ValueError(f"Undefined symbol '{operand}' at line {line_num}")
                    
                    # Update symbol table
                    for i, symbol in enumerate(symbol_table):
                        if symbol.name == label:
                            symbol_table[i] = Symbol(label, addr, 'label')
                            break
                    else:
                        symbol_table.append(Symbol(label, addr, 'label'))
                
                # Add to intermediate code
                intermediate_code.append({
                    'line_num': line_num,
                    'location': location_counter,  # EQU doesn't change LC
                    'label': label,
                    'opcode': opcode,
                    'operand': operand
                })
                
            elif opcode == 'LTORG':
                # Process literals
                if literal_table and any(lit.address is None for lit in literal_table):
                    pool_table.append(len(literal_table))
                    for i, lit in enumerate(literal_table):
                        if lit.address is None:
                            # Assign address to literal
                            literal_table[i] = Literal(lit.value, location_counter)
                            location_counter += 1
                
                # Add to intermediate code
                intermediate_code.append({
                    'line_num': line_num,
                    'location': location_counter,
                    'label': label,
                    'opcode': opcode,
                    'operand': operand
                })
        else:
            # Unknown opcode
            raise ValueError(f"Unknown opcode '{opcode}' at line {line_num}")
    
    # Return the results
    return {
        'symbol_table': symbol_table,
        'literal_table': literal_table,
        'pool_table': pool_table,
        'intermediate_code': intermediate_code
    }

def format_output(result):
    """Format the output of pass_one for display.
    
    Args:
        result (dict): The result from pass_one
        
    Returns:
        str: Formatted output
    """
    output = []
    
    # Symbol Table
    output.append("SYMBOL TABLE")
    output.append("-" * 40)
    output.append(f"{'Symbol':<10} {'Address':<10} {'Type':<10}")
    output.append("-" * 40)
    for symbol in result['symbol_table']:
        output.append(f"{symbol.name:<10} {symbol.address if symbol.address is not None else 'None':<10} {symbol.type:<10}")
    output.append("\n")
    
    # Literal Table
    output.append("LITERAL TABLE")
    output.append("-" * 40)
    output.append(f"{'Literal':<10} {'Address':<10}")
    output.append("-" * 40)
    for literal in result['literal_table']:
        output.append(f"{literal.value:<10} {literal.address if literal.address is not None else 'None':<10}")
    output.append("\n")
    
    # Pool Table
    output.append("POOL TABLE")
    output.append("-" * 40)
    output.append(f"{'Pool Index':<10} {'Literal Index':<15}")
    output.append("-" * 40)
    for i, pool_index in enumerate(result['pool_table']):
        output.append(f"{i+1:<10} {pool_index:<15}")
    output.append("\n")
    
    # Intermediate Code
    output.append("INTERMEDIATE CODE")
    output.append("-" * 60)
    output.append(f"{'Line':<5} {'LC':<5} {'Label':<10} {'Opcode':<10} {'Operand':<10}")
    output.append("-" * 60)
    for code in result['intermediate_code']:
        output.append(f"{code['line_num']:<5} {code['location']:<5} {code['label'] if code['label'] else '':<10} {code['opcode']:<10} {code['operand'] if code['operand'] else '':<10}")
    
    return "\n".join(output)

def main():
    """Main function to run the assembler from command line."""
    if len(sys.argv) != 2:
        print("Usage: python two_pass.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        result = pass_one(input_file)
        print(format_output(result))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
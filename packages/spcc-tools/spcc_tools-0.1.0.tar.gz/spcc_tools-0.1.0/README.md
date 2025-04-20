# SPCC Tools

A Python package containing implementations of System Programming and Compiler Construction experiments.

## Installation

```bash
pip install spcc-tools
```

## Features

This package includes the following experiments:

1. **Two Pass Assembler** - Implementation of Pass 1 of a Two Pass Assembler
2. **MACRO Expansion** - Program to define a MACRO without arguments and expand MACRO calls
3. **FOLLOW Computation** - Program to compute FOLLOW sets for a Context-Free Grammar (CFG)
4. **FIRST Computation** - Program to compute FIRST sets for a Context-Free Grammar (CFG)
5. **Lexical Analysis** - Program to count characters, words, sentences, lines, tabs, numbers, and blank spaces using LEX

## Usage

### Two Pass Assembler

```python
from spcc_tools.assembler.two_pass import pass_one

# Example usage
result = pass_one(input_file_path)
print(result)
```

Or use the command-line interface:

```bash
spcc-assembler input_file.asm
```

### MACRO Expansion

```python
from spcc_tools.macro.expander import expand_macro

# Example usage
expanded_code = expand_macro(input_file_path)
print(expanded_code)
```

Or use the command-line interface:

```bash
spcc-macro input_file.txt
```

### FOLLOW Computation

```python
from spcc_tools.cfg.follow import compute_follow

# Example usage
grammar = {
    'S': ['AB', 'BC'],
    'A': ['a'],
    'B': ['b'],
    'C': ['c']
}
follow_sets = compute_follow(grammar, 'S')
print(follow_sets)
```

Or use the command-line interface:

```bash
spcc-follow grammar_file.txt
```

### FIRST Computation

```python
from spcc_tools.cfg.first import compute_first

# Example usage
grammar = {
    'S': ['AB', 'BC'],
    'A': ['a'],
    'B': ['b'],
    'C': ['c']
}
first_sets = compute_first(grammar)
print(first_sets)
```

Or use the command-line interface:

```bash
spcc-first grammar_file.txt
```

### Lexical Analysis Counter

```python
from spcc_tools.lexical.counter import count_elements

# Example usage
result = count_elements(input_text)
print(result)
```

Or use the command-line interface:

```bash
spcc-lexcount input_file.txt
```

## License

MIT
# RPAL Interpreter

This project is the culmination of the **CS3513 - Programming Languages** module, offered by the Department of Computer Science & Engineering, University of Moratuwa. It was completed in the 4th semester of Batch 22.

---

## Table of Contents

- [Problem Requirements](#problem-requirements)  
- [About Our Solution](#about-our-solution)  
- [Usage](#usage)  
- [Features](#features)  
- [Project Structure](#project-structure)  
- [Modules](#modules)  
  - [Lexical Analyzer](#lexical-analyzer)  
  - [Screener](#screener)  
  - [Parser](#parser)  
  - [CSE Machine](#cse-machine)  
- [Contributors](#contributors)  
- [License](#license)  

---

## Problem Requirements

Implement a lexical analyzer and parser for the RPAL (Right-reference Pedagogic Algorithmic Language). The lexical rules are specified in `RPAL_Lex`, and grammar details are in `RPAL_Grammar`. Refer to the "About RPAL" documentation for language information.

The parser output must be the **Abstract Syntax Tree (AST)** for the input program. Additionally, implement an algorithm to convert the AST into a **Standardized Tree (ST)**, and implement the **CSE machine** as per the provided semantics document, which defines the rules for AST to ST transformation.

The program should read an input RPAL program file and produce output matching that of the reference `rpal.exe`.

---

## About Our Solution

- **Programming Language:** Python  
- **Development & Testing Tools:** Visual Studio Code, Command Line, Cygwin, Pytest, GitHub Actions, Makefile  

---

## Usage

### Prerequisites

- Python (preferably 3.7 or above) and pip installed on your system.

### Setup

1. Clone the repository or download the source code ZIP.  
2. Navigate to the project root directory.  
3. Install the required Python dependencies:

```bash
pip install -r requirements.txt


## Running the Interpreter

The project files are primarily executed from the `src` directory. To run the interpreter and other features, navigate to the `src` folder and run commands as follows:

```bash
cd src
python myrpal.py [switch] ../testing_rpal_sources/file_name.rpal

### Available Command-Line Switches

| Switch       | Description                               | Example Usage                                           |
|--------------|-------------------------------------------|---------------------------------------------------------|
| *(no switch)*| Run the interpreter on the RPAL source    | `python myrpal.py ../testing_rpal_sources/file_name.rpal` |
| `-ast`       | Generate the Abstract Syntax Tree (AST)   | `python myrpal.py -ast ../testing_rpal_sources/file_name.rpal` |
| `-st`        | Generate the Standardized Tree (ST)        | `python myrpal.py -st ../testing_rpal_sources/file_name.rpal`  |
| `-ct`        | Generate the CSE Machine table              | `python myrpal.py -ct ../testing_rpal_sources/file_name.rpal`  |
| `-t`         | Generate the token list from the lexer     | `python myrpal.py -t ../testing_rpal_sources/file_name.rpal`   |
| `-ft`        | Generate the filtered token list from screener | `python myrpal.py -ft ../testing_rpal_sources/file_name.rpal` |



Features

Lexical Analysis: Tokenizes RPAL source code based on RPAL_Lex rules.
Token Screening: Filters tokens to remove whitespace and comments, preparing them for parsing.
Parsing: Constructs the Abstract Syntax Tree (AST) and Standardized Tree (ST).
CSE Machine: Executes the RPAL program by traversing the ST and applying the 13 CSE evaluation rules.
Debugging Outputs: Provides options to view tokens, filtered tokens, AST, ST, and CSE machine table.
Error Handling: Robust handling of invalid inputs and syntax errors.


Project Structure
The project is organized into modular components, each handling a specific part of the interpretation process:
rpal-interpreter/
├── docs/                  # Documentation files
├── src/                   # Source code for the interpreter
│   ├── __pycache__/       # Python bytecode cache
│   ├── cse_machine/       # CSE machine implementation
│   │   ├── __pycache__/
│   │   ├── binop.py
│   │   ├── control_struct.py
│   │   ├── environment.py
│   │   ├── error_handler.py
│   │   ├── machine.py
│   │   ├── stack.py
│   │   ├── stlinearizer.py
│   │   ├── unop.py
│   │   └── utils.py
│   ├── rpal_source/       # RPAL source-related files
│   │   ├── cygwin1.dll    # Cygwin DLL for Windows compatibility
│   │   └── rpal.exe       # Reference RPAL executable
│   ├── table_routines/    # Table and state machine routines
│   │   ├── __pycache__/
│   │   ├── accept_states.py
│   │   ├── char_map.py
│   │   ├── fsa_table.py
│   │   ├── keywords.py
│   │   └── utils/         # Utility functions for table routines
│   │       ├── __pycache__/
│   │       ├── control_struct.py
│   │       ├── file_handler.py
│   │       ├── node.py
│   │       ├── stack.py
│   │       ├── token_printer.py
│   │       ├── tokens.py
│   │       ├── tree_list.py
│   │       ├── tree_printer.py
│   │       ├── build_standard.py
│   │       └── interpreter.py
│   ├── utils/             # General utility scripts
│   │   ├── __pycache__/
│   │   ├── control_struct.py
│   │   ├── file_handler.py
│   │   ├── node.py
│   │   ├── stack.py
│   │   ├── token_printer.py
│   │   ├── tokens.py
│   │   ├── tree_list.py
│   │   ├── tree_printer.py
│   │   ├── build_standard.py
│   │   ├── interpreter.py
│   │   ├── myrpal.py
│   │   ├── parser.py
│   │   ├── scanner.py
│   │   └── screener.py
├── testing_rpal_sources/  # Sample RPAL test files
├── .gitignore             # Git ignore file
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies


Modules
Lexical Analyzer
Purpose: Scans the RPAL source file and generates a token list based on RPAL_Lex rules.Input: RPAL source fileOutput: List of token objects (type, value attributes)Details: Implemented in scanner.py, utilizing finite state automata from table_routines.
Screener
Purpose: Filters the token list to prepare it for parsing.Input: Token list from the Lexical AnalyzerOutput: Filtered token listDetails: Implemented in screener.py, removing unnecessary tokens like whitespace and comments.
Parser
Purpose: Constructs the Abstract Syntax Tree (AST) and Standardized Tree (ST).Input: Filtered token list from the ScreenerOutput: Standardized Tree (ST)Details: Implemented in parser.py, with tree-building logic in build_standard.py.
CSE Machine
Purpose: Evaluates the RPAL program by traversing the ST and applying the 13 CSE rules.Input: Standardized Tree (ST)Output: Program outputDetails: Implemented in cse_machine/machine.py, with supporting logic in stlinearizer.py and environment.py.

Contributors

[Your Name] (GitHub: [your-username])
[Contributor Name] (GitHub: [contributor-username], if applicable)

Contributions are welcome! Please submit a pull request or open an issue for suggestions or bug reports.

License
This project is licensed under the MIT License. See the LICENSE file for details.

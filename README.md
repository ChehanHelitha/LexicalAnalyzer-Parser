RPAL Interpreter
This project is the culmination of the CS3513 - Programming Languages module, offered by the Department of Computer Science & Engineering, University of Moratuwa, completed in the 4th semester of Batch 22. It implements an interpreter for the RPAL (Right-reference Pedagogic Algorithmic Language) programming language, including a lexical analyzer, parser, and CSE machine.

Table of Contents

Problem Requirements
About Our Solution
Usage
Features
Project Structure
Modules
Lexical Analyzer
Screener
Parser
CSE Machine


Contributors
License


Problem Requirements
The project requires implementing a lexical analyzer and parser for the RPAL language, adhering to the lexical rules in RPAL_Lex and grammar in RPAL_Grammar. The interpreter must:

Generate an Abstract Syntax Tree (AST) from an input RPAL program.
Convert the AST into a Standardized Tree (ST).
Implement the CSE Machine to evaluate the ST based on the provided semantics (13 CSE rules).
Produce output matching the reference rpal.exe for any valid RPAL program.

Refer to the "About RPAL" documentation for detailed language specifications.

About Our Solution

Programming Language: Python (3.7 or higher)
Development & Testing Tools:
Visual Studio Code
Command Line (Cygwin for Windows compatibility)
Pytest for unit testing
GitHub Actions for CI/CD
Makefile for build automation



The solution is modular, with distinct components for lexical analysis, token screening, parsing, and program execution, ensuring maintainability and scalability.

Usage
Prerequisites

Python 3.7 or higher
pip (Python package manager)

Setup

Clone the repository or download the source code:git clone https://github.com/your-username/rpal-interpreter.git


Navigate to the project root directory:cd rpal-interpreter


Install the required Python dependencies:pip install -r requirements.txt



Running the Interpreter
The interpreter is executed from the src directory. Use the following command to run the interpreter or access specific outputs:
cd src
python myrpal.py [switch] ../testing_rpal_sources/<file_name>.rpal

Available Command-Line Switches



Switch
Description
Example Usage



(no switch)
Run the interpreter and produce program output
python myrpal.py ../testing_rpal_sources/example.rpal


-ast
Generate and display the Abstract Syntax Tree
python myrpal.py -ast ../testing_rpal_sources/example.rpal


-st
Generate and display the Standardized Tree
python myrpal.py -st ../testing_rpal_sources/example.rpal


-ct
Generate and display the CSE Machine table
python myrpal.py -ct ../testing_rpal_sources/example.rpal


-t
Generate and display the token list
python myrpal.py -t ../testing_rpal_sources/example.rpal


-ft
Generate and display the filtered token list
python myrpal.py -ft ../testing_rpal_sources/example.rpal



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

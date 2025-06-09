# RPAL Interpreter
A complete interpreter implementation for RPAL (Right-reference Pedagogic Algorithmic Language) built as part of CS3513 - Programming Languages module at the University of Moratuwa.

## 🎯 Overview
This project implements a full-featured RPAL interpreter that processes source code through multiple stages: lexical analysis, parsing, tree standardization, and execution via a CSE (Control-Stack-Environment) machine. The interpreter faithfully follows RPAL language specifications and produces output compatible with the reference implementation.

## ✨ Key Features
- **Complete Lexical Analysis** - Tokenizes RPAL source code following official lexical rules
- **Robust Parser** - Generates Abstract Syntax Trees (AST) with comprehensive error handling
- **Tree Standardization** - Transforms AST into Standardized Trees (ST) for execution
- **CSE Machine** - Executes programs using the 13 standardized CSE evaluation rules
- **Multiple Output Modes** - View tokens, trees, and execution states for debugging
- **Reference Compatibility** - Output matches the official rpal.exe implementation
- **Automated Build System** - Makefile for streamlined testing and development

## 📋 Requirements
Before running the interpreter, ensure you have:

- Python 3.7+ installed on your system
- pip package manager
- Git (for cloning the repository)
- Make (for using the automated build commands)

## 🚀 Quick Start

### Installation
1. Clone the repository
   ```bash
   git clone <repository-url>
   cd rpal-interpreter
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the Makefile (save the provided Makefile in your project root)

### Quick Test
```bash
# Run the default test using Makefile
make

# Or run manually
cd src
python myrpal.py ../testing_rpal_sources/test1.rpal
```

## 📖 Usage Guide

### Using the Makefile (Recommended)

The project includes a comprehensive Makefile for streamlined development and testing:

#### Quick Start Commands
```bash
# Run default test (test1.rpal)
make
# or
make default
# or  
make run_test1
```

#### Test Analysis Commands (for test1.rpal)
```bash
make ast_test1          # Generate and display AST
make tokens_test1       # Generate and display all tokens
make ftokens_test1      # Generate and display filtered tokens
make st_test1           # Generate and display Standardized Tree
make cse_test1          # Generate and display CSE Table
make list_src_test1     # List the source code of test1.rpal
```

#### Generic Commands (for any file)
```bash
# Run any RPAL file
make run_file FILE=filename.rpal

# Generate AST for any file
make ast_file FILE=filename.rpal

# Generate tokens for any file
make tokens_file FILE=filename.rpal
```

#### Utility Commands
```bash
make clean              # Remove temporary files
make help               # Display help message
```

#### Usage Examples
```bash
# Test different programs
make run_file FILE=test2.rpal
make run_file FILE=fibonacci.rpal

# Analyze program structure
make ast_file FILE=factorial.rpal
make st_file FILE=complex_program.rpal

# Debug tokenization
make tokens_file FILE=my_program.rpal

# Clean up after testing
make clean
```

### Manual Command Line Interface
You can also run the interpreter directly:

```bash
cd src
python myrpal.py [OPTION] <rpal-file>
```

#### Available Options
| Option | Description | Output |
|--------|-------------|--------|
| (none) | Execute program | Program execution results |
| -ast | Show AST | Abstract Syntax Tree visualization |
| -st | Show ST | Standardized Tree structure |
| -ct | Show CSE Table | CSE machine control structures |
| -t | Show Tokens | Raw lexical tokens |
| -ft | Show Filtered Tokens | Processed tokens after screening |
| -l | List Source | Display source code |

# Execute a program
python myrpal.py ../testing_rpal_sources/fibonacci.rpal

# View the Abstract Syntax Tree
python myrpal.py -ast ../testing_rpal_sources/factorial.rpal

# View the Standardized Tree
python myrpal.py -st ../testing_rpal_sources/test1.rpal

# View CSE machine control structures
python myrpal.py -ct ../testing_rpal_sources/test2.rpal

# Debug with raw token analysis
python myrpal.py -t ../testing_rpal_sources/simple.rpal

# View filtered tokens after screening
python myrpal.py -ft ../testing_rpal_sources/test3.rpal
```

## 🏗️ Architecture
The interpreter follows a modular design with four main processing stages:

**RPAL Source → Lexer → Parser → Standardizer → CSE Machine → Output**

### Core Components

#### 🔍 Lexical Analyzer (scanner.py)
- Converts source code into tokens using finite state automata
- Handles all RPAL lexical elements (identifiers, operators, literals, etc.)
- Implements comprehensive error detection for invalid characters

#### 🧹 Screener (screener.py)
- Filters token stream to remove whitespace and comments
- Prepares clean token sequence for parsing
- Maintains position information for error reporting

#### 🌳 Parser (parser.py)
- Constructs Abstract Syntax Tree from token stream
- Implements RPAL grammar rules with recursive descent parsing
- Transforms AST into Standardized Tree for execution

#### ⚙️ CSE Machine (cse_machine/)
- Executes standardized trees using stack-based evaluation
- Implements all 13 CSE machine rules
- Manages environments for variable scoping and function calls

## 📁 Project Structure
```
RPAL-Interpreter/
├── 📁 docs/
├── 📁 src/
│   ├── 📁 cse_machine/
│   │   ├── 📜 binop.py
│   │   ├── 📜 control_structure.py
│   │   ├── 📜 environment.py
│   │   ├── 📜 error_handler.py
│   │   ├── 📜 machine.py
│   │   ├── 📜 stack.py
│   │   ├── 📜 stlinearizer.py
│   │   ├── 📜 unop.py
│   │   └── 📜 utils.py
│   ├── 📁 interpreter/
│   │   └── 📜 interpreter.py
│   ├── 📁 lexical_analyzer/
│   │   └── 📜 scanner.py
│   ├── 📁 parser/
│   │   └── 📜 parser.py
│   ├── 📁 screener/
│   │   └── 📜 screener.py
│   ├── 📁 standardized_tree/
│   │   └── 📜 build_standardized_tree.py
│   ├── 📁 table_routines/
│   │   ├── 📜 accept_states.py
│   │   ├── 📜 char_map.py
│   │   ├── 📜 fsa_table.py
│   │   └── 📜 keywords.py
│   ├── 📁 utils/
│   │   ├── 📜 control_structure_evaluator.py
│   │   ├── 📜 file_handler.py
│   │   ├── 📜 node.py
│   │   ├── 📜 stack.py
│   │   ├── 📜 token_printer.py
│   │   ├── 📜 tokens.py
│   │   ├── 📜 tree_list.py
│   │   └── 📜 tree_printer.py
│   └── 📜 myrpal.py
├── 📁 testing_rpal_sources/
│   ├── 📄 test1.rpal
│   ├── 📄 test2.rpal
│   ├── 📄 test3.rpal
│   ├── 📄 test4.rpal
│   ├── 📄 test5.rpal
│   ├── 📄 test6.rpal
│   ├── 📄 test7.rpal
│   ├── 📄 test8.rpal
│   ├── 📄 test9.rpal
│   └── 📄 test10.txt
├── 📄 Makefile
├── 📄 .gitignore
├── 📄 README.md
└── 📄 requirements.txt
```

## 🧪 Testing

### Using Makefile (Recommended)
```bash
# Run comprehensive tests
make run_test1
make run_file FILE=test2.rpal
make run_file FILE=test3.rpal

# Analyze test outputs
make ast_test1
make st_test1
make cse_test1

# Debug specific tests
make tokens_file FILE=test5.rpal
make ftokens_file FILE=test6.rpal
```

### Manual Testing
```bash
# Run basic tests
cd src
python myrpal.py ../testing_rpal_sources/basic_ops.rpal

# Test complex programs
python myrpal.py ../testing_rpal_sources/recursive_functions.rpal

# Validate against reference implementation
python myrpal.py ../testing_rpal_sources/complex.rpal > output.txt
```

## 🛠️ Development

### Code Organization
- **Modular Design**: Each component is self-contained with clear interfaces
- **Error Handling**: Comprehensive error detection and reporting throughout
- **Documentation**: Well-documented code with clear function signatures
- **Testing**: Extensive test coverage with sample RPAL programs

### Key Algorithms
- **Lexical Analysis**: Finite State Automaton for tokenization
- **Parsing**: Recursive Descent Parser with predictive parsing
- **Tree Building**: AST construction with proper node relationships
- **Standardization**: Rule-based AST to ST transformation
- **Execution**: Stack-based evaluation with environment management

### Development Workflow
```bash
# Set up development environment
git clone <repository-url>
cd rpal-interpreter
pip install -r requirements.txt

# Test your changes
make clean
make run_test1
make ast_test1

# Run comprehensive tests
make run_file FILE=test2.rpal
make run_file FILE=complex_program.rpal

# Clean up
make clean
```

## 📚 Language Support
The interpreter supports the complete RPAL language specification including:

- **Data Types**: Integers, strings, booleans, tuples, functions
- **Operators**: Arithmetic, logical, comparison, and string operations
- **Control Flow**: Conditional expressions, recursion
- **Functions**: Lambda expressions, function application, currying
- **Pattern Matching**: Tuple destructuring and parameter binding

## 🤝 Contributing
This project was developed as part of academic coursework. If you'd like to contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

### Testing Your Contributions
```bash
# Verify your changes don't break existing functionality
make clean
make run_test1
make ast_test1
make st_test1

# Test with multiple files
make run_file FILE=test2.rpal
make run_file FILE=test3.rpal
```

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🎓 Academic Context
- **Course**: CS3513 - Programming Languages
- **Institution**: Department of Computer Science & Engineering, University of Moratuwa
- **Semester**: 4th Semester, Batch 22

This implementation demonstrates practical application of compiler design principles including lexical analysis, syntax analysis, semantic analysis, and code execution.

## 📞 Support
For questions or issues:

- 📧 Create an issue in the repository
- 📖 Refer to the RPAL language documentation in the docs/ folder
- 🔍 Check existing test cases for usage examples
- 🛠️ Use `make help` to see all available commands

## 🎯 Quick Reference

### Most Common Commands
```bash
make                    # Run default test
make ast_test1         # View AST structure
make run_file FILE=x   # Run specific file
make clean             # Clean temporary files
make help              # Show all commands
```

---

Built with ❤️ for the Programming Languages community
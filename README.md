# RPAL Interpreter

A complete interpreter implementation for **RPAL** (Right-reference Pedagogic Algorithmic Language) built as part of CS3513 - Programming Languages module at the University of Moratuwa.

## 🎯 Overview

This project implements a full-featured RPAL interpreter that processes source code through multiple stages: lexical analysis, parsing, tree standardization, and execution via a CSE (Control-Stack-Environment) machine. The interpreter faithfully follows RPAL language specifications and produces output compatible with the reference implementation.

## ✨ Key Features

- **Complete Lexical Analysis** - Tokenizes RPAL source code following official lexical rules
- **Robust Parser** - Generates Abstract Syntax Trees (AST) with comprehensive error handling  
- **Tree Standardization** - Transforms AST into Standardized Trees (ST) for execution
- **CSE Machine** - Executes programs using the 13 standardized CSE evaluation rules
- **Multiple Output Modes** - View tokens, trees, and execution states for debugging
- **Reference Compatibility** - Output matches the official `rpal.exe` implementation

## 📋 Requirements

Before running the interpreter, ensure you have:

- **Python 3.7+** installed on your system
- **pip** package manager
- **Git** (for cloning the repository)

## 🚀 Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd rpal-interpreter
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

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

### Command Line Interface

The interpreter supports various command-line switches for different output modes:

```bash
python myrpal.py [OPTION] <rpal-file>
```

#### Available Options

| Option | Description | Output |
|--------|-------------|---------|
| *(none)* | **Execute program** | Program execution results |
| `-ast` | **Show AST** | Abstract Syntax Tree visualization |
| `-st` | **Show ST** | Standardized Tree structure |
| `-ct` | **Show CSE Table** | CSE machine control structures |
| `-t` | **Show Tokens** | Raw lexical tokens |
| `-ft` | **Show Filtered Tokens** | Processed tokens after screening |

#### Example Commands

```bash
# Execute a program
python myrpal.py ../testing_rpal_sources/fibonacci.rpal

# View the Abstract Syntax Tree
python myrpal.py -ast ../testing_rpal_sources/factorial.rpal

# Debug with token analysis
python myrpal.py -t ../testing_rpal_sources/simple.rpal
```

## 🏗️ Architecture

The interpreter follows a modular design with four main processing stages:

```
RPAL Source → Lexer → Parser → Standardizer → CSE Machine → Output
```

### Core Components

#### 🔍 **Lexical Analyzer** (`scanner.py`)
- Converts source code into tokens using finite state automata
- Handles all RPAL lexical elements (identifiers, operators, literals, etc.)
- Implements comprehensive error detection for invalid characters

#### 🧹 **Screener** (`screener.py`) 
- Filters token stream to remove whitespace and comments
- Prepares clean token sequence for parsing
- Maintains position information for error reporting

#### 🌳 **Parser** (`parser.py`)
- Constructs Abstract Syntax Tree from token stream
- Implements RPAL grammar rules with recursive descent parsing
- Transforms AST into Standardized Tree for execution

#### ⚙️ **CSE Machine** (`cse_machine/`)
- Executes standardized trees using stack-based evaluation
- Implements all 13 CSE machine rules
- Manages environments for variable scoping and function calls

## 📁 Project Structure

```
rpal-interpreter/
├── 📁 docs/                     # Documentation files
├── 📁 src/                      # Source code
│   ├── 📁 cse_machine/          # CSE Machine implementation
│   │   ├── 📜 binop.py          # Binary operations
│   │   ├── 📜 control_structure.py # Control structures
│   │   ├── 📜 environment.py    # Environment management
│   │   ├── 📜 error_handler.py  # Error handling
│   │   ├── 📜 machine.py        # Main CSE machine
│   │   ├── 📜 stack.py          # Stack operations
│   │   ├── 📜 stlinearizer.py   # ST linearization
│   │   ├── 📜 unop.py           # Unary operations
│   │   └── 📜 utils.py          # Utility functions
│   ├── 📁 interpreter/
│   │   └── 📜 interpreter.py    # Main interpreter logic
│   ├── 📁 lexical_analyzer/
│   │   └── 📜 scanner.py        # Lexical analysis
│   ├── 📁 parser/
│   │   └── 📜 parser.py         # Syntax analysis
│   ├── 📁 screener/
│   │   └── 📜 screener.py       # Token filtering
│   ├── 📁 standardized_tree/
│   │   └── 📜 build_standardized_tree.py # Tree standardization
│   ├── 📁 table_routines/       # FSA tables and utilities
│   │   ├── 📜 accept_states.py  # Acceptance states
│   │   ├── 📜 char_map.py       # Character mapping
│   │   ├── 📜 fsa_table.py      # FSA transition table
│   │   └── 📜 keywords.py       # RPAL keywords
│   ├── 📁 utils/                # Utility modules
│   │   ├── 📜 control_structure_entities.py
│   │   ├── 📜 file_handler.py   # File I/O operations
│   │   ├── 📜 node.py           # Tree node definitions
│   │   ├── 📜 stack.py          # Stack data structure
│   │   ├── 📜 token_printer.py  # Token display utilities
│   │   ├── 📜 tokens.py         # Token definitions
│   │   ├── 📜 tree_list.py      # Tree list operations
│   │   └── 📜 tree_printer.py   # Tree visualization
│   └── 📜 myrpal.py             # Main entry point
├── 📁 testing_rpal_sources/     # Test RPAL programs
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
├── 📄 .gitignore               # Git ignore rules
├── 📄 Makefile                 # Build automation
├── 📄 README.md                # This file
└── 📄 requirements.txt         # Python dependencies
```

## 🧪 Testing

The project includes comprehensive test cases in the `testing_rpal_sources/` directory:

```bash
# Run basic tests
python myrpal.py ../testing_rpal_sources/test1.rpal

# Test complex programs  
python myrpal.py ../testing_rpal_sources/test2.rpal

# Validate against reference implementation
python myrpal.py ../testing_rpal_sources/test3.rpal > output.txt
```

### Test Cases

The test suite includes programs that verify:
- **Basic arithmetic operations**
- **Function definitions and calls**
- **Recursive functions**
- **Conditional expressions**
- **Tuple operations**
- **String manipulations**
- **Complex nested expressions**

## 🛠️ Development

### Code Organization

- **Modular Design**: Each component is self-contained with clear interfaces
- **Error Handling**: Comprehensive error detection and reporting throughout
- **Documentation**: Well-documented code with clear function signatures
- **Testing**: Extensive test coverage with sample RPAL programs

### Key Algorithms

1. **Lexical Analysis**: Finite State Automaton for tokenization
2. **Parsing**: Recursive Descent Parser with predictive parsing
3. **Tree Building**: AST construction with proper node relationships  
4. **Standardization**: Rule-based AST to ST transformation
5. **Execution**: Stack-based evaluation with environment management

## 📚 Language Support

The interpreter supports the complete RPAL language specification including:

- **Data Types**: Integers, strings, booleans, tuples, functions
- **Operators**: Arithmetic, logical, comparison, and string operations
- **Control Flow**: Conditional expressions, recursion
- **Functions**: Lambda expressions, function application, currying
- **Pattern Matching**: Tuple destructuring and parameter binding
- **Built-in Functions**: Print, arithmetic operations, string operations

### Example RPAL Programs

```rpal
// Factorial function
let rec factorial n = 
    n eq 0 -> 1 | n * factorial (n-1)
in factorial 5

// Fibonacci sequence
let rec fib n = 
    n le 1 -> n | fib(n-1) + fib(n-2)
in fib 10

// List operations
let list = (1, 2, 3, 4, 5) in
let head x = x 1 in
let tail x = x 2 in
print head list
```

## 🐛 Debugging

When encountering issues:

1. **Check syntax**: Use `-ast` to view the parsed tree structure
2. **Examine tokens**: Use `-t` or `-ft` to inspect tokenization
3. **Trace execution**: Use `-ct` to see CSE machine states
4. **Validate input**: Ensure proper RPAL syntax and semantics

## 🤝 Contributing

This project was developed as part of academic coursework. If you'd like to contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

### Development Guidelines

- Follow existing code style and conventions
- Add tests for new features
- Update documentation as needed
- Ensure compatibility with reference implementation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎓 Academic Context

**Course**: CS3513 - Programming Languages  
**Institution**: Department of Computer Science & Engineering, University of Moratuwa  
**Semester**: 4th Semester, Batch 22

This implementation demonstrates practical application of compiler design principles including lexical analysis, syntax analysis, semantic analysis, and code execution.

## 📈 Performance

The interpreter is optimized for:
- **Memory efficiency**: Proper memory management in CSE machine
- **Execution speed**: Optimized tree traversal and evaluation
- **Error handling**: Fast error detection and meaningful error messages

## 🔧 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed via `pip install -r requirements.txt`
2. **File Not Found**: Check that RPAL source files exist and paths are correct
3. **Syntax Errors**: Verify RPAL program syntax matches language specification
4. **Execution Errors**: Use debug flags to trace program execution

### Error Messages

The interpreter provides detailed error messages including:
- **Lexical errors**: Invalid characters or malformed tokens
- **Syntax errors**: Grammar violations with line numbers
- **Runtime errors**: Type mismatches and undefined variables
- **Semantic errors**: Invalid operations and scope violations

## 📞 Support

For questions or issues:

- 📧 Create an issue in the repository
- 📖 Refer to the RPAL language documentation in the `docs/` folder
- 🔍 Check existing test cases for usage examples
- 💬 Review the source code comments for implementation details

## 🏆 Acknowledgments

- **Dr. [Professor Name]** - Course instructor and guidance
- **University of Moratuwa** - Academic institution
- **RPAL Language Specification** - Reference documentation
- **CS3513 Course Materials** - Theoretical foundation

---

*Built with ❤️ for the Programming Languages community*

## 📚 Additional Resources

- [RPAL Language Specification](docs/rpal_spec.pdf)
- [CSE Machine Documentation](docs/cse_machine.md)
- [Project Report](docs/project_report.pdf)
- [API Documentation](docs/api_docs.md)
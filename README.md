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

### Basic Usage

Navigate to the source directory and run:

```bash
cd src
python myrpal.py ../testing_rpal_sources/sample.rpal
```

## 📖 Usage Guide

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
├── 📁 src/                          # Main source code
│   ├── 📁 cse_machine/              # CSE machine implementation
│   │   ├── machine.py               # Core CSE machine logic
│   │   ├── environment.py           # Environment management
│   │   ├── stack.py                 # Stack operations
│   │   └── ...
│   ├── 📁 table_routines/           # FSA tables and lexical rules
│   ├── 📁 utils/                    # Shared utilities
│   ├── myrpal.py                    # Main interpreter entry point
│   ├── scanner.py                   # Lexical analyzer
│   ├── screener.py                  # Token filter
│   └── parser.py                    # Parser implementation
├── 📁 testing_rpal_sources/         # Test RPAL programs
├── 📁 docs/                         # Documentation
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## 🧪 Testing

The project includes comprehensive test cases in the `testing_rpal_sources/` directory:

```bash
# Run basic tests
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

## 🤝 Contributing

This project was developed as part of academic coursework. If you'd like to contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎓 Academic Context

**Course**: CS3513 - Programming Languages  
**Institution**: Department of Computer Science & Engineering, University of Moratuwa  
**Semester**: 4th Semester, Batch 22

This implementation demonstrates practical application of compiler design principles including lexical analysis, syntax analysis, semantic analysis, and code execution.

## 📞 Support

For questions or issues:

- 📧 Create an issue in the repository
- 📖 Refer to the RPAL language documentation in the `docs/` folder
- 🔍 Check existing test cases for usage examples

---

*Built with ❤️ for the Programming Languages community*
# Enhanced Calculator Command-Line Application

An interactive command-line calculator built in Python, featuring persistent history, undo/redo support, and comprehensive logging. The application demonstrates several design patterns and includes a full test suite with 100% code coverage.

## Features

- **Interactive REPL** — type commands to perform calculations, manage history, and more
- **10 Arithmetic Operations** — add, subtract, multiply, divide, power, root, modulus, integer division, percentage, absolute difference
- **Calculation History** — view, save, load, and clear past calculations (CSV via `pandas`)
- **Undo / Redo** — undo or redo operations using the Memento pattern
- **Input Validation** — validates numeric input with configurable maximum values
- **Comprehensive Logging** — all operations, errors, and events logged to file
- **Environment-Based Configuration** — settings loaded from a `.env` file via `python-dotenv`
- **Observer Pattern** — auto-save and logging observers react to each calculation
- **100% Test Coverage** — full `pytest` suite with `pytest-cov`

## Design Patterns

| Pattern | Where | Purpose |
|---------|-------|---------|
| **Strategy** | `operations.py` | Each operation is an interchangeable strategy class |
| **Factory** | `operations.py` | `OperationFactory` creates operations by name |
| **Observer** | `history.py` | `LoggingObserver` and `AutoSaveObserver` react to calculations |
| **Memento** | `calculator_memento.py` | Captures history snapshots for undo/redo |

## Project Structure

```
app/
├── __init__.py
├── calculation.py
├── calculator.py
├── calculator_config.py
├── calculator_memento.py
├── calculator_repl.py
├── exceptions.py
├── history.py
├── input_validators.py
└── operations.py
tests/
├── __init__.py
├── test_calculation.py
├── test_calculator.py
├── test_calculator_config.py
├── test_calculator_memento.py
├── test_calculator_repl.py
├── test_exceptions.py
├── test_history.py
├── test_input_validators.py
└── test_operations.py
```

## Requirements

- Git
- Python 3.10 or newer

## Setup

Clone the repository:

```bash
git clone https://github.com/thejps92/is601-midterm-project
cd is601-midterm-project
```

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

> [!NOTE]
> The previous commands are for **Windows PowerShell.** On macOS or Linux, use `source venv/bin/activate` instead.

## Configuration

The application loads settings from a `.env` file in the project root. A default `.env` file is included:

| Variable | Default | Description |
|----------|---------|-------------|
| `CALCULATOR_LOG_DIR` | `logs` | Directory for log files |
| `CALCULATOR_HISTORY_DIR` | `history` | Directory for history CSV files |
| `CALCULATOR_MAX_HISTORY_SIZE` | `1000` | Maximum number of calculations to store |
| `CALCULATOR_AUTO_SAVE` | `true` | Automatically save history after each calculation |
| `CALCULATOR_PRECISION` | `10` | Decimal precision for result formatting |
| `CALCULATOR_MAX_INPUT_VALUE` | `1e999` | Maximum allowed input value |
| `CALCULATOR_DEFAULT_ENCODING` | `utf-8` | File encoding |

You can modify these values in the `.env` file to customize the calculator's behavior.

## Running the Calculator

```bash
python main.py
```

### Available Commands

| Command | Description |
|---------|-------------|
| `add` | Addition (a + b) |
| `subtract` | Subtraction (a - b) |
| `multiply` | Multiplication (a × b) |
| `divide` | Division (a ÷ b) |
| `power` | Exponentiation (a ^ b) |
| `root` | Nth root (ᵇ√a) |
| `modulus` | Remainder (a mod b) |
| `int_divide` | Integer division (a ÷ b, truncated) |
| `percent` | Percentage (a / b × 100) |
| `abs_diff` | Absolute difference (\|a - b\|) |
| `history` | Show calculation history |
| `clear` | Clear calculation history |
| `undo` | Undo the last calculation |
| `redo` | Redo the last undone calculation |
| `save` | Save history to CSV file |
| `load` | Load history from CSV file |
| `help` | Show available commands |
| `exit` | Exit the calculator |

### Example Session

```
Calculator started. Type 'help' for commands.

Enter command: add

Enter numbers (or 'cancel' to abort):
First number: 10
Second number: 5

Result: 15

Enter command: multiply

Enter numbers (or 'cancel' to abort):
First number: 3
Second number: 7

Result: 21

Enter command: history

Calculation History:
1. Addition(10, 5) = 15
2. Multiplication(3, 7) = 21

Enter command: undo
Operation undone

Enter command: exit
History saved successfully.
Goodbye!
```

## Running Tests

Run all tests with coverage reporting:

```bash
pytest --cov=app --cov-report=term-missing
```

Run tests without coverage:

```bash
pytest
```

Generate an HTML coverage report:

```bash
pytest --cov=app --cov-report=html
```

The HTML report will be generated in the `htmlcov/` directory.
"""Read-Eval-Print Loop (REPL) for the interactive calculator.

Provides a command-line interface for performing arithmetic operations,
managing history, and undo/redo support.
"""

from decimal import Decimal
import logging

from colorama import init, Fore, Style

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory

# Initialize colorama for cross-platform colored output
init(autoreset=True)


def calculator_repl():
    """Start the interactive calculator REPL."""
    try:
        calc = Calculator()

        calc.add_observer(LoggingObserver())
        calc.add_observer(AutoSaveObserver(calc))

        print(Fore.CYAN + "Calculator started. Type 'help' for commands.")

        while True:
            try:
                command = input("\nEnter command: ").lower().strip()

                if command == 'help':
                    print(Fore.CYAN + "\nAvailable commands:")
                    print(Fore.CYAN + "  add, subtract, multiply, divide, power, root, modulus, int_divide, percent, abs_diff - Perform calculations")
                    print(Fore.CYAN + "  history - Show calculation history")
                    print(Fore.CYAN + "  clear - Clear calculation history")
                    print(Fore.CYAN + "  undo - Undo the last calculation")
                    print(Fore.CYAN + "  redo - Redo the last undone calculation")
                    print(Fore.CYAN + "  save - Save calculation history to file")
                    print(Fore.CYAN + "  load - Load calculation history from file")
                    print(Fore.CYAN + "  exit - Exit the calculator")
                    continue

                if command == 'exit':
                    try:
                        calc.save_history()
                        print(Fore.GREEN + "History saved successfully.")
                    except Exception as e:
                        logging.warning(f"Could not save history on exit: {e}")
                        print(Fore.YELLOW + f"Warning: Could not save history: {e}")
                    logging.info("Calculator exiting")
                    print(Fore.CYAN + "Goodbye!")
                    break

                if command == 'history':
                    history = calc.show_history()
                    if not history:
                        print(Fore.YELLOW + "No calculations in history")
                    else:
                        print(Fore.CYAN + "\nCalculation History:")
                        for i, entry in enumerate(history, 1):
                            print(f"{i}. {entry}")
                    continue

                if command == 'clear':
                    calc.clear_history()
                    print(Fore.GREEN + "History cleared")
                    continue

                if command == 'undo':
                    if calc.undo():
                        print(Fore.GREEN + "Operation undone")
                    else:
                        print(Fore.YELLOW + "Nothing to undo")
                    continue

                if command == 'redo':
                    if calc.redo():
                        print(Fore.GREEN + "Operation redone")
                    else:
                        print(Fore.YELLOW + "Nothing to redo")
                    continue

                if command == 'save':
                    try:
                        calc.save_history()
                        print(Fore.GREEN + "History saved successfully")
                    except Exception as e:
                        print(Fore.RED + f"Error saving history: {e}")
                    continue

                if command == 'load':
                    try:
                        calc.load_history()
                        print(Fore.GREEN + "History loaded successfully")
                    except Exception as e:
                        print(Fore.RED + f"Error loading history: {e}")
                    continue

                if command in ['add', 'subtract', 'multiply', 'divide', 'power', 'root', 'modulus', 'int_divide', 'percent', 'abs_diff']:
                    try:
                        print("\nEnter numbers (or 'cancel' to abort):")
                        a = input("First number: ")
                        if a.lower() == 'cancel':
                            print(Fore.YELLOW + "Operation cancelled")
                            continue
                        b = input("Second number: ")
                        if b.lower() == 'cancel':
                            print(Fore.YELLOW + "Operation cancelled")
                            continue

                        operation = OperationFactory.create_operation(command)
                        calc.set_operation(operation)

                        result = calc.perform_operation(a, b)

                        if isinstance(result, Decimal):
                            result = result.normalize()
                            if result.as_tuple().exponent > 0:
                                result = result.quantize(Decimal('1'))

                        print(Fore.GREEN + f"\nResult: {result}")
                    except (ValidationError, OperationError) as e:
                        logging.error(f"Operation error: {e}")
                        print(Fore.RED + f"Error: {e}")
                    except Exception as e:
                        logging.error(f"Unexpected error during operation: {e}")
                        print(Fore.RED + f"Unexpected error: {e}")
                    continue

                logging.warning(f"Unknown command entered: '{command}'")
                print(Fore.YELLOW + f"Unknown command: '{command}'. Type 'help' for available commands.")

            except KeyboardInterrupt:
                logging.warning("Operation cancelled by user (KeyboardInterrupt)")
                print(Fore.YELLOW + "\nOperation cancelled")
                continue
            except EOFError:
                logging.info("Input terminated (EOFError)")
                print(Fore.YELLOW + "\nInput terminated. Exiting...")
                break
            except Exception as e:
                logging.error(f"Unexpected error in REPL loop: {e}")
                print(Fore.RED + f"Error: {e}")
                continue

    except Exception as e:
        print(Fore.RED + f"Fatal error: {e}")
        logging.error(f"Fatal error in calculator REPL: {e}")
        raise
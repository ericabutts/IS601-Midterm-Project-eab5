

from decimal import Decimal
import logging

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory

from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)



def calculator_repl():
    """
    Command-line interface for the calculator.
    Implements a Read-Eval-Print Loop (REPL) for operations, history, undo/redo, and persistence.
    """
    try:
        # Initialize calculator
        calc = Calculator()

        # Add observers for logging and auto-saving
        calc.add_observer(LoggingObserver())
        calc.add_observer(AutoSaveObserver(calc))

        print(Fore.GREEN+f"Calculator started. Type 'help' for commands.")

        while True:
            try:
                command = input(Fore.GREEN+f"\nEnter command: ").lower().strip()

                if command == 'help':
                    print(Fore.GREEN+f"\nAvailable commands:")
                    print(Fore.GREEN+f"  add, subtract, multiply, divide, power, root - Perform calculations")
                    print(Fore.GREEN+f"  history - Show calculation history")
                    print(Fore.GREEN+f"  clear - Clear calculation history")
                    print(Fore.GREEN+f"  undo - Undo the last calculation")
                    print(Fore.GREEN+f"  redo - Redo the last undone calculation")
                    print(Fore.GREEN+f"  save - Save calculation history to file")
                    print(Fore.GREEN+f"  load - Load calculation history from file")
                    print(Fore.GREEN+f"  exit - Exit the calculator")
                    continue

                if command == 'exit':
                    try:
                        calc.save_history()
                        print(Fore.GREEN+f"History saved successfully.")
                    except Exception as e:
                        print(Fore.YELLOW + f"Warning: Could not save history: {e}")
                    print("Goodbye!")
                    break

                if command == 'history':
                    history = calc.show_history()
                    if not history:
                        print(Fore.RED + f"No calculations in history")
                    else:
                        print(Fore.GREEN+f"\nCalculation History:")
                        for i, entry in enumerate(history, 1):
                            print(Fore.BLUE+f"{i}. {entry}")
                    continue

                if command == 'clear':
                    calc.clear_history()
                    print(Fore.GREEN+f"History cleared")
                    continue

                if command == 'undo':
                    if calc.undo():
                        print(Fore.YELLOW+f"Operation undone")
                    else:
                        print(Fore.YELLOW+f"Nothing to undo")
                    continue

                if command == 'redo':
                    if calc.redo():
                        print(Fore.YELLOW+f"Operation redone")
                    else:
                        print(Fore.YELLOW+f"Nothing to redo")
                    continue

                if command == 'save':
                    try:
                        calc.save_history()
                        print(Fore.GREEN+f"History saved successfully")
                    except Exception as e:
                        print(Fore.RED+f"Error saving history: {e}")
                    continue

                if command == 'load':
                    try:
                        calc.load_history()
                        print(Fore.GREEN+f"History loaded successfully")
                    except Exception as e:
                        print(Fore.RED+f"Error loading history: {e}")
                    continue

                if command in ['add', 'subtract', 'multiply', 'divide', 'power', 'root', 'integerdivision', 'modulus', 'percentage', 'absolutedifference']:
                    print("\nEnter numbers (or 'cancel' to abort):")
                    a = input(Fore.CYAN +f"First number: " + Style.RESET_ALL)
                    if a.lower() == 'cancel':
                        print(Fore.YELLOW+f"Operation cancelled")
                        continue
                    b = input(Fore.CYAN+f"Second number: "+ Style.RESET_ALL)
                    if b.lower() == 'cancel':
                        print(Fore.YELLOW+f"Operation cancelled")
                        continue

                    try:
                        operation = OperationFactory.create_operation(command)
                        calc.set_operation(operation)
                        result = calc.perform_operation(a, b)

                        # Normalize Decimal result
                        if isinstance(result, Decimal):
                            result = result.normalize()

                        print(Fore.GREEN+f"\nResult: {result}")
                    except (ValidationError, OperationError) as e:
                        print(Fore.RED+f"Error: {e}")
                    except Exception as e:
                        print(Fore.RED+f"Unexpected error: {e}")
                    continue

                print(Fore.YELLOW+f"Unknown command: '{command}'. Type 'help' for available commands.")

            except (KeyboardInterrupt, EOFError):
                print(Fore.RED+f"\nOperation cancelled or input terminated. Exiting...")
                break
            except Exception as e:
                print(Fore.RED+f"Error: {e}")
                continue

    except Exception as e:
        print(Fore.RED+f"Fatal error: {e}")
        logging.error(f"Fatal error in calculator REPL: {e}")
        raise

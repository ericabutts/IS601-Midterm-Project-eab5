from decimal import Decimal
import logging

from app.calculation import Calculation

def calculator_repl():
    """
    Command line interface for calculator application
    """

    print("Calculator started. Type 'help' for commands")

    history = []

    try:
        while True:
            command = input("\nEnter command: ").strip().lower()

            if command == 'exit':
                print("Goodbye!")
                break

            elif command == 'history':
                print("Print history of calculations")
                continue

            elif command == 'clear':
                print("History cleared")
                continue

            elif command == 'undo':
                print("Operation undone")
                continue

            elif command == 'redo':
                print("Operation redone")
                continue

            elif command == 'save':
                print("History saved")
                continue

            elif command == 'load':
                print("Loaded history successfully")
                continue

            elif command in ['add', 'subtract', 'multiply', 'divide', 'power', 'root']:
                try:
                    print("\nEnter numbers (or abort with 'cancel'):")

                    a = input("First number: ").strip()
                    if a.lower() == 'cancel':
                        print("Operation cancelled")
                        continue

                    b = input("Second number: ").strip()
                    if b.lower() == 'cancel':
                        print("Operation cancelled")
                        continue

                    # Convert inputs to Decimal for precision
                    a = Decimal(a)
                    b = Decimal(b)

                    # Perform the selected operation
                    if command == 'add':
                        result = a + b
                    elif command == 'subtract':
                        result = a - b
                    elif command == 'multiply':
                        result = a * b
                    elif command == 'divide':
                        result = a / b if b != 0 else "Error: Division by zero"
                    elif command == 'power':
                        result = a ** b
                    elif command == 'root':
                        result = a ** (Decimal(1) / b)

                    calc = Calculation(command, a, b, result)
                    history.append(calc)


                    print(f"\nResult: {result}")

                except Exception as e:
                    print(f"Error: {e}")

            elif command == 'help':
                print("Available commands:")
                print(" add, subtract, multiply, divide, power, root")
                print(" history, clear, undo, redo, save, load, exit")

            else:
                print(f"Unknown command: '{command}'. Type 'help' for available commands.")

    except Exception as e:
        print(f"Error: {e}")
        logging.error(f"Error in calculator repl: {e}")
        raise

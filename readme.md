Project Description: Overview of the calculator application and its features.

This project is a command-line Read Evaluate Print Loop (REPL) calculator application.

Installation Instructions: Steps to set up the virtual environment and install dependencies.

    git clone <repo link>
    cd IS601_MIDTERM_MODULE
    pip install -m requirements.txt

Configuration Setup: Instructions on creating and configuring the .env file with necessary environment variables.


Usage Guide: Detailed explanation of how to use the command-line interface and its supported commands.

The following commands are available:

    exit:
        Quit the program.

    help:
        List all possible commands.

    undo:
        Remove the previous calculation from the history.

    redo:
        Restore the most recently deleted calculation.

    save: 
        Save all calculations to a history file.

    load:
        Load a save file of calculation history.

    add:
        Add two numbers together.

        First number<Decimal>: the first operand.
        Second number <Decimal>: the second operand.

    subtract:
        Subtract a number from another number.

        First number<Decimal>: the first operand.
        Second number <Decimal>: the second operand.

    multiply:
        Multiply two numbers.

        First number<Decimal>: the first operand.
        Second number <Decimal>: the second operand.

    divide:
        Divide one number by another.

        First number<Decimal>: the first operand.
        Second number <Decimal>: the second operand.

    power: 
        Raise one number to the power of another.

        First number<Decimal>: the first operand.
        Second number <Decimal>: the second operand.

    root: 
        Calculate the nth root of a number.

        First number<Decimal>: the first operand.
        Second number <Decimal>: the second operand.

    modulus: 
        Compute the remainder of the division of two numbers.

        First number<Decimal>: the first operand.
        Second number <Decimal>: the second operand.

    integerdivide (known as Integer Division): 
        Perform division that results in an integer quotient, discarding any fractional part.

        First number<Decimal>: the first operand.
        Second number <Decimal>: the second operand.

    percentcalculation (known as Percentage Calculation): 
        Calculate the percentage of one number with respect to another (e.g., Percentage(a, b) computes (a / b) * 100).

        First number<Decimal>: the first operand.
        Second number <Decimal>: the second operand.

    absolutedifference: 
        Calculate the absolute difference between two numbers

        First number<Decimal>: the first operand.
        Second number <Decimal>: the second operand.

Testing Instructions: How to run unit tests and check test coverage.

    cd IS601_MIDTERM_MODULE
    pytest

CI/CD Information: Overview of GitHub Actions workflow and its purpose.

    Pushing commits to the repository triggers the GitHub Actions workflow. 
    The unit tests stored in the tests folders will run upon push.
    The tests will fail if the changes result in less than 90% coverage.


Include instructions on setting up .env files and configuring logging.
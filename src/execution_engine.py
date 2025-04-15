# execution_engine.py
import sys
from cse_machine import CSEMachine, CseMachineError # Import the machine and its error
from utils.node import Node # To check input type

def interpret(standardized_tree):
    """
    Interprets the given Standardized Tree (ST) using the CSE machine.

    Args:
        standardized_tree: The root Node of the ST.

    Returns:
        The final computed value, or None if an error occurred or execution
        resulted in an empty stack.

    Raises:
        CseMachineError: If a runtime error occurs during evaluation.
        TypeError: If the input is not a valid Node.
    """
    if not isinstance(standardized_tree, Node):
        raise TypeError("Interpreter input must be a valid Standardized Tree Node.")

    cse_machine = CSEMachine()
    try:
        result = cse_machine.evaluate(standardized_tree)
        return result
    except CseMachineError as e:
        # Re-raise the error for the main script to handle
        raise e
    except Exception as e:
        # Catch other potential unexpected errors from CSE evaluate
        raise CseMachineError(f"Unexpected error during CSE evaluation: {e}") from e


def format_result(result_value):
    """
    Formats the raw result value from the interpreter for printing.
    (This could live in CSEMachine too, but separating it here emphasizes
     the engine's role in final output presentation).

    Args:
        result_value: The value returned by the interpret function.

    Returns:
        A string representation suitable for printing, or None if input is None.
    """
    if result_value is None:
        return None # No result to format

    # Use a temporary CSE machine instance just to access its formatting method
    # Alternatively, make _format_value static or move it here.
    temp_cse = CSEMachine()
    return temp_cse._format_value(result_value)


# Example Usage (for testing execution_engine.py directly)
if __name__ == '__main__':
    # Requires Standardized Tree input
    # Example ST for: let x = 10 in x + 5 => Should evaluate to 15
    st_let_example = Node('gamma', children=[
                            Node('lambda', children=[
                                Node('ID', 'x'),
                                Node('gamma', children=[
                                     Node('gamma', children=[Node('ID', '+'), Node('ID', 'x')]),
                                     Node('INT', 5)
                                ])
                            ]),
                            Node('=', children=[Node('ID', 'x'), Node('INT', 10)])
                        ])

    print("--- Interpreting ST for: let x = 10 in x + 5 ---")
    try:
        final_value = interpret(st_let_example)
        formatted_output = format_result(final_value)
        print(f"\nFormatted Result: {formatted_output} (Expected: 15)")
    except (CseMachineError, TypeError) as e:
        print(f"\nInterpretation Error: {e}")
    except Exception as e:
        print(f"\nUnexpected Error: {e}")
        import traceback
        traceback.print_exc()
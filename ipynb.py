import json
import os


def append_code_to_ipynb(code_str, output_filename):
    """
    Appends Python code to an existing .ipynb Jupyter Notebook file, or creates a new one if it doesn't exist.

    Args:
    - code_str (str): A string containing Python code.
    - output_filename (str): The desired output filename for the .ipynb file.

    Returns:
    - None: Updates or creates the .ipynb file.
    """

    # Check if the file exists
    if os.path.exists(output_filename):
        # Open the existing file
        with open(output_filename, "r", encoding="utf-8") as f:
            notebook = json.load(f)
    else:
        # If file doesn't exist, create a new notebook structure
        notebook = {"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 5}

    # Split the code string by newlines
    code_lines = code_str.split("\n")

    # Create a new code cell
    new_cell = {
        "cell_type": "code",
        "metadata": {},
        "outputs": [],
        "source": code_lines,
        "execution_count": None,
    }

    # Append the new cell to the notebook's cells
    notebook["cells"].append(new_cell)

    # Write the updated notebook back to the file
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=2)


if __name__ == "__main__":
    # Example usage
    code_chunk1 = """
    def greet(name):
        return f"Hello, {name}!"
    """

    code_chunk2 = """
    print(greet('World'))
    """

    # Stream the code into the same notebook
    append_code_to_ipynb(code_chunk1, "streamed_notebook.ipynb")
    append_code_to_ipynb(code_chunk2, "streamed_notebook.ipynb")

# -*- coding: utf-8 -*-
"""
Example usage of the colab-print library.

This script demonstrates various features of the Printer class for displaying
styled text, lists, dictionaries, tables, and pandas DataFrames in environments
that support IPython display (like Jupyter notebooks or Google Colab).
"""

import pandas as pd
from colab_print import Printer

def main():
    """Main function to run the examples."""
    
    print("--- Initializing Printer ---")
    printer = Printer()
    print(f"Available default styles: {printer.get_available_styles()}")

    # --- Text Display --- 
    print("\n--- Text Display Examples ---")
    printer.display("This is default text.")
    printer.display("This is highlighted text.", style="highlight")
    printer.display("This is info text.", style="info")
    printer.display("This is success text.", style="success")
    printer.display("This is warning text.", style="warning")
    printer.display("This is error text.", style="error")
    printer.display("This is muted text.", style="muted")
    printer.display("Inline style example.", style="info", font_weight="bold", text_decoration="underline")

    # --- List Display --- 
    print("\n--- List Display Examples ---")
    simple_list = ['Apple', 'Banana', 'Cherry']
    nested_list = ['Fruit', ['Apple', 'Banana'], 'Vegetable', ['Carrot', 'Broccoli']]
    printer.display_list(simple_list, style="success", item_style="padding-left: 15px;")
    printer.display_list(nested_list, ordered=True, style="default")
    printer.display_list(('Tuple', 'Item 1', 'Item 2'), style="warning") # Also works with tuples

    # --- Dictionary Display --- 
    print("\n--- Dictionary Display Examples ---")
    simple_dict = {'Name': 'Bob', 'Role': 'Developer', 'Experience (Years)': 5}
    nested_dict = {
        'Project': 'Colab Print',
        'Version': '0.1.0',
        'Author': {'Name': 'Alaa', 'Contact': 'test@example.com'},
        'Features': ['Text', 'List', 'Dict', 'Table', 'DataFrame']
    }
    printer.display_dict(simple_dict, style="info")
    printer.display_dict(nested_dict, style="default", key_style="color: blue;", value_style="color: green;")

    # --- Table Display --- 
    print("\n--- Table Display Examples ---")
    headers = ["ID", "Product", "Price", "In Stock"]
    rows = [
        [101, "Laptop", 1200.50, True],
        [102, "Keyboard", 75.00, False],
        [103, "Mouse", 25.99, True]
    ]
    printer.display_table(headers, rows, style="default", caption="Inventory")
    printer.display_table(headers, rows, style="highlight", width="80%")

    # --- DataFrame Display --- 
    print("\n--- DataFrame Display Examples ---")
    data = {
        'StudentID': ['S101', 'S102', 'S103', 'S104', 'S105'],
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'Score': [85.5, 92.0, 78.8, 88.1, 95.2],
        'Major': ['CompSci', 'Physics', 'Math', 'CompSci', 'Physics']
    }
    df = pd.DataFrame(data)

    printer.display_df(df, caption="Student Scores")
    printer.display_df(df, style="info", max_rows=3, precision=1, caption="Limited Rows & Precision")
    printer.display_df(df, style="success", 
                      index=False, 
                      highlight_cols=['Name', 'Score'],
                      highlight_rows={1: "background-color: #DFF0D8;"}, # Bob
                      highlight_cells={(4, 'Score'): "background-color: yellow; font-weight: bold;"}, # Eve's score
                      caption="Styled DataFrame without Index")

    # --- Custom Styles & Themes --- 
    print("\n--- Custom Style & Theme Examples ---")
    
    # Add a single custom style
    printer.add_style("custom_blue", "color: navy; border: 1px solid blue; padding: 5px;")
    printer.display("This uses a custom added style.", style="custom_blue")
    print(f"Updated styles: {printer.get_available_styles()}")

    # Initialize a new Printer with additional themes
    custom_themes = {
        'dark_mode': 'color: #E0E0E0; background-color: #282C34; font-family: Consolas, monospace;',
        'report': 'font-family: "Times New Roman", serif; font-size: 14px; color: #333;'
    }
    themed_printer = Printer(additional_styles=custom_themes)
    themed_printer.display("Dark mode style text.", style="dark_mode")
    themed_printer.display_dict({'report_section': 'Results'}, style="report")

    print("\n--- End of Examples ---")

if __name__ == "__main__":
    main() 
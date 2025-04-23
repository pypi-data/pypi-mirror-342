"""
Colab Print - Enhanced display utilities for Jupyter/Colab notebooks.

This module provides a rich set of display utilities for creating beautiful, 
customizable HTML outputs in Jupyter and Google Colab notebooks. It includes
utilities for displaying styled text, tables, and pandas DataFrames with 
extensive styling options.

Features:
- Customizable text display with predefined styles
- Beautiful table formatting with row/column highlighting
- Rich DataFrame display with extensive styling options
- Configurable themes and styling

Usage:
    from colab_print import Printer
    
    printer = Printer()
    printer.display("Hello World", style="highlight")
    
    # Display a DataFrame
    printer.display_df(df, style="default", max_rows=20)
"""

from IPython.display import display as ip_display, HTML
import pandas as pd
from dataclasses import dataclass
from typing import Optional, Union, Dict, List, Any, Tuple
import abc
import warnings

__version__ = "0.1.0"
__author__ = "alaamer12"
__email__ = "ahmedmuhmmed239@gmail.com"
__license__ = "MIT"
__keywords__ = ["jupyter", "colab", "display", "dataframe", "styling", "html"]
__all__ = ["Printer"]

# Define the theme types
DEFAULT_THEMES = {
    'default': 'color: #2C3E50; font-size: 16px; font-family: Arial, sans-serif; letter-spacing: 0.2px;',
    'highlight': 'color: #E74C3C; font-size: 18px; font-weight: 600; font-family: Arial, sans-serif; text-shadow: 1px 1px 2px rgba(231, 76, 60, 0.2); letter-spacing: 0.5px;',
    'info': 'color: #3498DB; font-size: 16px; font-style: italic; font-family: Arial, sans-serif; border-bottom: 1px dotted #3498DB; letter-spacing: 0.2px;',
    'success': 'color: #27AE60; font-size: 16px; font-weight: 600; font-family: Arial, sans-serif; text-shadow: 1px 1px 2px rgba(39, 174, 96, 0.2); letter-spacing: 0.2px;',
    'warning': 'color: #F39C12; font-size: 16px; font-weight: 600; font-family: Arial, sans-serif; text-shadow: 1px 1px 2px rgba(243, 156, 18, 0.2); letter-spacing: 0.2px;',
    'error': 'color: #C0392B; font-size: 16px; font-weight: 600; font-family: Arial, sans-serif; text-shadow: 1px 1px 2px rgba(192, 57, 43, 0.2); letter-spacing: 0.2px;',
    'muted': 'color: #95A5A6; font-size: 14px; font-family: Arial, sans-serif; font-style: italic; letter-spacing: 0.1px;',
}

@dataclass
class DFDisplayParams:
    """Parameters for DataFrame display styling."""
    style: str = 'default'
    max_rows: Optional[int] = None
    max_cols: Optional[int] = None
    precision: int = 2
    header_style: Optional[str] = None
    odd_row_style: Optional[str] = None
    even_row_style: Optional[str] = None
    index: bool = True
    width: str = '100%'
    caption: Optional[str] = None
    highlight_cols: Optional[Union[List, Dict]] = None
    highlight_rows: Optional[Union[List, Dict]] = None
    highlight_cells: Optional[Dict] = None

@dataclass
class TableDisplayParams:
    """Parameters for table display styling."""
    style: str = 'default'
    width: str = '100%'
    header_style: Optional[str] = None
    row_style: Optional[str] = None
    caption: Optional[str] = None

class Displayer(abc.ABC):
    """
    Abstract base class for display components.
    
    All display components should extend this class and implement
    the display method according to their specific requirements.
    """
    
    def __init__(self, styles: Dict[str, str]):
        """
        Initialize a displayer with styles.
        
        Args:
            styles: Dictionary of named styles
        """
        self.styles = styles
    
    def _process_inline_styles(self, inline_styles: Dict[str, str]) -> str:
        """
        Convert Python-style keys to CSS style format and join them.
        
        Args:
            inline_styles: Dictionary of style attributes
            
        Returns:
            Formatted CSS string
        """
        corrected_styles = {k.replace('_', '-') if '_' in k else k: v for k, v in inline_styles.items()}
        return "; ".join([f"{key}: {value}" for key, value in corrected_styles.items()])
    
    @abc.abstractmethod
    def display(self, *args, **kwargs):
        """Display content with the specified styling."""
        pass

class TextDisplayer(Displayer):
    """Displays styled text content."""
    
    def display(self, text: str, *, style: str = 'default', **inline_styles) -> None:
        """
        Display styled text.
        
        Args:
            text: The text to display
            style: Named style from the available styles
            **inline_styles: Additional CSS styles to apply
        """
        base_style = self.styles.get(style, self.styles['default'])
        inline_style_string = self._process_inline_styles(inline_styles)
        final_style = f"{base_style} {inline_style_string}" if inline_style_string else base_style
        formatted_text = f'<span style="{final_style}">{text}</span>'
        
        self._display_html(formatted_text)
    
    def _display_html(self, html_content: str) -> None:
        """
        Display HTML content safely.
        
        Args:
            html_content: HTML content to display
        """
        try:
            ip_display(HTML(html_content))
        except NameError:
            warnings.warn("IPython environment not detected. HTML output will not be rendered properly.")
            print(f"HTML Content (not rendered): {html_content}")

class TableDisplayer(Displayer):
    """Displays HTML tables with customizable styling."""
    
    def _get_table_styles(self, style: str = 'default', width: str = '100%') -> tuple:
        """
        Generate the CSS styles for the table, headers, and cells.
        
        Args:
            style: Named style from the available styles
            width: Width of the table (CSS value)
            
        Returns:
            Tuple of (table_style, th_style, td_style)
        """
        base_style = self.styles.get(style, self.styles['default'])
        
        # Ensure width is explicitly included to take full notebook width
        table_style = f"{base_style} border-collapse: collapse; width: {width} !important;"
        th_style = "background-color: #f2f2f2; padding: 8px; border: 1px solid #ddd; text-align: left;"
        td_style = "padding: 8px; border: 1px solid #ddd;"
        
        return table_style, th_style, td_style
    
    def _generate_table_caption(self, caption: Optional[str], style_base: str) -> List[str]:
        """
        Generate HTML for the table caption if provided.
        
        Args:
            caption: Caption text
            style_base: Base CSS style string
            
        Returns:
            List of HTML caption elements or empty list
        """
        if not caption:
            return []
            
        caption_style = f"caption-side: top; text-align: left; font-weight: bold; margin-bottom: 10px; {style_base}"
        return [f'<caption style="{caption_style}">{caption}</caption>']
    
    def _generate_table_header(self, headers: List[str], th_style: str) -> List[str]:
        """
        Generate HTML for the table header row.
        
        Args:
            headers: List of header texts
            th_style: CSS style for header cells
            
        Returns:
            List of HTML elements for the header row
        """
        html = ['<tr>']
        for header in headers:
            html.append(f'<th style="{th_style}">{header}</th>')
        html.append('</tr>')
        return html
    
    def _generate_table_rows(self, rows: List[List[Any]], td_style: str) -> List[str]:
        """
        Generate HTML for the table data rows.
        
        Args:
            rows: List of rows, each row being a list of cell values
            td_style: CSS style for data cells
            
        Returns:
            List of HTML elements for data rows
        """
        html = []
        for row in rows:
            html.append('<tr>')
            for cell in row:
                html.append(f'<td style="{td_style}">{cell}</td>')
            html.append('</tr>')
        return html
    
    def _process_styles(self, style: str, width: str, custom_header_style: Optional[str], 
                        custom_row_style: Optional[str], inline_styles_dict: Dict[str, str]) -> Tuple[str, str, str, str]:
        """
        Process and prepare all styles for the table.
        
        Args:
            style: Named style from the available styles
            width: Width of the table (CSS value)
            custom_header_style: Optional custom CSS for header cells
            custom_row_style: Optional custom CSS for data cells
            inline_styles_dict: Dictionary of additional CSS styles
            
        Returns:
            Tuple of (table_style, th_style, td_style, inline_style_string)
        """
        # Process inline styles
        inline_style_string = self._process_inline_styles(inline_styles_dict)
        
        # Get base styles for table components
        table_style, th_style, td_style = self._get_table_styles(style, width)
        
        # Apply custom styles if provided
        if custom_header_style:
            th_style = custom_header_style
        if custom_row_style:
            td_style = custom_row_style
        
        # Add inline styles to the table style
        if inline_style_string:
            table_style = f"{table_style} {inline_style_string}"
            
        return table_style, th_style, td_style, inline_style_string
    
    def _build_table_html(self, headers: List[str], rows: List[List[Any]], 
                         table_style: str, th_style: str, td_style: str, 
                         caption: Optional[str], inline_style_string: str) -> List[str]:
        """
        Build the HTML components for the table.
        
        Args:
            headers: List of column headers
            rows: List of rows, each row being a list of cell values
            table_style: CSS style for the table
            th_style: CSS style for header cells
            td_style: CSS style for data cells
            caption: Optional table caption
            inline_style_string: Additional CSS styles
            
        Returns:
            List of HTML elements for the complete table
        """
        html = [f'<table style="{table_style}">']
        
        # Add caption if provided
        html.extend(self._generate_table_caption(caption, inline_style_string))
        
        # Add header row
        html.extend(self._generate_table_header(headers, th_style))
        
        # Add data rows
        html.extend(self._generate_table_rows(rows, td_style))
        
        # Close the table
        html.append('</table>')
        
        return html
    
    def _display_html(self, html: List[str], headers: List[str], rows: List[List[Any]]) -> None:
        """
        Display the HTML table or fallback to text representation.
        
        Args:
            html: List of HTML elements for the table
            headers: List of column headers (for fallback display)
            rows: List of rows (for fallback display)
        """
        try:
            ip_display(HTML(''.join(html)))
        except NameError:
            warnings.warn("IPython environment not detected. Table will not be rendered properly.")
            print(f"HTML Table (not rendered): {len(rows)} rows x {len(headers)} columns")
    
    def display(self, headers: List[str], rows: List[List[Any]], *, 
                style: str = 'default', width: str = '100%', 
                caption: Optional[str] = None, 
                custom_header_style: Optional[str] = None,
                custom_row_style: Optional[str] = None,
                **inline_styles) -> None:
        """
        Display a table with the given headers and rows.
        
        Args:
            headers: List of column headers
            rows: List of rows, each row being a list of cell values
            style: Named style from the available styles
            width: Width of the table (CSS value)
            caption: Optional table caption
            custom_header_style: Optional custom CSS for header cells
            custom_row_style: Optional custom CSS for data cells
            **inline_styles: Additional CSS styles to apply to the table
        """
        # Process inline styles (but don't let them override the width)
        inline_styles_dict = dict(inline_styles)
        if 'width' in inline_styles_dict:
            del inline_styles_dict['width']  # Ensure our width parameter takes precedence
        
        # Process all styles
        table_style, th_style, td_style, inline_style_string = self._process_styles(
            style, width, custom_header_style, custom_row_style, inline_styles_dict
        )
        
        # Build HTML components
        html = self._build_table_html(
            headers, rows, table_style, th_style, td_style, caption, inline_style_string
        )
        
        # Display the final HTML
        self._display_html(html, headers, rows)

class DFDisplayer(Displayer):
    """Displays pandas DataFrames with extensive styling options."""
    
    def __init__(self, styles: Dict[str, str], df: pd.DataFrame):
        """
        Initialize a DataFrame displayer.
        
        Args:
            styles: Dictionary of named styles
            df: The DataFrame to display
        """
        super().__init__(styles)
        self.df = df
    
    def _extract_base_color(self, base_style: str) -> str:
        """
        Extract the text color from a base style string.
        
        Args:
            base_style: CSS style string
            
        Returns:
            CSS color property or empty string
        """
        base_color = ""
        for part in base_style.split(';'):
            if 'color:' in part and not 'background-color:' in part:
                base_color = part.strip()
                break
        return base_color
    
    def _prepare_table_styles(self, style: str, width: str, inline_style_string: str, 
                             base_color: str, header_style: Optional[str], 
                             odd_row_style: Optional[str], even_row_style: Optional[str]) -> tuple:
        """
        Prepare all the styles needed for the table.
        
        Args:
            style: Named style from the available styles
            width: Table width (CSS value)
            inline_style_string: Processed inline CSS styles
            base_color: Extracted text color
            header_style: Custom CSS for header cells
            odd_row_style: Custom CSS for odd rows
            even_row_style: Custom CSS for even rows
            
        Returns:
            Tuple of (table_style, th_style, odd_td_style, even_td_style)
        """
        # Base styles
        base_style = self.styles.get(style, self.styles['default'])
        
        # Table element styles - ensure width is important to override any other styles
        table_only_styles = f"border-collapse: collapse; width: {width} !important;"
        table_style = f"{base_style} {table_only_styles}"
        
        # Cell styles base
        cell_style_base = inline_style_string if inline_style_string else ""
        
        # Default styles with inline styles
        default_header = f"background-color: #f2f2f2; padding: 8px; border: 1px solid #ddd; text-align: left; font-weight: bold; {base_color}; {cell_style_base}"
        default_odd_row = f"background-color: #ffffff; padding: 8px; border: 1px solid #ddd; {base_color}; {cell_style_base}"
        default_even_row = f"background-color: #f9f9f9; padding: 8px; border: 1px solid #ddd; {base_color}; {cell_style_base}"
        
        # Apply custom styles if provided
        th_style = f"{header_style} {cell_style_base}" if header_style else default_header
        odd_td_style = f"{odd_row_style} {cell_style_base}" if odd_row_style else default_odd_row
        even_td_style = f"{even_row_style} {cell_style_base}" if even_row_style else default_even_row
        
        return table_style, th_style, odd_td_style, even_td_style
    
    def _prepare_dataframe(self, df: pd.DataFrame, max_rows: Optional[int], 
                          max_cols: Optional[int], precision: int) -> pd.DataFrame:
        """
        Prepare the DataFrame for display with limits and formatting.
        
        Args:
            df: DataFrame to prepare
            max_rows: Maximum number of rows to display
            max_cols: Maximum number of columns to display
            precision: Decimal precision for float values
            
        Returns:
            Prepared DataFrame copy
        """
        df_copy = df.copy()
        
        # Handle row limits
        if max_rows is not None and len(df_copy) > max_rows:
            half_rows = max_rows // 2
            df_copy = pd.concat([df_copy.head(half_rows), df_copy.tail(half_rows)])
        
        # Handle column limits
        if max_cols is not None and len(df_copy.columns) > max_cols:
            half_cols = max_cols // 2
            first_cols = df_copy.columns[:half_cols].tolist()
            last_cols = df_copy.columns[-half_cols:].tolist()
            df_copy = df_copy[first_cols + last_cols]
        
        # Format numbers
        for col in df_copy.select_dtypes(include=['float']).columns:
            df_copy[col] = df_copy[col].apply(lambda x: f"{x:.{precision}f}" if pd.notnull(x) else "")
            
        return df_copy
    
    def _generate_table_caption(self, caption: Optional[str], cell_style_base: str) -> List[str]:
        """
        Generate HTML for the table caption if provided.
        
        Args:
            caption: Caption text
            cell_style_base: Base CSS style string
            
        Returns:
            List of HTML caption elements or empty list
        """
        if not caption:
            return []
            
        caption_style = f"caption-side: top; text-align: left; font-weight: bold; margin-bottom: 10px; {cell_style_base}"
        return [f'<caption style="{caption_style}">{caption}</caption>']
    
    def _generate_header_row(self, df_copy: pd.DataFrame, th_style: str, 
                            highlight_cols: Optional[Union[List, Dict]], 
                            index: bool) -> List[str]:
        """
        Generate HTML for the table header row.
        
        Args:
            df_copy: Prepared DataFrame
            th_style: CSS style for header cells
            highlight_cols: Columns to highlight
            index: Whether to show DataFrame index
            
        Returns:
            List of HTML elements for the header row
        """
        html = ['<tr>']
        
        # Add index header if showing index
        if index:
            html.append(f'<th style="{th_style}"></th>')
        
        # Add column headers
        for col in df_copy.columns:
            col_style = th_style
            
            # Apply highlighting to columns if specified
            if highlight_cols:
                if isinstance(highlight_cols, dict) and col in highlight_cols:
                    col_style = f"{th_style} {highlight_cols[col]}"
                elif isinstance(highlight_cols, list) and col in highlight_cols:
                    col_style = f"{th_style} background-color: #FFEB3B !important;"
                    
            html.append(f'<th style="{col_style}">{col}</th>')
            
        html.append('</tr>')
        return html
    
    def _generate_data_rows(self, df_copy: pd.DataFrame, even_td_style: str, 
                           odd_td_style: str, highlight_rows: Optional[Union[List, Dict]], 
                           highlight_cells: Optional[Dict], index: bool) -> List[str]:
        """
        Generate HTML for the table data rows.
        
        Args:
            df_copy: Prepared DataFrame
            even_td_style: CSS style for even rows
            odd_td_style: CSS style for odd rows
            highlight_rows: Rows to highlight
            highlight_cells: Cells to highlight
            index: Whether to show DataFrame index
            
        Returns:
            List of HTML elements for data rows
        """
        html = []
        
        for i, (idx, row) in enumerate(df_copy.iterrows()):
            row_style = even_td_style if i % 2 == 0 else odd_td_style
            
            # Apply row highlighting if specified
            if highlight_rows:
                if isinstance(highlight_rows, dict) and idx in highlight_rows:
                    row_style = f"{row_style} {highlight_rows[idx]}"
                elif isinstance(highlight_rows, list) and idx in highlight_rows:
                    row_style = f"{row_style} background-color: #FFEB3B !important;"
            
            html.append('<tr>')
            
            # Add index cell if showing index
            if index:
                html.append(f'<td style="{row_style} font-weight: bold;">{idx}</td>')
            
            # Add data cells
            for col in df_copy.columns:
                cell_style = row_style
                cell_value = row[col]
                
                # Apply cell highlighting if specified
                if highlight_cells:
                    # Try different ways to match the cell coordinates
                    if (idx, col) in highlight_cells:
                        cell_style = f"{cell_style} {highlight_cells[(idx, col)]}"
                    elif (i, col) in highlight_cells:
                        cell_style = f"{cell_style} {highlight_cells[(i, col)]}"
                    elif (str(i), col) in highlight_cells:
                        cell_style = f"{cell_style} {highlight_cells[(str(i), col)]}"
                
                html.append(f'<td style="{cell_style}">{cell_value}</td>')
            
            html.append('</tr>')
            
        return html
    
    def display(self, *,
                style: str = 'default',
                max_rows: Optional[int] = None,
                max_cols: Optional[int] = None,
                precision: int = 2,
                header_style: Optional[str] = None,
                odd_row_style: Optional[str] = None,
                even_row_style: Optional[str] = None,
                index: bool = True,
                width: str = '100%',
                caption: Optional[str] = None,
                highlight_cols: Optional[Union[List, Dict]] = None,
                highlight_rows: Optional[Union[List, Dict]] = None,
                highlight_cells: Optional[Dict] = None,
                **inline_styles) -> None:
        """
        Display a pandas DataFrame with customizable styling.

        Args:
            style: Named style from the available styles
            max_rows: Maximum number of rows to display
            max_cols: Maximum number of columns to display
            precision: Decimal precision for float values
            header_style: Custom CSS for header cells
            odd_row_style: Custom CSS for odd rows
            even_row_style: Custom CSS for even rows
            index: Whether to show DataFrame index
            width: Table width (CSS value)
            caption: Table caption
            highlight_cols: Columns to highlight (list) or {col: style} mapping
            highlight_rows: Rows to highlight (list) or {row: style} mapping
            highlight_cells: Cell coordinates to highlight {(row, col): style}
            **inline_styles: Additional CSS styles for all cells
        """
        # Process styles (but don't let them override the width)
        inline_styles_dict = dict(inline_styles)
        if 'width' in inline_styles_dict:
            del inline_styles_dict['width']  # Ensure our width parameter takes precedence
        
        inline_style_string = self._process_inline_styles(inline_styles_dict)
        base_style = self.styles.get(style, self.styles['default'])
        base_color = self._extract_base_color(base_style)
        
        # Prepare all styles
        table_style, th_style, odd_td_style, even_td_style = self._prepare_table_styles(
            style, width, inline_style_string, base_color, 
            header_style, odd_row_style, even_row_style
        )
        
        # Prepare the DataFrame
        df_copy = self._prepare_dataframe(self.df, max_rows, max_cols, precision)
        
        # Build HTML components
        html = [f'<table style="{table_style}">']
        
        # Add caption if provided
        html.extend(self._generate_table_caption(caption, inline_style_string))
        
        # Add header row
        html.extend(self._generate_header_row(df_copy, th_style, highlight_cols, index))
        
        # Add data rows
        html.extend(self._generate_data_rows(df_copy, even_td_style, odd_td_style, 
                                           highlight_rows, highlight_cells, index))
        
        html.append('</table>')
        
        # Display the final HTML
        try:
            ip_display(HTML(''.join(html)))
        except NameError:
            warnings.warn("IPython environment not detected. DataFrame will not be rendered properly.")
            print(f"DataFrame (not rendered): {df_copy.shape[0]} rows × {df_copy.shape[1]} columns")
            print(df_copy.head().to_string())

class ListDisplayer(Displayer):
    """Displays Python lists or tuples as HTML lists."""
    
    def _generate_list_html(self, items: Union[List, Tuple], ordered: bool, style: str, 
                           item_style: Optional[str], **inline_styles) -> str:
        """
        Recursively generate HTML for a list or tuple.
        
        Args:
            items: The list or tuple to display
            ordered: True for ordered list (<ol>), False for unordered (<ul>)
            style: Base style name for the list container
            item_style: Optional custom CSS for list items
            **inline_styles: Additional inline styles for list items
            
        Returns:
            HTML string for the list
        """
        tag = 'ol' if ordered else 'ul'
        html = [f'<{tag} style="{self.styles.get(style, self.styles['default'])}">']
        
        list_item_inline_style = self._process_inline_styles(inline_styles)
        final_item_style = item_style if item_style else ""
        if list_item_inline_style:
            final_item_style = f"{final_item_style}; {list_item_inline_style}".strip('; ')

        for item in items:
            item_content = ""
            if isinstance(item, (list, tuple)):
                # Recursively handle nested lists/tuples
                item_content = self._generate_list_html(item, ordered, style, item_style, **inline_styles)
            elif isinstance(item, dict):
                 # Delegate nested dicts to DictDisplayer (if available)
                 # Note: Requires access to a DictDisplayer instance or direct generation
                 # For simplicity here, we'll just convert to string
                 item_content = str(item) # Placeholder - ideally use DictDisplayer
            else:
                item_content = str(item)
                
            html.append(f'<li style="{final_item_style}">{item_content}</li>')
            
        html.append(f'</{tag}>')
        return ''.join(html)

    def display(self, items: Union[List, Tuple], *, 
                ordered: bool = False, style: str = 'default', 
                item_style: Optional[str] = None, 
                **inline_styles) -> None:
        """
        Display a list or tuple as an HTML list.
        
        Args:
            items: The list or tuple to display
            ordered: If True, use an ordered list (<ol>), otherwise unordered (<ul>)
            style: Named style for the list container
            item_style: Optional custom CSS style for list items
            **inline_styles: Additional CSS styles to apply to list items
        """
        if not isinstance(items, (list, tuple)):
            raise TypeError("Input must be a list or tuple")

        html_content = self._generate_list_html(items, ordered, style, item_style, **inline_styles)
        self._display_html(html_content, items)
        
    def _display_html(self, html_content: str, items: Union[List, Tuple]) -> None:
        """
        Display HTML content safely, with fallback.
        
        Args:
            html_content: HTML content to display
            items: Original list/tuple (for fallback)
        """
        try:
            ip_display(HTML(html_content))
        except NameError:
            warnings.warn("IPython environment not detected. List will not be rendered properly.")
            print(f"List (not rendered): {len(items)} items")
            for item in items:
                print(f"- {item}")

class DictDisplayer(Displayer):
    """Displays Python dictionaries as HTML definition lists or tables."""
    
    def _generate_dict_html_dl(self, data: Dict, style: str, 
                              key_style: Optional[str], value_style: Optional[str], 
                              **inline_styles) -> str:
        """
        Recursively generate HTML definition list for a dictionary.
        
        Args:
            data: The dictionary to display
            style: Base style name for the list container
            key_style: Optional custom CSS for keys (<dt>)
            value_style: Optional custom CSS for values (<dd>)
            **inline_styles: Additional inline styles for list items
        
        Returns:
            HTML string for the definition list
        """
        dl_style = self.styles.get(style, self.styles['default'])
        html = [f'<dl style="{dl_style}">']
        
        inline_style_string = self._process_inline_styles(inline_styles)
        final_key_style = key_style if key_style else "font-weight: bold;"
        final_value_style = value_style if value_style else "margin-left: 20px;"
        
        if inline_style_string:
            final_key_style = f"{final_key_style}; {inline_style_string}".strip('; ')
            final_value_style = f"{final_value_style}; {inline_style_string}".strip('; ')

        for key, value in data.items():
            key_content = str(key)
            value_content = ""
            
            if isinstance(value, dict):
                # Recursively handle nested dictionaries
                value_content = self._generate_dict_html_dl(value, style, key_style, value_style, **inline_styles)
            elif isinstance(value, (list, tuple)):
                # Delegate nested lists to ListDisplayer (if available)
                # For simplicity here, we'll just convert to string
                 value_content = str(value) # Placeholder - ideally use ListDisplayer
            else:
                value_content = str(value)
                
            html.append(f'<dt style="{final_key_style}">{key_content}</dt>')
            html.append(f'<dd style="{final_value_style}">{value_content}</dd>')
            
        html.append('</dl>')
        return ''.join(html)

    def display(self, data: Dict, *, style: str = 'default', 
                key_style: Optional[str] = None, 
                value_style: Optional[str] = None, 
                **inline_styles) -> None:
        """
        Display a dictionary as an HTML definition list.
        
        Args:
            data: The dictionary to display
            style: Named style for the definition list container
            key_style: Optional custom CSS style for keys (<dt>)
            value_style: Optional custom CSS style for values (<dd>)
            **inline_styles: Additional CSS styles to apply to list items
        """
        if not isinstance(data, dict):
            raise TypeError("Input must be a dictionary")

        html_content = self._generate_dict_html_dl(data, style, key_style, value_style, **inline_styles)
        self._display_html(html_content, data)

    def _display_html(self, html_content: str, data: Dict) -> None:
        """
        Display HTML content safely, with fallback.
        
        Args:
            html_content: HTML content to display
            data: Original dictionary (for fallback)
        """
        try:
            ip_display(HTML(html_content))
        except NameError:
            warnings.warn("IPython environment not detected. Dictionary will not be rendered properly.")
            print(f"Dictionary (not rendered): {len(data)} items")
            for key, value in data.items():
                print(f"- {key}: {value}")

class Printer:
    """
    Main class for displaying text, tables, and DataFrames with stylized HTML.
    
    This class provides a unified interface for all display operations,
    delegating to specialized displayers for each type of content.
    """
    
    def __init__(self, additional_styles: Optional[Dict[str, str]] = None):
        """
        Initialize the printer with default and optional additional styles.
        
        Args:
            additional_styles: Optional dictionary of additional styles to add
        """
        # Set up styles with defaults and any additional styles
        self.styles = DEFAULT_THEMES.copy()
        if additional_styles:
            self.styles.update(additional_styles)
            
        # Create displayers for different content types
        self.text_displayer = TextDisplayer(self.styles)
        self.table_displayer = TableDisplayer(self.styles)
        self.list_displayer = ListDisplayer(self.styles)
        self.dict_displayer = DictDisplayer(self.styles)
    
    def display(self, text: str, *, style: str = 'default', **inline_styles) -> None:
        """
        Display text with the specified styling.
        
        Args:
            text: Text to display
            style: Named style from available styles
            **inline_styles: Additional CSS styles to apply
        """
        self.text_displayer.display(text, style=style, **inline_styles)
    
    def display_table(self, headers: List[str], rows: List[List[Any]], *, 
                     style: str = 'default', **table_options) -> None:
        """
        Display a table with the given headers and rows.
        
        Args:
            headers: List of column headers
            rows: List of rows, each row being a list of cell values
            style: Named style from available styles
            **table_options: Additional table styling options
        """
        self.table_displayer.display(headers, rows, style=style, **table_options)
    
    def display_df(self, df: pd.DataFrame, *,
                  style: str = 'default',
                  max_rows: Optional[int] = None,
                  max_cols: Optional[int] = None,
                  precision: int = 2,
                  header_style: Optional[str] = None,
                  odd_row_style: Optional[str] = None,
                  even_row_style: Optional[str] = None,
                  index: bool = True,
                  width: str = '100%',
                  caption: Optional[str] = None,
                  highlight_cols: Optional[Union[List, Dict]] = None,
                  highlight_rows: Optional[Union[List, Dict]] = None,
                  highlight_cells: Optional[Dict] = None,
                  **inline_styles) -> None:
        """
        Display a pandas DataFrame with customizable styling.
        
        Args:
            df: DataFrame to display
            style: Named style from available styles
            max_rows: Maximum number of rows to display
            max_cols: Maximum number of columns to display
            precision: Decimal precision for float values
            header_style: Custom CSS for header cells
            odd_row_style: Custom CSS for odd rows
            even_row_style: Custom CSS for even rows
            index: Whether to show DataFrame index
            width: Table width (CSS value)
            caption: Table caption
            highlight_cols: Columns to highlight (list) or {col: style} mapping
            highlight_rows: Rows to highlight (list) or {row: style} mapping
            highlight_cells: Cell coordinates to highlight {(row, col): style}
            **inline_styles: Additional CSS styles for all cells
        """
        # Check if pandas is available
        if 'pandas.core.frame.DataFrame' not in str(type(df)):
            raise TypeError("The 'df' parameter must be a pandas DataFrame")
            
        # Create the displayer and use it
        displayer = DFDisplayer(self.styles, df)
        displayer.display(
            style=style,
            max_rows=max_rows,
            max_cols=max_cols,
            precision=precision,
            header_style=header_style,
            odd_row_style=odd_row_style,
            even_row_style=even_row_style,
            index=index,
            width=width,
            caption=caption,
            highlight_cols=highlight_cols,
            highlight_rows=highlight_rows,
            highlight_cells=highlight_cells,
            **inline_styles
        )
    
    def display_list(self, items: Union[List, Tuple], *, 
                     ordered: bool = False, style: str = 'default', 
                     item_style: Optional[str] = None, 
                     **inline_styles) -> None:
        """
        Display a list or tuple as an HTML list.

        Args:
            items: The list or tuple to display
            ordered: If True, use an ordered list (<ol>), otherwise unordered (<ul>)
            style: Named style for the list container
            item_style: Optional custom CSS style for list items
            **inline_styles: Additional CSS styles to apply to list items
        """
        self.list_displayer.display(items, ordered=ordered, style=style, 
                                    item_style=item_style, **inline_styles)

    def display_dict(self, data: Dict, *, style: str = 'default', 
                     key_style: Optional[str] = None, 
                     value_style: Optional[str] = None, 
                     **inline_styles) -> None:
        """
        Display a dictionary as an HTML definition list.

        Args:
            data: The dictionary to display
            style: Named style for the definition list container
            key_style: Optional custom CSS style for keys (<dt>)
            value_style: Optional custom CSS style for values (<dd>)
            **inline_styles: Additional CSS styles to apply to list items
        """
        self.dict_displayer.display(data, style=style, key_style=key_style, 
                                     value_style=value_style, **inline_styles)
    
    def add_style(self, name: str, style_definition: str) -> None:
        """
        Add a new style to the available styles.
        
        Args:
            name: Name of the style
            style_definition: CSS style string
        """
        self.styles[name] = style_definition
    
    def get_available_styles(self) -> List[str]:
        """
        Get a list of available style names.
        
        Returns:
            List of style names
        """
        return list(self.styles.keys())

# Add a function to check if we're in an IPython environment
def is_in_notebook() -> bool:
    """
    Check if code is running inside an IPython/Jupyter notebook.
    
    Returns:
        True if in a notebook, False otherwise
    """
    try:
        from IPython import get_ipython
        if get_ipython() is None:
            return False
        if 'IPKernelApp' not in get_ipython().config:
            return False
        return True
    except ImportError:
        return False
                
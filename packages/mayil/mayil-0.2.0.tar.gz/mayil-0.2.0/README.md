# Mayil

A Streamlit-like package for creating structured and formatted emails in Python.

## Installation

```bash
pip install mayil
```

## Usage

```python
import mayil as my

# Add components to your email
my.header("Welcome to Our Newsletter")
my.text("This is a sample text paragraph.")
my.text("This is another paragraph.")

# Get the complete HTML body
html_content = my.body()
```

## Components

### Header
```python
my.header("Your Header Text")
```

### Text
```python
my.text("Your paragraph text")
```

### Formatted Table (ftable)
```python
import pandas as pd

# Create a sample dataframe
df = pd.DataFrame({
    'Score': [85, 92, 78],
    'Status': ['Active', 'Inactive', 'Active'],
    'Date': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03'])
})

# Define conditions for formatting
conditions = {
    'Score': [
        (lambda x: x < 90, '#ff0000'),  # Red if < 90
        (lambda x: x >= 90, '#00ff00')  # Green if >= 90
    ],
    'Status': [
        (lambda x: x == 'Active', '#00ff00'),  # Green if active
        (lambda x: x == 'Inactive', '#ff0000')  # Red if inactive
    ],
    'Date': [
        (lambda x: x < pd.Timestamp('2024-01-02'), '#ff0000'),  # Red if before Jan 2
        (lambda x: x >= pd.Timestamp('2024-01-02'), '#00ff00')  # Green if Jan 2 or later
    ]
}

# Apply formatting
my.ftable(df, conditions=conditions)  # Apply to both cell and text
my.ftable(df, cell_colors=conditions)  # Apply only to cell background
my.ftable(df, text_colors=conditions)  # Apply only to text
```

## Features

- Streamlit-like interface for building emails
- HTML-based output
- Styled components
- Chainable methods
- Conditional formatting for tables
- Support for various data types (numbers, strings, dates)
- Flexible color customization

## Advanced Usage

### Creating Multiple Instances
While the default instance is available through `import mayil as my`, you can create additional instances if needed:

```python
from mayil import Mayil

# Create a new instance
custom_instance = Mayil()
custom_instance.header("Custom Header")
```

### Table Formatting Options
The `ftable` method supports three types of conditional formatting:
1. `conditions`: Applies formatting to both cell background and text
2. `cell_colors`: Applies formatting only to cell background
3. `text_colors`: Applies formatting only to text

Each condition is defined as a tuple of (lambda function, color) where:
- The lambda function should return a boolean
- The color can be any valid CSS color (hex, rgb, named colors) 
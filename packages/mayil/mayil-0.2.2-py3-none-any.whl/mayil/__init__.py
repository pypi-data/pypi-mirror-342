from mayil.core.mayil import Mayil

__version__ = "0.1.0"

# Create a default instance
_default_instance = Mayil()

# Expose all methods from the default instance
title = _default_instance.title
header = _default_instance.header
subheader = _default_instance.subheader
text = _default_instance.text
caption = _default_instance.caption
metric = _default_instance.metric
sticky_note = _default_instance.sticky_note
divider = _default_instance.divider
columns = _default_instance.columns
table = _default_instance.table
ftable = _default_instance.ftable
hyperlink = _default_instance.hyperlink
plotly_chart = _default_instance.plotly_chart

# Create a function to get the current body content
def body():
    return _default_instance.body

# Expose the class and instance for advanced usage
Mayil = Mayil
instance = _default_instance

__all__ = [
    "Mayil",
    "instance",
    "title",
    "header",
    "subheader",
    "text",
    "caption",
    "metric",
    "sticky_note",
    "divider",
    "columns",
    "table",
    "ftable",
    "hyperlink",
    "body",
    "plotly_chart"
] 
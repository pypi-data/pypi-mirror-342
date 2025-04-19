# TurtleGridUtil

TurtleGridUtil is a Python utility for drawing customizable coordinate grids using the Turtle graphics library. It provides an easy way to create visual grids for educational purposes, graphing, or any project that requires a coordinate system.

**source code on [github](https://github.com/Vskesha/TurtleGridUtil)**

## Features

- Draw major and minor grid lines
- Customizable line colors and widths
- Adjustable grid spacing
- Scale markers with customizable font and style
- Optional scale point markers

## Installation

Use `pip install turtlegridutil` for installing

## Usage

Here's a basic example of how to use TurtleGridUtil:

```python
import turtle
from turtlegridutil import draw_grid

# Create a turtle screen
screen = turtle.Screen()
screen.title("Grid Drawing")
screen.setup(width=800, height=600)

# Draw the grid
draw_grid(screen, major_line_step=50, minor_line_step=10)

# Keep the window open
turtle.done()
```


## API Reference
`draw_grid(screen, **kwargs)`  

Draws a coordinate grid on the given turtle screen.

Parameters:

`screen` (turtle.Screen): The turtle screen object on which to draw the grid.  
`major_line_step` (int): The distance between major grid lines. Default is 100.  
`minor_line_step` (int): The distance between minor grid lines. If 0, no minor lines are drawn. Default is 0.  
`major_line_color` (str): The color of major grid lines. Default is "black".  
`minor_line_color` (str): The color of minor grid lines. Default is "gray".  
`major_line_width` (int): The width of major grid lines. Default is 1.  
`minor_line_width` (int): The width of minor grid lines. Default is 1.  
`use_scale` (bool): Whether to draw scale markers and labels. Default is True.  
`scale_step` (int): The interval for placing scale markers and labels. If 0, uses major_line_step. Default is 0.  
`font_color` (str): The color of the scale labels. Default is "black".  
`font_family` (str): The font family for scale labels. Default is "Arial".  
`font_size` (int): The font size for scale labels. Default is 14.  
`font_style` (str): The font style for scale labels (e.g., "normal", "bold", "italic"). Default is "normal".  
`scale_points_size` (int): The size of the dots marking scale points. If 0, no dots are drawn. Default is 5.  

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
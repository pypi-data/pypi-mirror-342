import turtle


def draw_grid(
        screen: turtle.Screen,
        major_line_step=100,
        minor_line_step=0,
        major_line_color="black",
        minor_line_color="gray",
        major_line_width=1,
        minor_line_width=1,
        use_scale=True,
        scale_step=0,
        font_color="black",
        font_family="Arial",
        font_size=14,
        font_style="normal",
        scale_points_size=5,
):
    """
    Draw a coordinate grid on a Python turtle screen.

    This function creates a customizable coordinate grid on the provided turtle screen,
    including major and minor lines, scale markers, and labels.

    Parameters:
    screen (turtle.Screen): The turtle screen object on which to draw the grid.
    major_line_step (int): The distance between major grid lines. Default is 100.
    minor_line_step (int): The distance between minor grid lines. If 0, no minor lines are drawn. Default is 0.
    major_line_color (str): The color of major grid lines. Default is "black".
    minor_line_color (str): The color of minor grid lines. Default is "gray".
    major_line_width (int): The width of major grid lines. Default is 1.
    minor_line_width (int): The width of minor grid lines. Default is 1.
    use_scale (bool): Whether to draw scale markers and labels. Default is True.
    scale_step (int): The interval for placing scale markers and labels. If 0, uses major_line_step. Default is 0.
    font_color (str): The color of the scale labels. Default is "black".
    font_family (str): The font family for scale labels. Default is "Arial".
    font_size (int): The font size for scale labels. Default is 14.
    font_style (str): The font style for scale labels (e.g., "normal", "bold", "italic"). Default is "normal".
    scale_points_size (int): The size of the dots marking scale points. If 0, no dots are drawn. Default is 5.

    Returns:
    None

    Note:
    This function modifies the turtle screen directly and does not return any value.
    """

    screen.tracer(0)

    screen_width = screen.window_width()
    screen_height = screen.window_height()
    half_width = screen_width // 2
    half_height = screen_height // 2

    grid_drawer = turtle.Turtle()
    grid_drawer.hideturtle()

    # Draw minor lines
    if minor_line_step:
        grid_drawer.pensize(minor_line_width)
        grid_drawer.pencolor(minor_line_color)

        max_x = half_width // minor_line_step * minor_line_step
        max_y = half_height // minor_line_step * minor_line_step

        for x in range(-max_x, half_width, minor_line_step):
            grid_drawer.penup()
            grid_drawer.goto(x, half_height)
            grid_drawer.pendown()
            grid_drawer.goto(x, -half_height)

        for y in range(-max_y, half_height, minor_line_step):
            grid_drawer.penup()
            grid_drawer.goto(half_width, y)
            grid_drawer.pendown()
            grid_drawer.goto(-half_width, y)

    # Draw major lines
    grid_drawer.pensize(major_line_width)
    grid_drawer.pencolor(major_line_color)

    max_x = half_width // major_line_step * major_line_step
    max_y = half_height // major_line_step * major_line_step

    for x in range(-max_x, half_width, major_line_step):
        grid_drawer.penup()
        grid_drawer.goto(x, half_height)
        grid_drawer.pendown()
        grid_drawer.goto(x, -half_height)

    for y in range(-max_y, half_height, major_line_step):
        grid_drawer.penup()
        grid_drawer.goto(half_width, y)
        grid_drawer.pendown()
        grid_drawer.goto(-half_width, y)

    # Draw scale
    if use_scale:
        scale_step = scale_step or major_line_step
        grid_drawer.color(font_color)

        max_x = half_width // scale_step * scale_step
        max_y = half_height // scale_step * scale_step

        for x in range(-max_x, half_width, scale_step):
            grid_drawer.penup()
            grid_drawer.goto(x, 0)
            grid_drawer.pendown()
            grid_drawer.write(str(x), font=(font_family, font_size, font_style))
            if scale_points_size:
                grid_drawer.dot(scale_points_size)

        for y in range(-max_y, half_height, scale_step):
            grid_drawer.penup()
            grid_drawer.goto(0, y)
            grid_drawer.pendown()
            grid_drawer.write(str(y), font=(font_family, font_size, font_style))
            if scale_points_size:
                grid_drawer.dot(scale_points_size)

    screen.update()
    screen.tracer(1)


if __name__ == "__main__":
    # Create a turtle screen
    screen = turtle.Screen()
    screen.title("Grid Drawing")
    screen.setup(width=800, height=600)

    # Draw the grid
    draw_grid(screen, major_line_step=50, minor_line_step=10)

    # Keep the window open
    turtle.done()

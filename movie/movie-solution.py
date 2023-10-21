#!/usr/bin/env python3

"""
Stanford CS106A Movie Grid Example
Nick Parlante
"""

import sys
import tkinter
import random
import drawcanvas

from grid import Grid

SIDE = 20  # pixels across of one square


def set_edges(grid):
    """
    Set all the squares along the left edge (x=0) to 'a'.
    Do the same for the right edge.
    Return the changed grid.
    >>> grid = Grid.build([['b', 'b', 'b'], ['x', 'x', 'x']])
    >>> set_edges(grid)
    [['a', 'b', 'a'], ['a', 'x', 'a']]
    """
    pass
    for y in range(grid.height):
        grid.set(0, y, 'a')
        grid.set(grid.width - 1, y, 'a')
    return grid


def random_right(grid):
    """
    Set the right edge of the grid to some
    random letters from 'doofus'.
    (provided)
    """
    for y in range(grid.height):
        if random.randrange(10) == 0:  # 10% of the time
            ch = random.choice('doofus')
            grid.set(grid.width - 1, y, ch)
    return grid


def scroll_left(grid):
    """
    Implement scroll_left as in lecture notes.
    >>> grid = Grid.build([['a', 'b', 'c'], ['d', None, None]])
    >>> scroll_left(grid)
    [['b', 'c', None], [None, None, None]]
    """
    for y in range(grid.height):
        for x in range(grid.width):
            # Move char at x,y leftwards
            ch = grid.get(x, y)
            if ch != None and grid.in_bounds(x - 1, y):
                grid.set(x - 1, y, ch)
            grid.set(x, y, None)
            # This works correctly. Slight refinement:
            # Could arrange the logic to set x,y to None
            # only if ch != None
            # Setting it to None when it already is None
            # is a little silly.
    return grid


# ************* Utility Functions Below here


def draw_grid_canvas(grid, canvas):
    """
    Draw the movie grid to the canvas.
    """
    canvas.delete('all')
    canvas.create_rectangle(0, 0, grid.width * SIDE, grid.height * SIDE, fill='black')

    for y in range(grid.height):
        for x in range(grid.width):
            val = grid.get(x, y)
            if val:
                pixel_x = SIDE * x
                pixel_y = SIDE * y
                canvas.create_text(pixel_x, pixel_y, text=val, anchor=tkinter.NW, fill='white', font=('Courier', 24))

    canvas.update()


def movie_action(grid, canvas):
    """Do one round of the move, call in timer."""
    random_right(grid)
    draw_grid_canvas(grid, canvas)
    scroll_left(grid)


# TK Timer fns:


def start_timer(top, delay_ms, fn):
    """Start the my_timer system, calls given fn"""
    top.after(delay_ms, lambda: my_timer(top, delay_ms, fn))


def my_timer(top, delay_ms, fn):
    """my_timer callback, re-posts itself."""
    fn()
    top.after(delay_ms, lambda: my_timer(top, delay_ms, fn))


def main():
    args = sys.argv[1:]

    width = 30
    height = 30
    # Can give width/height on command line
    if len(args) == 2:
        width = int(args[0])
        height = int(args[1])

    grid = Grid(width, height)

    canvas = drawcanvas.make_canvas(width * SIDE, height * SIDE, 'Movie')
    draw_grid_canvas(grid, canvas)

    start_timer(canvas, 30, lambda: movie_action(grid, canvas))

    tkinter.mainloop()


if __name__ == '__main__':
    main()

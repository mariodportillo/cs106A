#!/usr/bin/env python3

"""
Stanford CS106A BabyNames Project
Part-B: graphics GUI built on the baby data
"""

import sys
import tkinter
import babynames


# Provided constants to load and draw the baby data
FILENAMES = ['baby-1900.txt', 'baby-1910.txt', 'baby-1920.txt', 'baby-1930.txt',
             'baby-1940.txt', 'baby-1950.txt', 'baby-1960.txt', 'baby-1970.txt',
             'baby-1980.txt', 'baby-1990.txt', 'baby-2000.txt', 'baby-2010.txt',
             'baby-2020.txt']

YEARS = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000,
         2010, 2020]
SPACE = 20
COLORS = ['red', 'purple', 'green']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def compute_x(width, year_index):
    """
    Given canvas width and year_index 0, 1, 2 .. into YEARS list,
    return the x value for the vertical line for that year.
    """

    years = len(YEARS)

    # calculate inner space by dividing the years by the amount of available space
    inner_space = (width - SPACE - SPACE) / years

    # calculates x by adding SPACE to the year_index * inner space
    x = SPACE + year_index * inner_space

    return x


def draw_fixed(canvas):
    """
    Erases the given canvas and draws the fixed lines on it.
    """
    canvas.delete('all')
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    # creates the 2 horizontal lines at the top and bottom
    canvas.create_line(SPACE, SPACE, width - SPACE, SPACE, fill="Black")
    canvas.create_line(SPACE, height - SPACE, width - SPACE, height - SPACE, fill="Black")

    # makes vertical lines separated evenly and creates the  years text for each year
    for i in range(len(YEARS)):
        canvas.create_line(compute_x(width, i), 0, compute_x(width, i), height)
        canvas.create_text(compute_x(width, i) + TEXT_DX, (height - SPACE), text= YEARS[i], anchor=tkinter.NW, fill='Black')



def compute_rank(names, name, year):
    """
    Given names dict, name string, and int year e.g. 1900.
    Return the best rank to use: the actual rank if
    that name+year exists in the data, or MAX_RANK
    if the name or year is not present.
    >>> # Tests provided, code TBD
    >>> compute_rank({'Abe': {1900: 100}}, 'Abe', 1900)
    100
    >>> compute_rank({'Abe': {1900: 100}}, 'Abe', 2020)
    1000
    >>> compute_rank({'Abe': {1900: 100}}, 'Alice', 1900)
    1000
    """
    # Creates a dictionary if name is not in the dictionary
    if name not in names:
        names[name] = {}

    years = names[name]

    # If year is not in the years then set years[year] equal to MAX_RANK
    if year not in years:
        years[year] = MAX_RANK

    return years[year]


def compute_y(names, name, height, year_index):
    """
    Given names dict, name string, canvas height, and
    year_index 0 1 2 ..., compute and return the y for
    the that name/year_index line endpoint.
    """
    year = YEARS[year_index]

    rank = compute_rank(names, name, year)

    bottom = (height - SPACE)

    """
    We can use the equation of a line to determine y
    y = m(rank) + b 
    m = (y2 - y1)/(x2 - x1) 
    
    We use whats given to us by our two points and connect the two
    f(1) = SPACE  -> Top 
    f(MAX_RANK) = bottom
    
    Use rise over run to determine the slope or rate of change
    x1 = MAX_RANK y1 = bottom
    x2 = 1 y2 = SPACE
    m = (SPACE - bottom) / (MAX_RANK - 1)
    
    Then solve for b in y = m(rank) + b given our rank and two points
    f(1) = Space
    SPACE = m(1) + b
    b = SPACE - m
    
    """

    m = (SPACE - bottom) / (1 - MAX_RANK)
    b = SPACE - m

    y = m * rank + b
    return y

def draw_name(canvas, names, name, color):
    """
    Given canvas, and names dict.
    Draw the data for the given name in the given color.
    """
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    # initializes previous_x and previous_y
    previous_x = None
    previous_y = None

    for i in range(len(YEARS)):
        year_index = i
        year = YEARS[year_index]

        # get our x and y using our helper functions
        x = compute_x(width, year_index)
        y = compute_y(names, name, height, year_index)

        # want the rank to be a string, so we can print it to the canvas later
        rank = str(compute_rank(names, name, year))

        # canvas.create_line(x, y, x + 40, y, width=LINE_WIDTH, fill=color)

        # Creates the text Name with the text Rank number next to point
        canvas.create_text(x + TEXT_DX, y, text=name + " " + rank, anchor=tkinter.SW, fill=color)

        # Creates lines connecting the two points
        if previous_x is not None and previous_y is not None:
            canvas.create_line(x, y, previous_x, previous_y, width=LINE_WIDTH, fill=color)

        # Sets previous_x and previous_y to be the current x and current y  to be used in future iteration
        previous_x = x
        previous_y = y



def draw_names(canvas, names, lookups):
    """
    Given canvas, names dict, lookups list of name strings,
    Draw the data for the lookups on the canvas.
    """
    draw_fixed(canvas)

    # Jennifer dev-mode - set to False and/or delete these lines
    # for last part.
    value = len(COLORS)

    for i in lookups:
        # grabs the index of the name in lookups
        name_idx = lookups.index(i)

        # takes the modulo of name_idx by value to get repeating colors
        color_idx = name_idx % value

        # draws the name with the correct color.
        draw_name(canvas, names, i, COLORS[color_idx])

def upper_name(name):
    """
    (provided)
    The names in the SSA data set all have their first
    char uppercase, then lowercase e.g. 'Emily'.
    Given a name typed by the user, change its case
    to the SSA form.
    >>> upper_name('emily')
    'Emily'
    >>> upper_name('EMILY')
    'Emily'
    """
    if len(name) > 0:
        return name[0].upper() + name[1:].lower()
    return name


def make_gui(top, width, height, names):
    """
    (provided)
    Set up the GUI elements for Baby Names, returning the TK Canvas to use.
    top is TK root, width/height is canvas size, names is BabyNames dict.
    """
    # name entry field
    entry = tkinter.Entry(top, width=60, name='entry', borderwidth=2)
    entry.grid(row=0, columnspan=12, sticky='w')
    entry.focus()

    # canvas for drawing
    canvas = tkinter.Canvas(top, width=width, height=height, name='canvas')
    canvas.grid(row=1, columnspan=12, sticky='w')

    space = tkinter.LabelFrame(top, width=10, height=10, borderwidth=0)
    space.grid(row=2, columnspan=12, sticky='w')

    # Search field etc. at the bottom
    label = tkinter.Label(top, text='Search:')
    label.grid(row=3, column=0, sticky='w')
    search_entry = tkinter.Entry(top, width=15, name='searchentry')
    search_entry.grid(row=3, column=1, sticky='w')
    search_out = tkinter.Text(top, height=3, width=70, name='searchout', borderwidth=2)
    search_out.grid(row=3, column=3, sticky='w')

    # When <return> key is hit in a text field .. connect to the handle_draw()
    # and handle_search() functions to do the work.
    entry.bind('<Return>', lambda event: handle_draw(entry, canvas, names))
    search_entry.bind('<Return>', lambda event: handle_search(search_entry, search_out, names))

    top.update()
    return canvas


def handle_draw(entry, canvas, names):
    """
    (provided)
    Called when <return> key hit in given text entry field.
    Gets search text, looks up names, calls draw_names()
    for those names to draw the results.
    """
    text = entry.get()
    lookups = text.split()
    lookups = [upper_name(s) for s in lookups]  # convert names to upper-first form
    draw_names(canvas, names, lookups)


def handle_search(search_entry, search_out, names):
    """
    (provided) Called for <return> key in lower search field.
    Calls babynames.search() and displays results in GUI.
    Gets search target from given search_entry, puts results
    in given search_out text area.
    """
    target = search_entry.get().strip()
    search_out.delete('1.0', tkinter.END)
    # GUI detail: by deleting always, but only putting in new text
    # if there is data .. hitting return on an empty field
    # lets the user clear the output.
    if target:
        # Call the search_names function in babynames.py
        result = babynames.search_names(names, target)
        out = ' '.join(result)
        search_out.insert('1.0', out)


# main() code is provided
def main():
    args = sys.argv[1:]
    # Establish size - user can override
    width = 1000
    height = 600
    # Let command line override size of window
    if len(args) == 2:
        width = int(args[0])
        height = int(args[1])

    # Load data
    names = babynames.read_files(FILENAMES)

    # Make window
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = make_gui(top, width, height, names)

    # draw_fixed once at startup so we have the lines
    # even before the user types anything.
    draw_fixed(canvas)

    # This needs to be called just once
    top.mainloop()


if __name__ == '__main__':
    main()

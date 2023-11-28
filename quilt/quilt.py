#!/usr/bin/env python3

"""
Stanford CS106A Quilt Project
"""

import sys
from drawcanvas import DrawCanvas


def draw_bars(canvas, left, top, width, height, n):
    """
    Draw bars in the given canvas at left, top, with width, height, n
    """
    canvas.draw_rect(left, top, width, height, color='lightblue')

    for i in range(n):
        x_add = (i / (n - 1) * (width - 1))

        canvas.draw_line(left + x_add, top, left + x_add, top + height - 1)




def draw_eye(canvas, left, top, width, height, n):
    """
    Draw eye in the given canvas at left, top with width, height, n
    """
    canvas.draw_rect(left, top, width, height, color='lightblue')

    canvas.fill_oval(left, top, width, height, color="yellow")

    for i in range(n):
        x_add = (i / (n - 1) * (width - 1))

        canvas.draw_line(left + ((width - 1) * 0.5), top + ((height - 1) * 0.5), left + x_add, top + height - 1)

def draw_bowtie(canvas, left, top, width, height, n):
    """
    Draw bowtie in the given canvas at left, top, with width, height, n
    """
    canvas.draw_rect(left, top, width, height, color='lightblue')

    for i in range(n):
        y_delta = (i / (n - 1) * (height - 1))

        canvas.draw_line(left, top + y_delta, left + width - 1, top + height - 1 - y_delta, color='red')


def draw_power(canvas, left, top, width, height, n):
    """
    Draw power patch at the given left, top, with width, height, n.
    """
    canvas.draw_rect(left, top, width, height, color='lightblue')
    draw_bowtie(canvas, left, top, (width - 1) * 0.5, (height - 1) * 0.5, n)
    draw_eye(canvas, left + ((width - 1) * 0.5), top + ((height - 1) * 0.5), (width - 1) * 0.5, (height - 1) * 0.5, n)


def draw_quilt(width, height, n):
    """
    Create a canvas of width, height and draw the whole
    quilt on it. Draw an n by n grid of patches.
    """
    canvas = DrawCanvas(width, height, title="Quilt")

    sub_width = width / n
    sub_height = height / n

    # Your code here
    for row in range(n):
        for col in range(n):
            choice = (row + col) % 4

            left = col * sub_width
            top = row * sub_height

            if choice == 1:
                draw_eye(canvas, left, top, sub_width, sub_height, n)
            elif choice == 2:
                draw_power(canvas, left, top, sub_width, sub_height, n)
            elif choice == 3:
                draw_bowtie(canvas, left, top, sub_width, sub_height, n)
            else:
                draw_bars(canvas, left, top, sub_width, sub_height, n)



# main() code is complete.
# There are 5 command lines that work here,
# with width/height/n being positive integers.
#  -bars width height n
#  -eye width height n
#  -bowtie width height n
#  -power width height n
#  -quilt width height n
# e.g. run like this in the terminal:
#  python3 quilt.py -bars 600 400 10


def main():
    # main() code is complete.
    # This main() is not a great example of command line processing,
    # as this application has some unusual issues.

    args = sys.argv[1:]
    if len(args) != 4:
        print('usage: (one of -bars -eye -bowtie -power -quilt) width height n')
        return

    # Parse width/height/n from command line, giving a helpful
    # error message if it fails.
    try:
        window_width = int(args[1])
        window_height = int(args[2])
        n = int(args[3])
    except Exception:
        print("Error parsing int width/height/n from command line:" + ' '.join(args))
        return

    # Width/height of one patch
    width = window_width / 2
    height = window_height / 2

    # Tricky: we do all the drawing in a try, so that if it takes an exception,
    # we can still do the mainloop() at the end. If we do not do this, an exception
    # causes no graphics output to appear which makes debugging hard.
    try:
        if args[0] == '-bars':
            canvas = DrawCanvas(window_width, window_height, fast_draw=True, title='Quilt')
            # Can change to fast_draw=False .. drawing plays out more slowly
            draw_bars(canvas, 0, 0, width, height, n)
            draw_bars(canvas, width, height, width, height, n)

        if args[0] == '-eye':
            canvas = DrawCanvas(window_width, window_height, fast_draw=True, title='Quilt')
            draw_eye(canvas, 0, 0, width, height, n)
            draw_eye(canvas, width, height, width, height, n)

        if args[0] == '-bowtie':
            canvas = DrawCanvas(window_width, window_height, fast_draw=True, title='Quilt')
            draw_bowtie(canvas, 0, 0, width, height, n)
            draw_bowtie(canvas, width, height, width, height, n)

        if args[0] == '-power':
            canvas = DrawCanvas(window_width, window_height, fast_draw=True, title='Quilt')
            draw_power(canvas, 0, 0, width, height, n)
            draw_power(canvas, width, height, width, height, n)

        if args[0] == '-quilt':
            draw_quilt(window_width, window_height, n)

    # Print out exception from draw
    except Exception as e:
        print(e)

    DrawCanvas.mainloop()


if __name__ == '__main__':
    main()

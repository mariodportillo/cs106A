#!/usr/bin/env python3

"""
Stanford CS106A Ghost Project
"""

import os
import sys

# This line imports SimpleImage for use here
# This depends on the Pillow package
from simpleimage import SimpleImage


def pix_dist2(pix1, pix2):
    """
    Returns the square of the color distance between 2 pix tuples.
    >>> pix_dist2((1, 2, 3), (3, 4, 5 ))
    12

    >>> pix_dist2((0, 1, 2), (6, 3, 2))
    40

    >>> pix_dist2((2, 2, 2), (1, 2, 4))
    5

    """

    # Finds the differences between each value of rgb.
    x_difference = (pix1[0] - pix2[0]) ** 2
    y_difference = (pix1[1] - pix2[1]) ** 2
    z_difference = (pix1[2] - pix2[2]) ** 2

    # Determines the overall difference by adding all the calculated differences together.
    dist = x_difference + y_difference + z_difference

    return dist

def average_pix(pixs):
    """
    Takes in list of pix and determines the average.
    :return: Average of pixs in a list
    >>> average_pix([(1, 4, 1), (5, 6, 1), (0, 2, 4)])
    (2.0, 4.0, 2.0)

    >>> average_pix([(3, 6, 8), (0, 6, 2), (0, 0, 5)])
    (1.0, 4.0, 5.0)

    >>> average_pix([(20, 9, 1), (0, 5, 3)])
    (10.0, 7.0, 2.0)

    """
    # init the totals.
    totalr = 0
    totalg = 0
    totalb = 0

    # add up all the totals based on how many pixs there are.
    for i in pixs:
        r_value = i[0]
        g_value = i[1]
        b_value = i[2]

        totalr += r_value
        totalb += b_value
        totalg += g_value

    # take the average of each rgb value by dividing by how many pixs we have.

    averager = totalr/len(pixs)
    averageg = totalg/len(pixs)
    averageb = totalb/len(pixs)

    # We can then store the averages of the RGB values in a Tuple.
    pixaverage = (averager, averageg, averageb)

    return pixaverage



def best_pix(pixs):
    """
    Given a list of 1 or more pix, returns the best pix.
    >>> best_pix([(1,2,3), (5,6,7)])
    (1, 2, 3)

    >>> best_pix([(5,6,7), (0, 1, 2), (1,2,3)])
    (1, 2, 3)

    >>> best_pix([(5,6,7),(0,1,2),(1,2,3),(2, 3,0)])
    (1, 2, 3)

    >>> best_pix([(5,6,7),(0,1,2),(9,2,3),(2,3,4)])
    (2, 3, 4)
    """
    # gets the average of all the pixs.
    avg = average_pix(pixs)

    # finds the distance between each pix and the avg.
    distances = list(map(lambda pix: pix_dist2(pix, avg), pixs))

    # set bestpix variable equal to the lowest distance.
    bestpix = min(distances)

    # We want to find the index of the bestpix in the distances list.
    pixidx = distances.index(bestpix)

    # Return the pix at the bestpix index.
    return pixs[pixidx]



def good_apple_pix(pixs):
    """
    Given a list of 2 or more pix, return the best pix
    according to the good-apple strategy.
    >>> good_apple_pix([(18, 18, 18), (0, 2, 0), (19, 23, 18), (19, 22, 18), (19, 22, 18), (1, 0, 1)])
    (19, 22, 18)
    """
    avg = average_pix(pixs)

    # Use lambda to create a sorted list of the pix based on their distance to average.
    lst = sorted(pixs, key=lambda pix: pix_dist2(pix, avg))

    # Find the middle of the list
    mid = len(lst) // 2

    # Make a goodlist of pixs that only includes everything before the midpoint
    goodlist = lst[:mid]

    # Using our new goodlist we use best_pix() helper function to output the true best pix.
    return best_pix(goodlist)


def pixs_at_xy(images, x, y):
    """
    takes in a list of images and (x,y) and creates an output list of all the rgb values in those images.
    """
    pixs = []

    # loops through each image and extracts each RGB value at the specified (x, y).
    for image in images:
        pix = image.get_pix(x, y)
        pixs.append(pix)

    # returns list with tuple data that holds the rgb values of each image at (x, y).
    return pixs

def solve(images, mode):
    """
    Given a list of image objects and mode,
    compute and show a Ghost solution image based on these images.
    Mode will be None or '-good'.
    There will be at least 3 images and they will all be
    the same size.
    """
    # init width and height based on the first image
    width = images[0].width
    height = images[0].height

    # solution will be a blank image initially.
    solution = SimpleImage.blank(width, height)

    # condition to run either good_apple mode or non good_apple mode
    if mode == "-good":

        # loops through each (x,y) in the given height and width
        for y in range(height):
            for x in range(width):

                # extracts a list of the pixs from each image at the specific (x, y)
                pixs = pixs_at_xy(images, x, y)

                # determines the best pix at that (x, y) using the good_apple method
                best = good_apple_pix(pixs)

                # sets the pix at (x, y) on the solution canvas to the best rgb values
                solution.set_pix(x, y, best)
    else:
        for y in range(height):
            for x in range(width):

                # extracts a list of the pixs from each image at the specific (x, y)
                pixs = pixs_at_xy(images, x, y)

                # determines the best pix at that (x, y)
                best = best_pix(pixs)

                # sets the pix at (x, y) on the solution canvas to the best rgb values
                solution.set_pix(x, y, best)

    solution.show()


def jpgs_in_dir(dir):
    """
    (provided)
    Given the name of a directory
    returns a list of the .jpg filenames within it.
    """
    filenames = []
    for filename in os.listdir(dir):
        if filename.endswith('.jpg'):
            filenames.append(os.path.join(dir, filename))
    return filenames


def load_images(dir):
    """
    (provided)
    Given a directory name, reads all the .jpg files
    within it into memory and returns them in a list.
    Prints the filenames out as it goes.
    """
    images = []
    jpgs = jpgs_in_dir(dir)
    for filename in jpgs:
        print(filename)
        image = SimpleImage.file(filename)
        images.append(image)
    return images


def main():
    # (provided)
    args = sys.argv[1:]
    # Command line args
    # 1 arg:  dir-of-images
    # 2 args: -good dir-of-images
    if len(args) == 1:
        images = load_images(args[0])
        solve(images, None)

    if len(args) == 2 and args[0] == '-good':
        images = load_images(args[1])
        solve(images, '-good')


if __name__ == '__main__':
    main()

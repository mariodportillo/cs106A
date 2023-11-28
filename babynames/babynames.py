#!/usr/bin/env python3

"""
Stanford CS106A BabyNames Project
Part-A: organizing the bulk data
"""

import sys

YEARS = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000,
         2010, 2020]
def add_name(names, year, rank, name):
    """
    Add the given data: int year, int rank, string name
    to the given names dict and return it.
    (1 test provided, more tests TBD)
    >>> add_name({}, 2000, 10, 'Abe')
    {'Abe': {2000: 10}}
    >>> # Student Tests Here (keep this line)
    >>> add_name({"Abe": {2003: 5}}, 2004, 4, 'Abe')
    {'Abe': {2003: 5, 2004: 4}}
    >>> add_name({"Abe": {2003: 6}}, 2003, 5, 'Abe')
    {'Abe': {2003: 5}}
    """
    # Creates dicitionary for names.
    if name not in names:
        names[name] = {}

    years = names[name]

    # Sets the year key to a rank
    if year not in years:
        years[year] = rank
    else:
        # Else condition if the rank already exist to compare the two.
        existing_rank = years[year]
        if existing_rank > rank:

            # if exisiting_rank is greater than the new rank then just set the rank to the new one
            years[year] = rank

    return names



def parse_year(filename):
    """
    Given filename, like 'baby-2000.txt'
    extract and return the int year from between
    the dash and the dot, e.g. 2000
    Raises an exception on failure.
    (Tests provided)
    >>> parse_year('baby-2000.txt')
    2000
    >>> parse_year('infant-123.txt')
    123
    >>> parse_year('nope123.txt')  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    Exception: Cannot parse filename:nope123.txt
    """

    if "." in filename and "-" in filename:
        first_parts = filename.split('.')

        # After the first split the second part must also be split up, so we only get the year alone.
        second_part = first_parts[0].split("-")

        # We want it to return only the year so from ["string", "year"] we extract only the year as an int.
        return int(second_part[1])
    else:
        raise Exception('Cannot parse filename:' + filename)




def add_file(names, filename):
    """
    Given a names dict and filename like baby-2000.txt,
    add the file's data to the dict and return it.
    (Tests provided, Code TBD)
    >>> add_file({}, 'small-2000.txt')
    {'Bob': {2000: 1}, 'Alice': {2000: 1}, 'Cindy': {2000: 2}}
    >>> add_file({}, 'small-2010.txt')
    {'Yot': {2010: 1}, 'Zena': {2010: 1}, 'Bob': {2010: 2}, 'Alice': {2010: 2}}
    >>> # Names non-empty, add small-2010.txt to it
    >>> add_file({'Bob': {2000: 1}, 'Alice': {2000: 1}, 'Cindy': {2000: 2}}, 'small-2010.txt')
    {'Bob': {2000: 1, 2010: 2}, 'Alice': {2000: 1, 2010: 2}, 'Cindy': {2000: 2}, 'Yot': {2010: 1}, 'Zena': {2010: 1}}
    """
    # use the parse_year function to get our year
    year = parse_year(filename)

    with open(filename) as f:
        for line in f:
            line = line.strip()
            parts = line.split(',')

            # We have to split up each line because we know it is separated by a ",".

            rank = int(parts[0])

            # We need to have two name values for the girls and the boys
            name1 = parts[1]
            name2 = parts[2]

            # We call the add_name() twice because we have name1 and name2 values
            add_name(names, year, rank, name1)
            add_name(names, year, rank, name2)
    return names




def read_files(filenames):
    """
    Given list of filenames, build and return a names dict
    of all their data.
    >>> read_files(['small-2000.txt', 'small-2010.txt'])
    {'Bob': {2000: 1, 2010: 2}, 'Alice': {2000: 1, 2010: 2}, 'Cindy': {2000: 2}, 'Yot': {2010: 1}, 'Zena': {2010: 1}}
    """

    names = {}

    # Loop through each file, if the file is not in names than we want to add it to the dictionary using our add_file()
    for file in filenames:
        if file not in names:
            add_file(names, file)
    return names


def search_names(names, target):
    """
    Given names dict and a target string,
    return a sorted list of all the name strings
    that contain that target string anywhere.
    Not case sensitive.
    (Code and tests TBD)
    >>> search_names({'Bob': {2000: 1}, 'Alice': {2000: 1}, 'Cindy': {2000: 2}}, "i")
    ['Alice', 'Cindy']
    >>> search_names({'Aalex': {2000: 1}, 'Alice': {2000: 1}, 'Andy': {2000: 2}}, "A")
    ['Aalex', 'Alice', 'Andy']
    >>> search_names({'Jacob': {2000: 1}, 'Denise': {2000: 1}, 'Chuck': {2000: 2}}, "y")
    []
    """

    result = []

    # Loop through each key in names dictionary and search for the target to add it to a new array to be returned.
    for key in names.keys():
        if target.lower() in key.lower():
            result.append(key)
    return sorted(result)


def print_names(names):
    """
    (provided)
    Given names dict, print out all its data, one name per line.
    The names are printed in increasing alphabetical order,
    with its years data also in increasing order, like:
    Aaden [(2010, 560)]
    Aaliyah [(2000, 211), (2010, 56)]
    ...
    Surprisingly, this can be done with 2 lines of code.
    We'll explore this in lecture.
    """
    for key, value in sorted(names.items()):
        print(key, sorted(value.items()))


def main():
    # (provided)
    args = sys.argv[1:]
    # Two command line forms
    # 1. file1 file2 file3 ..
    # 2. -search target file1 file2 file3 ..

    # Assume no search, so list of filenames to read
    # is the args list
    filenames = args

    # Check if we are doing search, set target variable
    target = ''
    if len(args) >= 2 and args[0] == '-search':
        target = args[1]
        filenames = args[2:]  # Change filenames to skip first 2

    # Read in all the filenames: baby-1990.txt, baby-2000.txt, ...
    names = read_files(filenames)

    # Either we do a search or just print everything.
    if target != '':
        search_results = search_names(names, target)
        for name in search_results:
            print(name)
    else:
        print_names(names)


if __name__ == '__main__':
    main()

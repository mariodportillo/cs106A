#!/usr/bin/env python3

"""
Stanford CS106A TipTop Project
"""

import sys


# define functions here
def read_tags(filename):
    """
    This function will read the filename and extract a dictionary which
    includes the hastags as  keys and the users in list to those hashtags

    >>> read_tags("test1.txt")
    {'#aaa': ['@bob', '@alice'], '#bbb': ['@bob', '@alice']}

    >>> read_tags("test2.txt")
    {'#bbb': ['@alice', '@bob'], '#aaa': ['@alice', '@bob', '@aardvark'], '#z': ['@bob']}
    """
    # init a new dictionary called tags
    tags = {}

    with open(filename) as f:
        # go line by line
        for line in f:
            # strip each line of any spaces
            line = line.strip()

            # split the new string based on the ^ sign.
            parts = line.split("^")

            # we know the poster will be first, so we set it equal to the first item in parts.
            poster = parts[0].lower()

            # We need to loop through each part in parts after the poster.
            for i in parts[1:]:
                # let the tag be equal to each part after poster.
                tag = i.lower()

                # if statement that sets our tag equal to an empty list if tag is not in our dictionary.
                if tag not in tags:
                    tags[tag] = []

                users = tags[tag]

                # if our poster is not already assigned to that tag then we add it to the list in our dictionary.
                if poster not in users:
                    users.append(poster)

    return tags

def print_tags(filename):
    """
    This function will take in the filename then
    print out the key of the tags tictionary first
    with all the values inside sorted alphabetically.
    All the keys are also sorted out alfabetically.


    >>> print_tags("test1.txt")
    #aaa
     @alice
     @bob
    #bbb
     @alice
     @bob

    """
    # creates a dictionary of all our tags using the read_tags() helper
    tags = read_tags(filename)

    # makes a list of all the keys inside of tag
    keys = list(tags.keys())

    # sorts the list of keys alphabetically
    keys.sort()

    # loops through each key
    for key in keys:
        # looks up the value for each key which is a list of users
        values = tags[key]

        #  sorts the list of users at each key alphabetically
        values.sort()

        # prints the key
        print(key)

        # Prints a space and each value that is inside the list of users
        for value in values:
            print(" " + value)

def main():
    args = sys.argv[1:]

    if len(args) == 1:
        print_tags(args[0])


if __name__ == '__main__':
    main()

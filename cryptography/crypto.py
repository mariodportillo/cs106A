#!/usr/bin/env python3

"""
Stanford CS106A Cryptography Project
"""

import sys

# provided ALPHABET constant - list of the regular alphabet
# in lowercase. Refer to this simply as ALPHABET in your code.
# This list should not be modified.
ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']


def compute_slug(key):
    """
    :param key: A string used to create a slug.
    :return slug: A slug which is used to encrypt messages.

    Given a key string, compute and return the len-26 slug list for it.
    >>> compute_slug('z')
    ['z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y']
    >>> compute_slug('Bananas!')
    ['b', 'a', 'n', 's', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'o', 'p', 'q', 'r', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    >>> compute_slug('Life, Liberty, and')
    ['l', 'i', 'f', 'e', 'b', 'r', 't', 'y', 'a', 'n', 'd', 'c', 'g', 'h', 'j', 'k', 'm', 'o', 'p', 'q', 's', 'u', 'v', 'w', 'x', 'z']
    >>> compute_slug('Zounds!')
    ['z', 'o', 'u', 'n', 'd', 's', 'a', 'b', 'c', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'p', 'q', 'r', 't', 'v', 'w', 'x', 'y']
    """
    result = []

    # This for loop allows us to loop through each letter in key and if the letter is in the
    # ALPHABET and not already in the list add it to result.

    for i in key:
        ch = i.lower()
        if ch in ALPHABET and ch not in result:
            result.append(ch)

    # This for loop goes through the ALPHABET list and adds anything that is not in result into result.
    for i in ALPHABET:
        if i not in result:
            result.append(i)

    return result


def encrypt_char(source, slug, ch):
    """
    Given source and slug lists,
    if the char ch is in source, return
    its encrypted form. Otherwise return ch unchanged.

    :param source: This is the original list of letters used.
    :param slug:This is the list that contains the key at the start with no repeating letters.
    :param ch: An inputed char from original list to be encrypted using the slug.
    :return ch: Outputs the encrypted char form of the inputted char.


    >>> encrypt_char(['a', 'b', 'c', 'd'], ['d', 'c', 'b', 'a'], 'a')
    'd'
    >>> encrypt_char(['a', 'b', 'c', 'd'], ['d', 'c', 'b', 'a'], 'c')
    'b'
    >>> encrypt_char(['a', 'b', 'c', 'd'], ['d', 'c', 'b', 'a'], 'C')
    'B'
    >>> encrypt_char(['a', 'b', 'c', 'd'], ['d', 'c', 'b', 'a'], ',')
    ','
    >>> # Compute 'z' slug, store it in a var named z_slug
    >>> # and pass that in as the slug for the tests.
    >>> z_slug = compute_slug('z')
    >>> encrypt_char(ALPHABET, z_slug, 'A')
    'Z'
    >>> encrypt_char(ALPHABET, z_slug, 'n')
    'm'
    >>> encrypt_char(ALPHABET, z_slug, ' ')
    ' '
    """

    # If the char is in source we will then use its old index from source to match it with its new index of the slug.
    if ch.lower() in source:
        old = source.index(ch.lower())
        if ch.isupper():
            ch = slug[old].upper()
            return ch
        ch = slug[old]

    return ch


def encrypt_str(source, slug, s):
    """
    :param source: This is the original list of letters used.
    :param slug: This is the list that contains the key at the start with no repeating letters.
    :param s: An inputed string from original list to be encrypted using the slug.
    :return result: The returned value is a new modified string which is encrypted based on the source and slug provided.

    Given source and slug lists and string s,
    return a version of s where every char
    has been encrypted by source/slug.
    >>> z_slug = compute_slug('z')
    >>> encrypt_str(ALPHABET, z_slug, 'And like a thunderbolt he falls.')
    'Zmc khjd z sgtmcdqanks gd ezkkr.'
    """

    # Here we use a for loop to loop through each char in s to encrypt it.
    result = ""

    for i in s:
        result += encrypt_char(source, slug, i)

    return result


def decrypt_str(source, slug, s):
    """
    Given source and slug lists and encrypted string s,
    return the decrypted form of s.
    :param source: This is the original list of letters used.
    :param slug: This is the list that contains the key at the start with no repeating letters.
    :param s: An encrypted string that needs to be decrypted to make sense of.
    :return result: The returned value is the original decrypted string.

    >>> z_slug = compute_slug('z')
    >>> decrypt_str(ALPHABET, z_slug, 'Zmc khjd z sgtmcdqanks gd ezkkr.')
    'And like a thunderbolt he falls.'
    """
    result = ""
    # Use a for loop to go  through each char and assign its bad slug index to its original source index.

    for i in s:
        if i.lower() in slug:
            bad = slug.index(i.lower())
            if i.isupper():
                result += source[bad].upper()
            else:
                result += source[bad]

        elif i == " ":
            result += " "
        elif i == ".":
            result += "."
        elif i == ",":
            result += ","
        elif i == "'":
            result += "'"

    return result


def encrypt_file(filename, key):
    """
    Given filename and key, compute and
    print the encrypted form of its lines.

    :param filename: The name of the file which you want to encrypt.
    :param key: The assigned key that will be used to create a slug.
    :return print(line): The printed values will be encrypted forms of the inputed file.

    >>> encrypt_file('test-plain.txt', 'z')
    zab
    wxy

    """
    # Going through the file and use a for loop to encrypt each line using the ALPHABET
    # and a generated slug with the key provided.
    with open(filename) as f:
        slug = compute_slug(key)

        for line in f:
            line = line.strip()
            line = encrypt_str(ALPHABET, slug, line)

            print(line)


def decrypt_file(filename, key):
    """
    :param filename: The name of the file which you want to encrypt.
    :param key: The assigned key that will be used to create a slug.
    :return print(line): The printed values will be decrypted forms of the inputed file.

    Given filename and key, compute and
    print the decrypted form of its lines.
    >>> decrypt_file('test-crypt.txt', 'z')
    abc
    xyz
    """
    # Going through the file and use a for loop to decrypt each line using the ALPHABET
    # and a generated slug with the key provided.

    with open(filename) as f:
        slug = compute_slug(key)

        for line in f:
            line = line.strip()
            line = decrypt_str(ALPHABET, slug, line)
            print(line)


def main():
    args = sys.argv[1:]
    # 2 command line argument patterns:
    # -encrypt key filename
    # -decrypt key filename
    # Call encrypt_file() or decrypt_file() based on the args.
    if len(args) == 3 and args[0] == "-encrypt":
        encrypt_file(args[2], args[1])
    elif len(args) == 3 and args[0] == "-decrypt":
        decrypt_file(args[2], args[1])


# Python boilerplate.
if __name__ == '__main__':
    main()

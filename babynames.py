#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re

"""Baby Names exercise"""


def extract_names(filename):
    """
    Given a file name for baby.html, returns a list starting with the year string
    followed by the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
    """

    # The list [year, name_and_rank, name_and_rank, ...] we'll eventually return.
    names = []

    # Open and read the file.
    f = open(filename, 'rU')
    text = f.read()
    # Could process the file line-by-line, but regex on the whole text
    # at once is even easier.

    # Get the year.
    year_match = re.search(r'Popularity\sin\s(\d\d\d\d)', text)
    if not year_match:
        # We didn't find a year, so we'll exit with an error message.
        sys.stderr.write('Couldn\'t find the year!\n')
        sys.exit(1)
    year = year_match.group(1)
    names.append(year)

    # Extract all the data tuples with a findall()
    # each tuple is: (rank, boy-name, girl-name)
    tuples = re.findall(r'<td>(\d+)</td><td>(\w+)</td>\<td>(\w+)</td>', text)
    # print tuples

    # Store data into a dict using each name as a key and that
    # name's rank number as the value.
    # (if the name is already in there, don't add it, since
    # this new rank will be bigger than the previous rank).
    names_to_rank = {}
    for rank_tuple in tuples:
        (rank, boyname, girlname) = rank_tuple  # unpack the tuple into 3 vars
        if boyname not in names_to_rank:
            names_to_rank[boyname] = rank
        if girlname not in names_to_rank:
            names_to_rank[girlname] = rank
    # You can also write:
    # for rank, boyname, girlname in tuples:
    #   ...
    # To unpack the tuples inside a for-loop.

    # Get the names, sorted in the right order
    sorted_names = sorted(names_to_rank.keys())

    # Build up result list, one element per line
    for name in sorted_names:
        names.append(name + " " + names_to_rank[name])

    return names


def main():
    # This command-line parsing code is provided.
    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]

    if not args:
        print('usage: [--summaryfile] file [file ...]')
        sys.exit(1)

    # Notice the summary flag and remove it from args if it is present.
    summary = False
    if args[0] == '--summaryfile':
        summary = True
        del args[0]

    for filename in args:
        names = extract_names(filename)

        text = '\n'.join(names)

        if summary:
            with open(filename + '.summary', 'w') as outf:
                outf.write(text + '\n')
                outf.close()
        else:
            print(text)


if __name__ == '__main__':
    main()

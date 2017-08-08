#!/usr/bin/env python

'''Prints a pretty version of the given html file'''

import sys
from bs4 import BeautifulSoup


def main(argv=None):
    '''Argv[1] is the source file'''
    if argv is None:
        argv = sys.argv

    with open(argv[1]) as handle:
        data = handle.read()
        soup = BeautifulSoup(data, 'html.parser')

        print(soup.prettify())


if __name__ == '__main__':
    main()

#!/usr/bin/env python

'''Parse PCS TT ranking data'''

import sys
from bs4 import BeautifulSoup
import pandas as pd
import csv

import pycountry


def nation_full_name(code):
    '''Gets the full name for a nation based on its two digit domain code.'''
    return pycountry.countries.get(alpha_2=code.upper()).name


def int_parser(key, cell):
    '''Returns the integer inside cell'''
    return {key: int(cell.text.strip())}


def ignore_parser(_key, _cell):
    '''Ignores the current cell'''
    return {}


def string_parser(key, cell):
    '''Returns a single string'''
    return {key: cell.text.strip()}


def rider_parser(_key, cell):
    '''Parses the rider name and nationality'''

    names = cell.text.strip().split('\n')
    name = ' '.join(reversed([n.strip() for n in names if n.strip()]))
    nation_tag = cell.select('span.flags')[0]
    classes = nation_tag.attrs['class'][:]
    classes.remove('flags')

    nation = nation_full_name(classes[0])

    return {'name': name,
            'nation': nation}


DISPATCHER = {
    'Rnk': int_parser,
    'Prev.': ignore_parser,
    'Diff.': ignore_parser,
    'Rider': rider_parser,
    'Team': string_parser,
    'Points': int_parser,
    '': ignore_parser
}


def cell_parser(header, cell):
    '''Parses cell according to dispatcher table'''
    return DISPATCHER[header](header, cell)


def parse_header(table):
    '''Parse the header names for a given table.'''

    headers = table.select('thead')[0]
    # print(headers)
    parsed_headers = []
    for header in headers.select('th'):
        for string in header.strings:
            if string.strip():
                parsed_headers.append(string.strip())
                break

    return parsed_headers


def main(argv=None):
    '''Argv[1] is the source file'''
    if argv is None:
        argv = sys.argv

    with open(argv[1]) as handle:
        data = handle.read()
        soup = BeautifulSoup(data, 'html.parser')

    table = soup.select('table[class="basic"]')[0]

    parsed_headers = parse_header(table)
    print(parsed_headers)

    lines = table.select('tr')[1:]  # Skip tr in header

    riders = []

    for line in lines:
        rider = {}
        cells = line.select('td')[:-1]  # Avoid last col with menu
        for i, cell in enumerate(cells):
            header = parsed_headers[i]
            cell_data = cell_parser(header, cell)

            rider = {**rider, **cell_data}

        riders.append(rider)

    for rider in riders:
        print(rider)

    # Writing to csv
    with open('output.csv', 'w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=['Rnk',
                                                    'name',
                                                    'nation',
                                                    'Team',
                                                    'Points'])
        writer.writeheader()
        for rider in riders:
            writer.writerow(rider)

if __name__ == '__main__':
    main()

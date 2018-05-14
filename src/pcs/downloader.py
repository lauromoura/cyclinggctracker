#!/usr/bin/env python

'''Download multipage PCS ranking data'''

import os
import csv
import json
import argparse

from bs4 import BeautifulSoup
from tidylib import tidy_document
import requests


BASE_URL = 'https://www.procyclingstats.com/race/{race}/{year}/stage-{stage}-gc'

def get_soup_for(filename):
    with open(filename) as handle:
        html_raw_data = handle.read()
        html_data, errors = tidy_document(html_raw_data)
    return BeautifulSoup(html_data, 'html.parser')

def save_records_to_csv(records, filename):
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=records[0]._fields)
        writer.writeheader()
        for record in records:
            writer.writerow(record._asdict())

def download(url, filename):
    '''Downloads url to filename'''
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'})
    r.raise_for_status()
    with open(filename, 'w', encoding=r.encoding) as output:
        output.write(r.text)

def get(url, filename, source):
    if source == 'download' or not os.path.isfile(filename):
        download(url, filename)

def cleanup(key, value):
    if key in ('BIB', 'Age', 'UCI', 'Pnt', 'GC'):
        return int(value) if value else 0
    if key in ('Avg',):
        return float(value) if value else 0.0
    if key in ('GC-Time',):
        if '-' in value:
            value = value[3:] # Skip the prefix '+ -'
        else:
            value = value[1:]

        tokens = [int(x) for x in value.split(':')]
        acc = tokens[-1]
        acc += tokens[-2] * 60
        try:
            acc += tokens[-3] * 3600
        except IndexError:
            pass # No hours yet

        return acc

    return value


def process(filename, stage):
    soup = get_soup_for(filename)

    table = soup.select('table.basic')[0]
    headers = [x.text.strip() for x in table.select('thead > tr > th')]
    print(headers)
    riders = []
    for row in table.select('tbody > tr'):
        cells = [cell.text.strip() for cell in row.select('td')]
        rider_data = {key: cleanup(key, value) for key, value in zip(headers, cells)}
        rider_data['Stage'] = stage
        riders.append(rider_data)

    return riders


def jsonify(riders_results):
    riders = {}
    for result in sorted(riders_results, key=lambda res: res['Stage']):
        print(result)
        name = result['Rider']

        if name not in riders:
            riders[name] = {
                    'name': name,
                    'pos': result['GC'],
                    'time': [result['GC-Time']],
                    'team': result['Team']
                    }
        else:
            riders[name]['time'].append(result['GC-Time'])
            riders[name]['pos'] = result['GC']

    print(riders)

    with open('out.json', 'w') as handle:
        json.dump(riders, handle)


def main():
    parser = argparse.ArgumentParser(description='Download pcs data.')

    parser.add_argument('source', help='download or try local data', nargs='?',
                        choices=('download', 'local'), default='local')
    parser.add_argument('--max-stage', help='last stage to download',
                        action='store', type=int, default=21)
    parser.add_argument('--race', help='race to get',
                        action='store', default='giro-d-italia')
    parser.add_argument('--year', help='year to get',
                        action='store', type=int, default=2018)
    parser.add_argument('--directory', help='directory to store the files',
                        action='store', default='.')
    args = parser.parse_args()

    print(args)

    riders_results = []

    for stage in range(1, args.max_stage+1):
        filename = '{a.race}-{a.year}-stage-{stage:02d}.html'.format(a=args, stage=stage)
        path = os.path.join(args.directory, filename)
        url = BASE_URL.format(race=args.race, year=args.year, stage=stage)
        print(url, filename, args.source)

        get(url, filename, args.source)

        riders_results += process(filename, stage)

    print(riders_results)

    jsonify(riders_results)

    for team in set(x['Team'] for x in riders_results):
        print(team)




if __name__ == '__main__':
    main()

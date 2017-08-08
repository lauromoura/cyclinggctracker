#!/usr/bin/env python

'''Download multipage PCS ranking data'''

import sys
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="")
    parser.parse_args()


if __name__ == '__main__':
    main()

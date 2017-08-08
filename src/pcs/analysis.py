#!/usr/bin/env python

'''Parse PCS TT ranking data'''

import sys
import pandas as pd
import csv


def main(argv=None):
    '''Argv[1] is the source file'''
    if argv is None:
        argv = sys.argv

    df = pd.read_csv(argv[1], )

    df_agg = df.groupby(['Team',])
    res = df_agg.apply(lambda x: x.nlargest(6, columns=['Points'])['Points'].sum())
    print(res.sort_values(ascending=False))
    print(df_agg.size().sort_values(ascending=False))

if __name__ == '__main__':
    main()

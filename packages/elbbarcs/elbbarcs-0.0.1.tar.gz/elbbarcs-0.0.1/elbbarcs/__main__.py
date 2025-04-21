#!/usr/bin/env python3

import unicodedata
from collections import defaultdict
import math
from elbbarcs import Estimator

def main():
    import argparse, sys
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', action='store')
    parser.add_argument('-d', '--digraph', action='store', default='')
    parser.add_argument('-t', '--tiles', type=int, default=100)
    parser.add_argument('-b', '--buckets', type=int, default=12)
    args = parser.parse_args()

    e = Estimator(args.digraph, args.tiles, args.buckets)
    s = e.estimate(args.infile)
    e.table(s)

if __name__ == '__main__':
    main()

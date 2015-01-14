#! /usr/bin/env python3
# Created on Jan 13 2015

import ast

__author__ = "Jinglei Ren"
__copyright__ = "Copyright (c) 2015 Jinglei Ren"
__email__ = "jinglei@ren.systems"


import data

def main():
    results_file = open(data.RESULTS_FILE, 'r')
    results = ast.literal_eval(results_file.read())
    is_header = True
    for workload, aofs in iter(sorted(results.items())):
        if is_header:
            print('#', end='\t')
            [print(aof + ' (mean stderr)', end='\t')
                    for aof in sorted(aofs.keys())]
            print()
            is_header = False
        print(workload, end='\t')
        for aof, runs in iter(sorted(aofs.items())):
            [print(number, end='\t') for number in data.calculate(runs)]
        print()

if __name__ == '__main__':
    main()


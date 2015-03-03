#! /usr/bin/env python3
# Created on Mar. 2 2015

import sys
import os
import io
from os import path

__author__ = "Jinglei Ren"
__copyright__ = "Copyright (c) 2015 Jinglei Ren"
__email__ = "jinglei@ren.systems"

def main():
    if len(sys.argv) != 3:
        print('Usage:', sys.argv[0], '[training set dir]', '[output file]')
        exit(-1)

    data_dir = sys.argv[1]

    output = io.StringIO()
    m = 0;
    n = 0;
    l = 0;
    for file_name in os.listdir(data_dir):
        path = os.path.join(data_dir, file_name)
        if not os.path.isfile(path): continue

        in_file = io.open(path, 'r')
        movie = int(in_file.readline().strip().rstrip(':'))
        assert movie == int(os.path.splitext(file_name)[0].split('_')[1])
        if movie > n: n = movie

        print('Processing Movie#', movie)
        for line in in_file:
            line = line.strip()
            user, rate, date = line.split(',')
            user = int(user)
            rate = int(rate)
            if user > m: m = user
            l += 1
            print(user, movie, rate, file=output)
            
        in_file.close()

    out_file = io.open(sys.argv[2], 'w')
    print('%%MatrixMarket matrix coordinate integer general', file=out_file)
    print(m, n, l, file=out_file)
    print(output.getvalue(), file=out_file)

    out_file.close()
    output.close()

if __name__ == '__main__':
    main()


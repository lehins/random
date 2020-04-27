#! /usr/bin/env nix-shell
#! nix-shell -i python3 -p python3 python37Packages.pandas

# Usage: compare.py <reference.csv> <results.csv>
#
# Compares the benchmark results in the second argument with those in the first
# argument. Outputs a comparison of those rows where the results differ
# significantly.

import pandas as pd

# Threshold for the speedup or slowdown factor
SIGNIFICANT = 0.2

if __name__ == '__main__':
    from sys import argv

    ref = pd.read_csv(argv[1])
    res = pd.read_csv(argv[2])
    comp = pd.merge(ref, res, on='Name', how='outer', validate='one_to_one', suffixes=('_ref', '_res'))

    speedup_col = 'Speedup_rel'
    comp[speedup_col] = (comp['Mean_ref'] - comp['Mean_res']) / comp['Mean_ref']

    cols = ['Name', 'Mean_ref', 'Mean_res', speedup_col]
    print('SLOWER')
    print(comp[comp[speedup_col] < - SIGNIFICANT].loc[:, cols].to_string(index=False))

    print('\nFASTER')
    print(comp[comp[speedup_col] > SIGNIFICANT].loc[:, cols].to_string(index=False))

# -*- coding: utf-8 -*-
"""
netconv CLI interface

Authors:  Chia-Hung Yang <yang.chi@husky.neu.edu>
          Leonardo Torres <leo@leotrs.com>
          Stefan McCabe <mccabe.s@husky.neu.edu>
          Jean-Gabriel Young <jgyou@umich.edu>
"""
import netconv

formats = ['graphml', 'edgelist']

if __name__ == '__main__':
    # Compatibility checks
    import sys
    if sys.version_info[0] < 3:
        raise UserWarning("netconv is designed with python 3+ in mid.")

    # Interace proper
    import argparse as ap
    prs = ap.ArgumentParser(prog="netconv",
                            description=netconv.__desc__)
    prs.add_argument("--from", "--read", '-f', '-r',
                     type=str, default='graphml',
                     const='graphml', nargs='?',
                     choices=formats,
                     help='Origin graph format  (default: %(default)s).')
    prs.add_argument("--to", "--write", '-t', '-w',
                     type=str, default='edgelist',
                     const='edgelist', nargs='?',
                     choices=formats,
                     help='Origin graph format  (default: %(default)s).')
    prs.add_argument('--output', '-o', type=str,
                     help="Write output to OUTPUT instead of stdout.")
    prs.add_argument('--version', '-v', action='store_true',
                     help="Print version.")
    args = prs.parse_args()

    if args.version:
        print("netconv", netconv.__version__)
        print(netconv.__license__, "license.")
        print("Copyright (C) netconv team.")

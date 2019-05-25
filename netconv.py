# -*- coding: utf-8 -*-
"""
netconv CLI interface

Authors:  Chia-Hung Yang <yang.chi@husky.neu.edu>
          Leonardo Torres <leo@leotrs.com>
          Stefan McCabe <mccabe.s@husky.neu.edu>
          Jean-Gabriel Young <jgyou@umich.edu>
"""
import netconv

format_dict = {"graphml": {'graphml'},
               "sparse6": {'s6', 'g6'},
               "gexf": {'gexf'}}
formats = ['graphml', 'edgelist']

if __name__ == '__main__':
    # Compatibility checks
    import sys
    if sys.version_info[0] < 3:
        raise UserWarning("netconv is designed for python 3+.")

    # Interface proper
    from os import path
    import argparse as ap
    prs = ap.ArgumentParser(prog="netconv",
                            description=netconv.__desc__)
    prs.add_argument("-f", "--from", dest='from_',
                     type=str, default=None,
                     const='graphml', nargs='?',
                     choices=list(format_dict.keys()),
                     help='Origin graph format. Guessed from extension \
                           if not given as input.')
    prs.add_argument("-t", '--to', dest='to_',
                     type=str, default=None,
                     const='edgelist', nargs='?',
                     choices=list(format_dict.keys()),
                     help='Output graph format. Guessed from extension \
                           if not given as input.')
    prs.add_argument('input', type=str,
                     help='Input file.')
    prs.add_argument('--output', '-o', type=str, default=None,
                     help="Write output to OUTPUT instead of stdout.")
    prs.add_argument('--version', '-v', action='store_true',
                     help="Print version.")
    args = prs.parse_args()

    if args.version:
        print("netconv", netconv.__version__)
        print(netconv.__license__, "license.")
        print("Copyright (C) netconv team.")
        exit()

    # extension matching
    if args.from_ is None:
        ext = path.splitext(args.input)[1][1:]
        for ext_name, ext_aliases in format_dict.items():
            if ext in ext_aliases:
                args.from_ = ext_name

    if args.to_ is None and args.output is not None:
        ext = path.splitext(args.output)[1][1:]
        for ext_name, ext_aliases in format_dict.items():
            if ext in ext_aliases:
                args.to_ = ext_name

    # Checks on arguments
    if args.from_ is None:
        print("Input format unspecified.")
        exit()

    if args.to_ is None:
        print("Output format unspecified.")
        exit()


    print("Converting form", args.from_, 'to', args.to_)

    # graph = netconv.decode(args.from,a )
    # Output

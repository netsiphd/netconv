# -*- coding: utf-8 -*-
"""
netconv CLI interface

Authors:  Chia-Hung Yang <yang.chi@husky.neu.edu>
          Leonardo Torres <leo@leotrs.com>
          Stefan McCabe <mccabe.s@husky.neu.edu>
          Jean-Gabriel Young <jgyou@umich.edu>
"""
import netconv

format_dict = {"graphml":
                    {"ext": {'graphml'},
                     "ext_aliases": {'graphml'}},
               "sparse6":
                    {"ext": {'s6'},
                     "ext_aliases": {'s6', 'g6'}},
               "gexf":
                    {"ext": {'gexf'},
                     "ext_aliases": {'gexf'}},
               "edgelist":
                    {"ext": {'edgelist'},
                     "ext_aliases": {'el', 'edgelist', "edges"}}}


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
    prs.add_argument("--sep", '-s',
                     type=str, default=" ",
                     help='Separator.')
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
        for format_name, format_spec in format_dict.items():
            if ext in format_spec['ext_aliases']:
                args.from_ = format_name

    if args.to_ is None and args.output is not None:
        ext = path.splitext(args.output)[1][1:]
        for format_name, format_spec in format_dict.items():
            if ext in format_spec['ext_aliases']:
                args.to_ = format_name

    # Checks on arguments
    if args.from_ is None:
        print("Input format unspecified.")
        exit()

    if args.to_ is None:
        print("Output format unspecified.")
        exit()

    print("Converting form", args.from_, 'to', args.to_)

    # Decode
    # with open(args.input, 'r') as f:
    g = netconv.read(args.input, args.from_)


    #     def read(filename, fmt, *args, **kwargs):
    # with open(filename) as file:
    #     text = file.read()
    # return decode(text, fmt, *args, **kwargs)


    #     format_dict[args.from_]['decoder'](f.read(), delimiter=args.sep)

    # Encode
    if args.output is None:
        # stdout
        netconv.write(g, args.to_, sys.stdout)
        # print(format_dict[args.to_]['encoder'](g, delimiter=args.sep, attr=False))
    elif args.output:
        netconv.write(g, args.to_, args.output)


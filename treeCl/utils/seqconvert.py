#!/usr/bin/env python

# standard library
import argparse
import sys

# treeCl
import fileIO
from ..datastructs.seq import Seq
from ..errors import filecheck


def change_case(rec, case):
    if case.startswith('u'):
        rec.change_case('upper')
    else:
        rec.change_case('lower')


def sort(rec, scheme):
    if scheme == 'l':
        rec.sort_by_length()
    elif scheme == 'lr':
        rec.sort_by_length(reverse=False)
    elif scheme == 'n':
        rec.sort_by_name()
    elif scheme == 'nr':
        rec.sort_by_name(reverse=True)


def write(rec, outfile, to_format='phylip',
          interleaved=False, linebreaks=None,
          datatype='protein'):
    if to_format == 'fasta':
        rec.write_fasta(outfile, linebreaks=linebreaks)
    elif to_format == 'nexus':
        rec.write_nexus(outfile, datatype)
    elif to_format == 'phylip':
        rec.write_phylip(outfile, interleaved=interleaved,
                         linebreaks=linebreaks)


def parse_args():
    prog = fileIO.basename(sys.argv[0])
    desc = '{0}: Sequence file format converter'.format(prog.upper())
    f_choices = ['fasta', 'phylip']
    t_choices = ['fasta', 'nexus', 'phylip']
    c_choices = ['l', 'u', 'lower', 'upper']
    s_choices = ['n', 'l', 'nr', 'lr']
    d_choices = ['dna', 'protein']

    parser = argparse.ArgumentParser(prog=prog, description=desc)
    parser.add_argument('-i', '--infile', dest='infile', type=str,
                        help='Input filename', required=True)
    parser.add_argument('-o', '--outfile', dest='outfile', type=str,
                        default='stdout',
                        help='Output filename (\'stdout\' to write to screen(default))')
    parser.add_argument('-f', '--from', dest='fr', type=str,
                        default='fasta', choices=f_choices,
                        help='Input file format (this program doesn\'t guess; default=fasta)')
    parser.add_argument('-t', '--to', dest='to', type=str,
                        default='phylip', choices=t_choices,
                        help='Output file format (default=phylip)')
    parser.add_argument('-n', '--interleaved', dest='interleaved',
                        action='store_true',
                        help='Set phylip output to interleaved (default=sequential)')
    parser.add_argument('-s', '--sort', dest='sort',
                        choices=s_choices,
                        help=('Sort sequences by name (n) ([A-Z] order);\n'
                              'reverse by name (nr) ([Z-A] order);\n'
                              'by ungapped length (l) (long to short);\n'
                              'or reverse by ungapped length (lr) (short to long)\n'))
    parser.add_argument('-d', '--datatype', dest='datatype',
                        choices=d_choices, default='protein',
                        help='Datatype (optional) = \'dna\', \'protein\'')
    parser.add_argument('-l', '--linewidth', type=int,
                        help='Break lines up by length')
    parser.add_argument('-c', '--case', dest='case', type=str,
                        choices=c_choices, help='Change case of sequences')

    return parser.parse_args()


def main():
    args = parse_args()
    filecheck(args.infile)
    rec = Seq(args.infile, file_format=args.fr)
    if args.sort:
        sort(rec, args.sort)
    if args.case:
        change_case(rec, args.case)

    write(rec, args.outfile, args.to, args.interleaved,
          args.linewidth, args.datatype)


if __name__ == '__main__':
    sys.exit(main())

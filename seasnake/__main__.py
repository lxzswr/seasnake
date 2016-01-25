'''
This is the main entry point for SeaSnake.
'''
import argparse
import sys

from seasnake.parser import CodeConverter


def main():
    opts = argparse.ArgumentParser(
        description='Convert C++ code to Python.',
    )

    opts.add_argument(
        '-o', '--output',
        metavar='module',
        help='The name of the output module to write.',
    )

    opts.add_argument(
        '-s', '--stdout',
        help='The name of the output module to write.',
        action='store_true'
    )

    opts.add_argument(
        '-v', '--verbosity',
        action='count',
        default=0
    )

    opts.add_argument(
        '-I', '--include',
        dest='includes',
        metavar='/path/to/includes',
        help='A directory of includes',
        action='append',
        default=[]
    )

    opts.add_argument(
        '-D',
        dest='defines',
        metavar='SYMBOL',
        help='Preprocessor symbols to use',
        action='append',
        default=[]
    )

    opts.add_argument(
        'filename',
        metavar='file.cpp',
        help='The file(s) to compile.',
        nargs="+"
    )

    args = opts.parse_args()

    converter = CodeConverter('output', verbosity=args.verbosity)
    for filename in args.filename:
        converter.parse(
            filename,
            flags=[
                '-I%s' % inc for inc in args.includes
            ] + [
                '-D%s' % define for define in args.defines
            ]
        )

    converter.diagnostics(sys.stderr)

    if args.output:
        with open('%s.py' % args.output, 'w') as out:
            converter.output('%s.py' % args.output, out)
    else:
        if args.stdout:
            converter.output_all(sys.stdout)
        else:
            print("Can't output multiple files (yet!)")


if __name__ == '__main__':
    main()

from os import path
from sys import argv, stderr
from mbnf_scanner import MbnfScanner
from mbnf_parser import MbnfParser
from parser_generator import ParserGenerator

HELP = '''
USAGE:
llgen -h
Produce a list of valid command-line arguments.

llgen -t <file name>
Produce an LL(1) parse table in YAML format for the input grammar contained in <file name>

llgen -s <file name>
Print the following sets for the input grammar in <file name>
1. the productions, as recognized by the parser,
2. the FIRST sets for each grammar symbol,
3. the FOLLOW sets for each nonterminal, and
4. the FIRST+ sets for each production.
'''


def get_parser_generator(file_name):
    scanner = MbnfScanner()
    tokens = scanner.scan(argv[2])
    parser = MbnfParser(tokens)
    parser.parse()

    return ParserGenerator(parser)


def main():
    if len(argv) >= 2 and argv[1] == '-h':
        print(HELP)
    elif len(argv) >= 3 and argv[1] == '-t':
        if not path.exists(argv[2]):
            raise IOError('Could not find the file {}.'.format(argv[2]))
        pg = get_parser_generator(argv[2])
        pg.print_yaml_ll1_table()

    elif len(argv) >= 3 and argv[1] == '-s':
        if not path.exists(argv[2]):
            raise IOError('Could not find the file {}.'.format(argv[2]))
            pg = get_parser_generator(argv[2])
            pg.print_ll1_sets()

if __name__ == '__main__':
    try:
        main()
    except (IOError, RuntimeError) as e:
        print(e, file=stderr)
        exit(1)
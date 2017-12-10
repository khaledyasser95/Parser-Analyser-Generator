from mbnf_scanner import MbnfScanner
from mbnf_parser import MbnfParser
from parser_generator import ParserGenerator


s = MbnfScanner()
tokens = s.scan('grammars/CEG-RR')
print(tokens)
p = MbnfParser(tokens)
p.parse()
pg = ParserGenerator(p)
pg.print_ll1_sets()
pg.print_yaml_ll1_table()


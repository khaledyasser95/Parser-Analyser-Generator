grammar = """
# METHOD_BODY = STATEMENT_LIST
# STATEMENT_LIST = STATEMENT |    STATEMENT_LIST    STATEMENT
# STATEMENT =      DECLARATION
| IF
| WHILE
| ASSIGNMENT
# DECLARATION = PRIMITIVE_TYPE 'id' ';'
# PRIMITIVE_TYPE = 'int' | 'float'
# IF = 'if' '(' EXPRESSION ')' '{' STATEMENT '}' 'else' '{' STATEMENT '}'
# WHILE = 'while' '(' EXPRESSION ')' '{' STATEMENT '}'
# ASSIGNMENT = 'id' '=' EXPRESSION ';'
# EXPRES
SION =    SIMPLE_EXPRESSION
| SIMPLE_EXPRESSION 'relop' SIMPLE_EXPRESSION
# SIMPLE_EXPRESSION = TERM | SIGN TERM | SIMPLE_EXPRESSION 'addop' TERM
# TERM = FACTOR | TERM 'mulop' FACTOR
"""
_term = 't'
_nterm = 'n'
def fix_lines(gstr):
    """
    This funtion takes input grammar string and outputs grammar 
    string where each grammar rule is represented in only one line
    """
    _input = list(filter(None, gstr.split("\n")))
    i = 0
    _output = []
    while i < len(_input):
        line  = _input[i].strip()
        if line[0] == '#':
            _output.append(line)
        else:
            _output[-1] = " ".join([_output[-1], line])
        i += 1
    return "\n".join(_output)

def __parse_rules(rules):
    """
        This function takes rules string and return array of
        array list representing terminals and nonterminals list
    """
    output = [[]]
    for word in list(filter(None, rules.split(" "))):
        if word[0] == "'":
            output[-1].append((word[1:-1],_term))
        elif word[0] == '|':
            output.append([])
        else:
            output[-1].append((word,_nterm))

    return output

def get_grammar(gfix):
    """
        This function takes grammar string, each line should be:
            1- each grammar rule is represented by one line,
            2- each grammar rule should start with #
            3- All terminal are between quotes
            4- We don't fucken handle any fucken god damn user error
    """
    g = {}
    for line in gfix.split("\n"):
        name = line[1:line.find("=")].strip()
        rules = line[line.find("=") + 1:]
        g[name] = __parse_rules(rules)
    return g

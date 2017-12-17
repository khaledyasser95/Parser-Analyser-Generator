from collections import namedtuple

SEMICOLON = 0
DERIVES = 1
ALSODERIVES = 2
EPSILON = 3
EPSILON = 4
SYMBOL = 5
EOF = 6

Token = namedtuple('Token', ['lexeme', 'type'])


class MbnfScanner:
    def __init__(self):
        pass

    def get_type(self, lexeme):
        if lexeme == ';':
            return Token(lexeme=lexeme, type=SEMICOLON)
        elif lexeme == ':':
            return Token(lexeme=lexeme, type=DERIVES)
        elif lexeme == '|':
            return Token(lexeme=lexeme, type=ALSODERIVES)
        elif lexeme == 'EPSILON' or lexeme == 'epsilon' or lexeme == 'Epsilon':
            return Token(lexeme=lexeme, type=EPSILON)
        else:
            return Token(lexeme=lexeme, type=SYMBOL)

    def scan(self, file_name):
        file_content = open(file_name).read()
        i = 0
        tokens = []
        token = ''
        while i < len(file_content):
            c = file_content[i]
            old = file_content[i]
            if c == ' ' or c == '\t' or c == '\n':
                if len(token) > 0:
                    tokens.append(self.get_type(token))
                    token = ''
            elif c == ':' or c == '|' or c == ';':
                if len(token) > 0:
                    tokens.append(self.get_type(token))

                tokens.append(self.get_type(c))
                token = ''
            # remove comments
            elif c == '/':
                if len(token) > 0:
                    tokens.append(self.get_type(token))
                    token = ''
                while c != '\n':
                    i += 1
                    c = file_content[i]
            else:
                token += c

            i += 1

        if len(token) > 0:
            tokens.append(self.get_type(token))

        return tokens
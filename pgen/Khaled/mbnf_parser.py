from collections import namedtuple

from mbnf_scanner import SEMICOLON, Token, EOF, ALSODERIVES, EPSILON

from mbnf_scanner import SYMBOL
from mbnf_scanner import DERIVES


'''
LL(1) Grammar

00 Grammar -> ProductionList

01 ProductionList -> SYMBOL RightHandSide SEMICOLON ProductionList
02                 | epsilon

03 RightHandSide -> DERIVES SymbolList RightHandSide'

04 RightHandSide' -> ALSODERIVES SymbolList RightHandSide'
05                 | epsilon

06 SymbolList -> SYMBOL SymbolList
07             | EPSILON
08             | epsilon
'''

Production = namedtuple('Production', ('lhs', 'rhs'))


class MbnfParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = 0
        self.word = None
        self.productions = []
        self.int_to_sym = {}
        self.sym_to_int = {}
        self.goal = None
        self.epsilon = None
        self.terminals = None
        self.non_terminals = set()

    def next_word(self):
        """
        Get the next Token
        :return: next Token object
        """
        if self.token_idx < len(self.tokens):
            word = self.tokens[self.token_idx]
            self.token_idx += 1
            return word

        return Token(lexeme=None, type=EOF)

    def parse_sym(self):
        """
        Parse all the symbols and category them into terminals, non-terminals
        epsilon and goal
        """
        # Map symbols to integers
        idx = 0
        for i in range(0, len(self.tokens)):
            if self.tokens[i].type == SYMBOL or self.tokens[i].type == EPSILON:
                if self.tokens[i].lexeme not in self.sym_to_int:
                    self.sym_to_int[self.tokens[i].lexeme] = idx
                    self.int_to_sym[idx] = self.tokens[i].lexeme
                    if self.tokens[i].type == EPSILON:
                        self.epsilon = idx
                    idx += 1

        # Get non-terminals
        for i in range(0, len(self.tokens)):
            if self.tokens[i].type == DERIVES:
                self.non_terminals.add(self.sym_to_int[self.tokens[i - 1].lexeme])

        # Get terminals
        self.terminals = set(self.int_to_sym) - self.non_terminals
        self.terminals -= {self.epsilon}

        # Get goal
        i = 0
        temp = set(self.non_terminals)
        while i < len(self.tokens):
            if self.tokens[i].type == DERIVES:
                while i < len(self.tokens) and self.tokens[i].type != SEMICOLON:
                    if self.tokens[i].type == SYMBOL:
                        idx = self.sym_to_int[self.tokens[i].lexeme]
                        if idx in self.non_terminals and idx in temp:
                            temp.remove(idx)

                    i += 1

            i += 1

        for goal in temp:
            self.goal = goal
        self.goal = self.int_to_sym[0]

    def parse(self):
        """
        Recursive descent LL(1) parser
        """
        self.parse_sym()
        self.word = self.next_word()
        self.grammar()
        if self.word.type != EOF:
            raise RuntimeError('Syntax Error')

    def grammar(self):
        """
        Parse from Grammar
        Grammar[00]
        """
        self.p_list()

    def p_list(self):
        """
        Parse from ProductionList
        """
        # Grammar[01]
        if self.word.type == SYMBOL:
            lhs_symbol = self.sym_to_int[self.word.lexeme]
            self.word = self.next_word()
            rhs_symbols = []
            self.rhs(lhs_symbol, rhs_symbols)
            if self.word.type == SEMICOLON:
                self.word = self.next_word()
                self.p_list()
            else:
                raise RuntimeError('Syntax Error')
        # Grammar[02]
        elif self.word.type == EOF:
            return
        else:
            raise RuntimeError('Syntax Error')

    def rhs(self, lhs_symbol, rhs_symbols):
        """
        Parse from RightHandSide
        :param lhs_symbol: symbols at left hand side
        :param rhs_symbols: symbols at right hand side
        """
        # Grammar[03]
        if self.word.type == DERIVES:
            self.word = self.next_word()
            self.sym_list(rhs_symbols)
            self.productions.append(Production(lhs=lhs_symbol, rhs=rhs_symbols))
            next_rhs_symbols = []
            self.rhs_prime(lhs_symbol, next_rhs_symbols)
        else:
            raise RuntimeError('Syntax Error')

    def rhs_prime(self, lhs_symbol, rhs_symbols):
        """
        Parse from RightHandSide'
        :param lhs_symbol: symbols at left hand side
        :param rhs_symbols: symbols at right hand side
        """
        # Grammar[04]
        if self.word.type == ALSODERIVES:
            if len(rhs_symbols) > 0:
                self.productions.append(Production(lhs=lhs_symbol, rhs=rhs_symbols))
                rhs_symbols = []

            self.word = self.next_word()
            self.sym_list(rhs_symbols)
            self.rhs_prime(lhs_symbol, rhs_symbols)
        # Grammar[05]
        elif self.word.type == SEMICOLON:
            if len(rhs_symbols) > 0:
                self.productions.append(Production(lhs=lhs_symbol, rhs=rhs_symbols))
        else:
            raise RuntimeError('Syntax Error')

    def sym_list(self, rhs_symbols):
        """
        Parse from SymbolList
        :param rhs_symbols: symbols at right hand side
        """
        # Grammar[06]
        if self.word.type == SYMBOL:
            rhs_symbols.append(self.sym_to_int[self.word.lexeme])
            self.word = self.next_word()
            self.sym_list(rhs_symbols)
        # Grammar[07]
        elif self.word.type == EPSILON:
            rhs_symbols.append(self.sym_to_int[self.word.lexeme])
            self.word = self.next_word()
        # Grammar[08]
        elif self.word.type == SEMICOLON or self.word.type == ALSODERIVES:
            return
        else:
            raise RuntimeError('Syntax Error')
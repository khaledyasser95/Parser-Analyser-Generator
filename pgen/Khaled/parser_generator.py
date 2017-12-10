from copy import deepcopy


class ParserGenerator:
    def __init__(self, parser):
        self.productions = parser.productions
        self.int_to_sym = parser.int_to_sym
        self.sym_to_int = parser.sym_to_int
        self.goal = parser.goal
        self.epsilon = parser.epsilon
        self.terminals = parser.terminals
        self.non_terminals = parser.non_terminals
        self.eof = -1
        self.error = -2
        self.int_to_sym[self.eof] = '<EOF>'
        self.int_to_sym[self.error] = '--'
        self.sym_to_int['<EOF>'] = self.eof
        self.sym_to_int['--'] = self.error

        self.first = self.get_first()
        self.follow = self.get_follow(self.first)
        self.first_plus = self.get_first_plus(self.first, self.follow)
        self.table = self.get_ll1_table(self.first_plus)

    def get_first(self):
        first = {terminal: {terminal} for terminal in self.terminals}
        first[self.eof] = {self.eof}
        first[self.epsilon] = {self.epsilon}
        first.update({nterminal: set() for nterminal in self.non_terminals})
        changed = True
        while changed:
            old_first = deepcopy(first)

            for lhs, rhs in self.productions:
                rhs_set = first[rhs[0]] - {self.epsilon}
                i = 0
                while self.epsilon in first[rhs[i]] and i < len(rhs) - 1:
                    rhs_set |= first[rhs[i + 1]] - {self.epsilon}
                    i += 1

                if i == len(rhs) - 1 and self.epsilon in first[rhs[-1]]:
                    rhs_set |= {self.epsilon}

                first[lhs] |= rhs_set

            changed = self.is_changing(first, old_first)

        return first

    def get_follow(self, first):
        follow = {nterminal: set() for nterminal in self.non_terminals}
        follow[self.goal] = {self.eof}

        changed = True
        while changed:
            old_follow = deepcopy(follow)

            for lhs, rhs in self.productions:
                trailer = set(follow[lhs])
                for i in reversed(list(range(0, len(rhs)))):
                    beta = rhs[i]
                    if beta in self.non_terminals:
                        follow[beta] |= trailer

                        if self.epsilon in first[beta]:
                            trailer |= first[beta] - {self.epsilon}
                        else:
                            trailer = set(first[beta])
                    else:
                        trailer = {beta}

            changed = self.is_changing(follow, old_follow)

        return follow

    def is_changing(self, new_sets, old_sets):
        for key, val in new_sets.items():
            if len(val ^ old_sets[key]) > 0:
                return True

        return False

    def get_first_plus(self, first, follow):
        first_plus = {}
        for i in range(0, len(self.productions)):
            first_plus[i] = set()
            rhs = self.productions[i].rhs
            for symbol in rhs:
                first_plus[i] |= first[symbol]
                if self.epsilon not in first[symbol]:
                    break

                if symbol == rhs[-1]:
                    first_plus[i] |= follow[self.productions[i].lhs]

        return first_plus

    def get_ll1_table(self, first_plus):
        table = {}
        for nterminal in self.non_terminals:
            table[nterminal] = {terminal: self.error for terminal in self.terminals}
            table[nterminal][self.eof] = self.error

        for i, fp_set in first_plus.items():
            lhs = self.productions[i].lhs
            for terminal in fp_set:
                if terminal == self.epsilon:
                    continue

                if table[lhs][terminal] != self.error:
                    error_msg = self.get_error_production(lhs)
                    raise RuntimeError('Illegal LL(1) grammar: {}'.format(error_msg))

                table[lhs][terminal] = i

        return table

    def get_error_production(self, lhs):
        error_productions = [p for p in self.productions if p.lhs == lhs]
        error_msg = self.int_to_sym[error_productions[0].lhs] + ' : '
        str_rhs = []
        for p in error_productions:
            symbols = [self.int_to_sym[symbol] for symbol in p.rhs]
            str_rhs.append(' '.join(symbols))

        error_msg += ' | '.join(str_rhs)
        return error_msg

    def print_yaml_ll1_table(self):
        str_terminals = [self.int_to_sym[t] for t in self.terminals]
        print(('terminals: [{}]'.format(', '.join(str_terminals))))

        str_nterminals = [self.int_to_sym[nt] for nt in self.non_terminals]
        print(('non-terminals: [{}]'.format(', '.join(str_nterminals))))

        print(('eof-marker: {}'.format(self.int_to_sym[self.eof])))
        print(('error-marker: {}'.format(self.int_to_sym[self.error])))
        print(('start-symbol: {}'.format(self.int_to_sym[self.goal])))

        print()
        print('productions:')
        for i in range(0, len(self.productions)):
            lhs, rhs = self.productions[i]
            symbols = [self.int_to_sym[symbol] for symbol in rhs if symbol != self.epsilon]
            print(('  {}: {{{}: [{}]}}'.format(i, self.int_to_sym[lhs], ', '.join(symbols))))

        print()
        print('table:')
        for nt, row in self.table.items():
            str_row = []
            for t in self.terminals:
                idx = str(row[t]) if row[t] >= 0 else self.int_to_sym[self.error]
                str_row.append(self.int_to_sym[t] + ': ' + idx)

            str_eof_idx = str(row[self.eof]) if row[self.eof] > 0 else self.int_to_sym[self.error]
            str_row.append(self.int_to_sym[self.eof] + ': ' + str_eof_idx)
            print(('  {}: {{{} }}'.format(self.int_to_sym[nt], ', '.join(str_row))))

    def print_ll1_sets(self):
        print('productions:')
        for i in range(0, len(self.productions)):
            lhs, rhs = self.productions[i]
            symbols = [self.int_to_sym[symbol] for symbol in rhs]
            print(('  {}: {{{}: [{}]}}'.format(i, self.int_to_sym[lhs], ', '.join(symbols))))

        print('first:')
        for symbol, symbol_set in self.first.items():
            if symbol is None:
                continue

            symbols = [self.int_to_sym[s] for s in symbol_set]
            print(('  {}: {{{}}}'.format(self.int_to_sym[symbol], ', '.join(symbols))))

        print('follow:')
        for nt, nt_set in self.follow.items():
            symbols = [self.int_to_sym[s] for s in nt_set]
            print(('  {}: {{{}}}'.format(self.int_to_sym[nt], ', '.join(symbols))))

        print('first+:')
        for p_idx, symbol_set in self.first_plus.items():
            lhs, rhs = self.productions[p_idx]
            symbols = [self.int_to_sym[symbol] for symbol in rhs if symbol != self.epsilon]
            str_p = '{{{}: [{}]}}'.format(self.int_to_sym[lhs], ', '.join(symbols))
            symbols = [self.int_to_sym[s] for s in symbol_set]
            print((' {}: {{{}}}'.format(str_p, ', '.join(symbols))))
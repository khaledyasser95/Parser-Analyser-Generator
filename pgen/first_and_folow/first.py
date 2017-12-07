def compute_first_N(non_terminal, Grammar):
    # import pdb
    # pdb.set_trace()
    if non_terminal not in Grammar:
        return -1
    for x in Grammar[non_terminal]:
        # if the first is terminal so push it in the first dict
        # else go to the production of this non-terminal
        token, type = Grammar.get(non_terminal)[x][0]
        if type == 't':
            return token
        elif type == 'n':
            compute_first_N(token, Grammar)


def compute_First(Grammar):
    # here is a dictionary of non-terminals and the first of each one
    first = {}

    # this shit is used to reverse the dict keys so that we could iterate reversely on it in first computation
    keys = Grammar.keys()
    keyz = []

    for x in keys:
        keyz.append(x)

    i = 0
    for x in range(int(len(keyz) / 2)):
        temp = keyz[i]
        keyz[i] = keyz[len(keyz) - i - 1]
        keyz[len(keyz) - i - 1] = temp
        i += 1

    # we will loop on the non-terminals in Grammar
    for x in keyz:
        # we will loop on all productions in the same non-terminal
        for y in Grammar[x]:
            # take the first tuple in each list
            token, type = y[0]
            print("Token: ", token)
            print("Type: ", type)

            # if the first is terminal so push it in the first dict
            # else go get the first of this non-terminal
            if type == 't':
                if x not in first:
                    first.update({x: []})
                    first[x].append(token)
                elif (x in first) and (token not in first[x]):
                    first[x].append(token)
            elif type == 'n':
                if token in first:
                    if x not in first:
                        first.update({x: first[token]})
                    elif x in first:
                        #this is to add only the first that doesn't exist in first[x] and remove duplicates
                        for z in first[token]:
                            print("First of token: ", first[token])
                            if z not in first[x]:
                                first[x] = first[x] + [z]

                else:
                    if token != x:
                        first_of_N = compute_first_N(token, Grammar)
                        if first_of_N != -1:
                            first[x].append(first_of_N)
                        else:
                            print("Error in NON-TERMINAL ", x, " the NON-TERMINAL ", token, " not in the Grammar")
            print("The first dict: ", first)
    return first


Grammar = {
    'METHOD_BODY': [
        [
            ('STATEMENT_LIST', 'n')
        ]
    ],
    'STATEMENT_LIST': [
        [
            ('STATEMENT', 'n')
        ],
        [
            ('STATEMENT_LIST', 'n'),
            ('STATEMENT', 'n')
        ],
        [
            (None, 't')
        ]
    ],
    'STATEMENT': [
        [
            ('DECLARATION', 'n')
        ],
        [
            ('IF', 'n')
        ],
        [
            ('WHILE', 'n')
        ],
        [
            ('ASSIGNMENT', 'n')
        ]
    ],
    'DECLARATION': [
        [
            ('PRIMITIVE_TYPE', 'n'),
            ('id', 't'),
            (';', 't')
        ]
    ],
    'PRIMITIVE_TYPE': [
        [
            ('int', 't')
        ],
        [
            ('float', 't')
        ]
    ],
    'IF': [
        [
            ('if', 't'),
            ('(', 't'),
            ('EXPRESSION', 'n'),
            (')', 't'),
            ('{', 't'),
            ('STATEMENT', 'n'),
            ('}', 't'),
            ('else', 't'),
            ('{', 't'),
            ('STATEMENT', 'n'),
            ('}', 't'),
        ]
    ],
    'WHILE': [
        [
            ('while', 't'),
            ('(', 't'),
            ('EXPRESSION', 'n'),
            (')', 't'),
            ('{', 't'),
            ('STATEMENT', 'n'),
            ('}', 't')
        ]
    ],
    'ASSIGNMENT': [
        [
            ('id', 't'),
            ('=', 't'),
            ('EXPRESSION', 'n'),
            (';', 't')
        ]
    ]
}

compute_First(Grammar)

'''
#if the non-terminal has an epsilon in the first and there exists non-terminals after this one
                if None in first[token]:
                  for z in Grammar[x][y]:
                      token, type = z

                      if token in first:
                          if x not in first:
                              first.update({x: first[token]})
                          elif x in first:
                              # this is to add only the first that doesn't exist in first[x] and remove duplicates
                              for w in first[token]:
                                  if z not in first[x]:
                                      first[x] = first[x] + [w]

                      else:
                          if token != x:
                              first_of_N = compute_first_N(token, Grammar)
                              if first_of_N != -1:
                                  first[x].append(first_of_N)
                              else:
                                  print("Error in NON-TERMINAL ", x, " the NON-TERMINAL ", token, " not in the Grammar")

                      if None not in first[z]:
                          continue
'''
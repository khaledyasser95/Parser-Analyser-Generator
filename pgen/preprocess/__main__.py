from pgen.preprocess.preprocessor import *

lines = []
while True:
    line = input()
    if line:
        lines.append(line)
    else:
        break
i = '\n'.join(lines)
print(get_grammar(fix_lines(i)))

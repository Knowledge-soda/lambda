import lexer
import parser


def evaluate_term(text, mode=0):
    stream = lexer.tokenize(text)
    par = parser.ParserLL1(stream)
    term = parser.term(par)
    term.desugar()
    term.debrujin(())
    changed = True
    while changed:
        text = "= {}".format(term)
        if mode == 1:
            print(text)
        elif mode == 2:
            try:
                input(text)
            except KeyboardInterrupt:
                print()
                break
        term, changed = term.reduce()
    if not mode:
        print("= {}".format(term))

import argparse

import lexer
import parser
from abstract import Program, Test
from errors import LambdaError


def nice_version(term):
    newterm = term.clone()
    free = set()
    newterm.get_free(free)
    newterm.bruijn((), free)
    newterm.resugar()
    return newterm


def evaluate_term(term, mode=0):
    term.desugar()
    term.debruijn(())
    changed = True
    while changed:
        text = "-> {}".format(nice_version(term))
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
        print("-> {}".format(nice_version(term)))
    return term


def full_reduce(term):
    term.desugar()
    term.debruijn(())
    changed = True
    while changed:
        term, changed = term.reduce()
    return term


def execute_program(text, strict=False, sugar=True):
    stream = lexer.tokenize(text, strict)
    par = parser.ParserLL1(stream)
    prog = parser.program(par, sugar)
    for line in prog.get_singles():
        if isinstance(line, Test):
            print(line)
            print(line.test())
        else:
            print("{} ->".format(line))
            res = full_reduce(line)
            print("-> {}".format(nice_version(res)))
    return prog


def repl(strict=False, sugar=True, mode=2, program=None):
    if program is None:
        program = Program()
    while True:
        try:
            text = input("λ> ")
        except KeyboardInterrupt:
            print()
            break
        if not text:
            continue
        try:
            stream = lexer.tokenize(text, strict)
            par = parser.ParserLL1(stream)
            parser.line(par, program, sugar)
        except LambdaError as err:
            print(err)
            continue
        term = program.get_last()
        if isinstance(term, Test):
            print(term.test())
        elif term is not None:
            result = evaluate_term(term, mode)
            short = str(nice_version(result.decompile(program)))
            if str(result) != short and short != text:
                print("= {}".format(short))


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "filename", nargs="?",
        help="if missing will enter REPL mode")
    argparser.add_argument(
        "-s", "--strict", action="store_true",
        help="enforce format vN for variable names")
    argparser.add_argument(
        "-n", "--nosugar", action="store_true",
        help="disable syntatic sugar e.g. xy.T")
    argparser.add_argument(
        "-i", "--interactive", action="store_true",
        help="activates REPL shell after running program")
    mode_group = argparser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "-w", "--wait", action="store_true",
        help="REPL only, when evaluating term wait user input after every step"
    )
    mode_group.add_argument(
        "-p", "--print", action="store_true",
        help="REPL only, print every step (without stopping)")
    args = argparser.parse_args()

    if args.wait:
        mode = 2
    elif args.print:
        mode = 1
    else:
        mode = 0

    if args.filename:
        with open(args.filename, "r") as file:
            text = file.read()
        prog = execute_program(text, args.strict, not args.nosugar)
        if args.interactive:
            repl(args.strict, not args.nosugar, mode, prog)
    else:
        repl(args.strict, not args.nosugar, mode)

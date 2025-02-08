import lexer
import parser


def parse_term(text):
    stream = lexer.tokenize(text)
    par = parser.ParserLL1(stream)
    return parser.term(par)

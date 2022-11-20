from ply.lex import *

# list of token names
tokens = (
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
)

# regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer:Lexer = lex()


def tokenize(data: str) -> list[LexToken]:
    lexer:Lexer = lex()
    lexer.input(data)
    tokens = []
    while True:
        tok: LexToken = lexer.token()
        if not tok:
            break  # No more input
        tokens.append(tok)
    return tokens


def yieldtokenize(data: str) -> list[LexToken]:
    lexer:Lexer = lex()
    lexer.input(data)
    tok: LexToken = lexer.token()
    while tok:
        yield tok
        tok = lexer.token()


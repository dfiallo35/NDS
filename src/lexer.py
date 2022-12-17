from sly import Lexer

class CalcLexer(Lexer):
    tokens = { NAME, NUMBER }
    ignore = ' \t'
    literals = { '=', '+', '-', '*', '/', '(', ')' }


    # Tokens
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER = r'\d+'

    def NUMBER(self, t):
        t.value = int(t.value)
        return t
    
    

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1





class CalcLexer_1(Lexer):
    # Set of token names.   This is always required
    tokens = { NUMBER, ID, WHILE, IF, ELSE, PRINT,
               PLUS, MINUS, TIMES, DIVIDE, ASSIGN,
               EQ, LT, LE, GT, GE, NE }


    literals = { '(', ')', '{', '}', ';' }

    # String containing ignored characters
    ignore = ' \t'

    # Regular expression rules for tokens
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    EQ      = r'=='
    ASSIGN  = r'='
    LE      = r'<='
    LT      = r'<'
    GE      = r'>='
    GT      = r'>'
    NE      = r'!='

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    # Identifiers and keywords
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE
    ID['print'] = PRINT

    ignore_comment = r'\#.*'

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1

if __name__ == '__main__':
    data = '''
# Counting
x = 0;
while (x < 10) {
    print x:
    x = x + 1;
}
'''
    lexer = CalcLexer_1()
    for tok in lexer.tokenize(data):
        print(tok)
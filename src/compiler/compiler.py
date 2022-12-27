from sly import Lexer, Parser

class NDSLexer(Lexer):
    tokens = {'NATION', 'PROVINCE', 'SEA', 'NEUTRAL', 'EVENT', 'DISTRIBUTION',
            'NAME',
            'NUMBER',
            'ASSIGN', 'LINEEND', 'COMMA',
            'LPAREN', 'RPAREN', 'LBRAKET', 'RBRAKET', 'LKEY', 'RKEY',
            'FOR', 'WHILE', 'IF', 'ELSE',
            'GREATER', 'LESS', 'XPLUS', 'XMINUS',
            'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS'}
    ignore = ' \t'


    #ELEMENTS
    NATION= 'nation\s+'
    def NATION(self, t):
        t.value = str(t.value).strip()
        return t
    
    PROVINCE= r'province\s+'
    def PROVINCE(self, t):
        t.value = str(t.value).strip()
        return t
    
    SEA= r'sea\s+'
    def SEA(self, t):
        t.value = str(t.value).strip()
        return t
    
    NEUTRAL= r'neutral\s+'
    def NEUTRAL(self, t):
        t.value = str(t.value).strip()
        return t
    
    EVENT= r'event\s+'
    def EVENT(self, t):
        t.value = str(t.value).strip()
        return t
    
    DISTRIBUTION= r'distribution\s+'
    def DISTRIBUTION(self, t):
        t.value = str(t.value).strip()
        return t
    
    #PARAMETERS
    #todo: add parameters if needed


    #LOOPS
    FOR= r'for\s+'
    def FOR(self, t):
        t.value = str(t.value).strip()
        return t
    
    WHILE= r'while\s+'
    def WHILE(self, t):
        t.value = str(t.value).strip()
        return t
    
    #CONDITIONS
    IF= r'if\s+'
    def IF(self, t):
        t.value = str(t.value).strip()
        return t
    
    ELSE= r'else\s+'
    def ELSE(self, t):
        t.value = str(t.value).strip()
        return t
    
    #VARIABLES
    NAME= r'[a-zA-Z][a-zA-Z0-9_]*[a-zA-Z0-9]*'
    #CONSTANTS
    NUMBER = r'\d+'

    # Special symbols
    ASSIGN = r':'
    LINEEND= r';'
    COMMA= r','

    LPAREN = r'\('
    RPAREN = r'\)'
    LBRAKET= r'\['
    RBRAKET= r'\]'
    LKEY= r'\{'
    RKEY= r'\}'

    XPLUS= r'\+\+'
    XMINUS= r'--'

    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'

    EQUALS= r'='
    GREATER= r'>'
    LESS= r'<'

    # Ignored pattern
    ignore_newline = r'\n+'
    ignore_comment = r'\#.*'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1




class NDSParser(Parser):
    tokens = NDSLexer.tokens

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'UMINUS'),
        )

    def __init__(self):
        self.names = { }

    @_('NAME ASSIGN expr')
    def statement(self, p):
        self.names[p.NAME] = p.expr

    @_('expr')
    def statement(self, p):
        print(p.expr)

    @_('expr PLUS expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr MINUS expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr DIVIDE expr')
    def expr(self, p):
        return p.expr0 / p.expr1

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return int(p.NUMBER)

    @_('NAME')
    def expr(self, p):
        try:
            return self.names[p.NAME]
        except LookupError:
            print(f'Undefined name {p.NAME!r}')
            return 0



lexer = CalcLexer()
tokens = lexer.tokenize(
    '''
    t2= 20
    '''
)
# print([a for a in tokens])
parser = CalcParser()
pars= parser.parse(tokens)
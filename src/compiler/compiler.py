from sly import Lexer, Parser

class NDSLexer(Lexer):
    tokens = {'NATION', 'PROVINCE', 'SEA', 'NEUTRAL', 'TRAIT', 'EVENT', 'DISTRIBUTION',
            'NAME',
            'NUMBER', 'STRING',
            'ASSIGN', 'ARROW', 'PARAMASSIGN',
            'FOR', 'WHILE', 'IF', 'ELSE',
            'NOT', 'AND', 'OR', 'XOR',
            'GREATER', 'EGREATER', 'LESS', 'ELESS', 'XPLUS', 'XMINUS', 'EQUALS', 'NOTEQUALS', 
            'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE'}
    
    literals = { '(', ')', '{', '}', '[', ']', ';', ','}

    ignore = "\t "

    newline = r'\n+'
    def newline(self, t):
        self.lineno += t.value.count('\n')

    #ELEMENTS
    NATION= r'nation\s+'
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
    
    TRAIT= r'trait\s+'
    def TRAIT(self, t):
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
    
    NOT= r'not\s+'
    def NOT(self, t):
        t.value = str(t.value).strip()
        return t
    
    AND= r'and\s+'
    def AND(self, t):
        t.value = str(t.value).strip()
        return t
    
    OR= r'or\s+'
    def OR(self, t):
        t.value = str(t.value).strip()
        return t
    
    XOR= r'xor\s+'
    def XOR(self, t):
        t.value = str(t.value).strip()
        return t
    
    #OPERATORS
    EQUALS= r'=='
    NOTEQUALS= r'!='
    GREATER= r'>'
    LESS= r'<'
    EGREATER= r'>='
    ELESS= r'<='

    
    #VARIABLES
    NAME= r'[a-zA-Z][a-zA-Z0-9_]*[a-zA-Z0-9]*'

    #CONSTANTS
    NUMBER = r'\d+'
    STRING = r'\'.*?\''
    def STRING(self, t):
        t.value = str(t.value).strip('\'')
        return t

    # Special symbols
    ASSIGN = r'='
    PARAMASSIGN= r':'
    ARROW = r'->'

    XPLUS= r'\+\+'
    XMINUS= r'--'

    PLUS = r'\+'
    MINUS = r'-'
    MULTIPLY = r'\*'
    DIVIDE = r'/'

    # Ignored pattern
    ignore_comment = r'\#.*'

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1


class obj:
    def __init__(self, type:str, **kwargs):
        self.type= type
        self.__dict__.update(kwargs)
    
    def __str__(self):
        return str(self.__dict__)
    
    def get(self, key: str):
        return self.__dict__.get(key)


#fix: end with ; or not works. Must be only with ;.
class NDSParser(Parser):
    tokens = NDSLexer.tokens
    debugfile = 'parser.out'

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULTIPLY', 'DIVIDE'),
        #todo: precedences
        )

    def __init__(self):
        self.queue= []
    
    #SCRIPT
    @_('code ";" script')
    def script(self, p):
        return p.code + p.script
    
    @_('')
    def script(self, p):
        return []


    #CODE    
    @_('element')
    def code(self, p):
        return [p.element]
    
    @_('function')
    def code(self, p):
        return [p.function]
    
    @_('var')
    def code(self, p):
        return [p.var]
    
    @_('expr')
    def code(self, p):
        return [p.expr]
    

    #ELEMENTS
    @_('NATION NAME params', 'PROVINCE NAME params', 'SEA NAME params', 'NEUTRAL NAME params', 'TRAIT NAME params')
    def element(self, p):
        return obj(type='element', subtype=p[0], name=p.NAME, params=p[2])
    

    #VARS
    @_('NAME ASSIGN expr')
    def var(self, p):
        return obj(type='var', name=p.NAME, value=p.expr)
    

    #PARAMETERS
    @_('"(" params ")"')
    def params(self, p):
        return p.params
    
    @_('param "," params')
    def params(self, p):
        return [p.param] + p.params
    
    @_('param')
    def params(self, p):
        return [p.param]
    
    @_('')
    def params(self, p):
        return []

    @_('NAME PARAMASSIGN expr')
    def param(self, p):
        return obj(type='param', name=p.NAME, value=p.expr)
    

    #CONDITIONS
    @_('expr AND expr', 'expr OR expr', 'expr XOR expr', 'expr EQUALS expr', 'expr NOTEQUALS expr', 'expr GREATER expr', 'expr LESS expr', 'expr EGREATER expr', 'expr ELESS expr')
    def condition(self, p):
        return obj(type='condition', subtype=p[1], left=p.expr0, right=p.expr1)
    
    @_('NOT expr')
    def condition(self, p):
        return obj(type='condition', subtype=p[0], left=p.expr)


    #EXPRESSIONS
    @_('NUMBER')
    def expr(self, p):
        return obj(type='expr', subtype='number', value=int(p.NUMBER))
    
    @_('STRING')
    def expr(self, p):
        return obj(type='expr', subtype='string', value=str(p.STRING))
    
    @_('"[" list_expr "]"')
    def expr(self, p):
        return obj(type='expr', subtype='list', value=p.list_expr)
    
    @_('condition')
    def expr(self, p):
        return p.condition
    
    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr
    
    #ARITHMETIC
    @_('expr PLUS expr', 'expr MINUS expr', 'expr MULTIPLY expr', 'expr DIVIDE expr')
    def expr(self, p):
        return obj(type='arithmetic', subtype=p[1], left=p.expr0, right=p.expr1)
    
    @_('XPLUS expr', 'XMINUS expr')
    def expr(self, p):
        return obj(type='arithmetic', subtype=p[0], left=p.expr)
    
    @_('expr ARROW expr')
    def expr(self, p):
        return obj(type='expr', subtype='arrow', left=p.expr0, right=p.expr1)
    

    #LIST
    @_('expr "," list_expr')
    def list_expr(self, p):
        return [p.expr] + p.list_expr
    
    @_('')
    def list_expr(self, p):
        return []
    
    @_('expr')
    def list_expr(self, p):
        return [p.expr]
    

    #FUNCTIONS
    @_('EVENT NAME params "{" script "}"', 'DISTRIBUTION NAME params "{" script "}"')
    def function(self, p):
        if p[0] == 'event':
            return obj(type='function', subtype=p[0], name=p.NAME, params=p.params, script=p.script)
    
    @_('ELSE "{" script "}"')
    def function(self, p):
        return obj(type='function', subtype=p[0], script=p.script)

    @_('IF "(" condition ")" "{" script "}"', 'WHILE "(" condition ")" "{" script "}"')
    def function(self, p):
        return obj(type='function', subtype=p[0], condition=p.condition, script=p.script)



def compile(code: str):
    lexer = NDSLexer()
    parser = NDSParser()
    tokens = lexer.tokenize(code)
    return parser.parse(tokens)

# for i in compile(
#     '''
#     2+2;
#     '''
# ):
#     print(i)
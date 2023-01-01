from sly import Lexer, Parser

#todo: recordar strips
#todo: add time
#todo: add floordiv
#todo: add, sub, mul, div to arrays
class NDSLexer(Lexer):
    tokens = {'NATION', 'PROVINCE', 'SEA', 'NEUTRAL', 'TRAIT', 'EVENT', 'DISTRIBUTION', 'TIME',
            'SHOW',
            'NAME',
            'NUMBER', 'STRING', 'BOOL',
            'ASSIGN', 'ARROW', 'PARAMASSIGN',
            'FOR', 'WHILE', 'IF', 'ELSE',
            'NOT', 'AND', 'OR', 'XOR',
            'GREATER', 'EGREATER', 'LESS', 'ELESS', 'XPLUS', 'XMINUS', 'EQUALS', 'NOTEQUALS', 
            'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'POW', 'MOD'}
    
    literals = { '(', ')', '{', '}', '[', ']', ';', ','}

    ignore = "\t "

    newline = r'\n+'
    def newline(self, t):
        self.lineno += t.value.count('\n')
    

    #VARIABLES
    NAME= r'[_]*[a-zA-Z][a-zA-Z0-9_]*'

    #TIME
    TIME = r'\d+[dmy]'

    #BOOLEANS
    NAME['true'] = 'BOOL'
    NAME['false'] = 'BOOL'

    #ELEMENTS
    NAME['nation'] = 'NATION'
    NAME['province'] = 'PROVINCE'
    NAME['sea'] = 'SEA'
    NAME['neutral'] = 'NEUTRAL'
    NAME['trait'] = 'TRAIT'
    NAME['event'] = 'EVENT'
    NAME['distribution'] = 'DISTRIBUTION'

    #FUNCTIONS
    NAME['show'] = 'SHOW'
    NAME['for'] = 'FOR'
    NAME['while'] = 'WHILE'
    NAME['if'] = 'IF'
    NAME['else'] = 'ELSE'

    #LOGIC
    NAME['not'] = 'NOT'
    NAME['and'] = 'AND'
    NAME['or'] = 'OR'
    NAME['xor'] = 'XOR'
    
    #OPERATORS
    EQUALS= r'=='
    NOTEQUALS= r'!='
    GREATER= r'>'
    LESS= r'<'
    EGREATER= r'>='
    ELESS= r'<='

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
    POW = r'\*\*'
    MULTIPLY = r'\*'
    MOD= r'\%'
    DIVIDE = r'/'

    # Ignored pattern
    ignore_comment = r'\#.*'

    def error(self, t):
        raise Exception("Illegal character '%s'" % t.value)
        self.index += 1


class pobj:
    def __init__(self, type:str, **kwargs):
        self.type= type
        self.__dict__.update(kwargs)
    
    def __str__(self):
        return str(self.__dict__)
    
    def get(self, key: str):
        return self.__dict__.get(key)


#fix: end with ; or not works. Must be only with ;.
#fix: las lineas de codigo no comienzan a machear desde script, buscan machear con todo los elementos de ela gramatica.
#todo: precedences
#todo: mejorar la deteccion de errores
#todo: agregar for al parser

#todo: agregar funciones especiales(print, simulate, len....)

class NDSParser(Parser):
    tokens = NDSLexer.tokens
    debugfile = 'parser.out'

    precedence = (
        ('left', 'NATION', 'PROVINCE', 'SEA', 'NEUTRAL', 'TRAIT', 'EVENT', 'DISTRIBUTION'),
        ('left', 'NAME', 'NUMBER', 'STRING', 'BOOL'),
        ('left', 'TIME'),
        ('left', 'SHOW'),
        ('left', 'FOR', 'WHILE', 'IF', 'ELSE'),

        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULTIPLY', 'DIVIDE', 'MOD', 'POW'),
        ('left', 'AND', 'OR', 'XOR'),
        ('left', 'EQUALS', 'NOTEQUALS', 'GREATER', 'LESS', 'EGREATER', 'ELESS'),
        ('left', 'XPLUS', 'XMINUS'),
        ('left', 'UMINUS', 'UPLUS'),
        ('left', 'NOT'),
        #todo: precedences
        )

    def __init__(self):
        self.queue= []
    
    #SCRIPT
    @_('code script')
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
        return pobj(type='element', subtype=p[0], name=p.NAME, params=p[2])
    

    #VARS
    @_('NAME ASSIGN expr')
    def var(self, p):
        return pobj(type='var', name=p.NAME, value=p.expr)
    

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
        return pobj(type='param', name=p.NAME, value=p.expr)
    

    #CONDITIONS
    @_('expr AND expr', 'expr OR expr', 'expr XOR expr')
    def condition(self, p):
        return pobj(type='condition', subtype=p[1], left=p.expr0, right=p.expr1)
    
    @_('NOT expr')
    def condition(self, p):
        return pobj(type='scondition', subtype=p[0], value=p.expr)
    

    #COMPARATIONS
    @_('expr EQUALS expr', 'expr NOTEQUALS expr', 'expr GREATER expr', 'expr LESS expr', 'expr EGREATER expr', 'expr ELESS expr')
    def condition(self, p):
        return pobj(type='comparation', subtype=p[1], left=p.expr0, right=p.expr1)

    #EXPRESSIONS
    @_('NAME')
    def expr(self, p):
        return pobj(type='expr', subtype='name', value=str(p.NAME))

    @_('NUMBER')
    def expr(self, p):
        return pobj(type='expr', subtype='number', value=int(p.NUMBER))
    
    @_('STRING')
    def expr(self, p):
        return pobj(type='expr', subtype='string', value=str(p.STRING))
    
    @_('BOOL')
    def expr(self, p):
        return pobj(type='expr', subtype='bool', value=str(p.BOOL))
    
    @_('TIME')
    def expr(self, p):
        return pobj(type='expr', subtype='time', value=str(p.TIME))
    
    @_('"[" list_expr "]"')
    def expr(self, p):
        return pobj(type='expr', subtype='list', value=p.list_expr)
    
    @_('condition')
    def expr(self, p):
        return p.condition
    
    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr
    
    #ARITHMETIC
    @_('expr PLUS expr', 'expr MINUS expr', 'expr MULTIPLY expr', 'expr DIVIDE expr', 'expr POW expr', 'expr MOD expr')
    def expr(self, p):
        return pobj(type='arithmetic', subtype=p[1], left=p.expr0, right=p.expr1)
    
    @_('XPLUS expr', 'XMINUS expr')
    def expr(self, p):
        return pobj(type='xarithmetic', subtype=p[0], left=p.expr)
    
    @_('PLUS expr %prec UPLUS', 'MINUS expr %prec UMINUS')
    def expr(self, p):
        return pobj(type='uarithmetic', subtype=p[0], value=p.expr)
    
    @_('expr ARROW expr')
    def expr(self, p):
        return pobj(type='expr', subtype='arrow', left=p.expr0, right=p.expr1)
    

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
    @_('SHOW "(" expr ")"')
    def function(self, p):
        return pobj(type='function', subtype=p[0], value=p.expr)

    @_('EVENT NAME params "{" script "}"', 'DISTRIBUTION NAME params "{" script "}"')
    def function(self, p):
        if p[0] == 'event':
            return pobj(type='function', subtype=p[0], name=p.NAME, params=p.params, script=p.script)
    
    @_('ELSE "{" script "}"')
    def function(self, p):
        return pobj(type='function', subtype=p[0], script=p.script)

    @_('IF "(" condition ")" "{" script "}"', 'WHILE "(" condition ")" "{" script "}"')
    def function(self, p):
        return pobj(type='function', subtype=p[0], condition=p.condition, script=p.script)

    #ERRORS
    def error(self, p):
        if p:
            raise Exception("Syntax error at token", p.type)
        else:
            raise Exception("Syntax error at EOF")


def compile(code: str):
    lexer = NDSLexer()
    parser = NDSParser()
    tokens = lexer.tokenize(code)
    return parser.parse(tokens)

# for i in compile(
#     '''
#     2y
#     '''
# ):
#     print(i)













from sly import Lexer, Parser


#todo: add floordiv
#todo: add, sub, mul, div to arrays
class NDSLexer(Lexer):
    tokens = {'ELEMENT', 'EVENT', 'DECISION',
            'FUNC', 'RETURN',
            'NAME','NUMBER', 'STRING', 'BOOL', 'TIME', 'TYPE',
            'ASSIGN', 'ARROW', 'PARAMASSIGN',
            'FOR', 'WHILE', 'IF', 'ELSE',
            'NOT', 'AND', 'OR', 'XOR',
            'GREATER', 'EGREATER', 'LESS', 'ELESS', 'XPLUS', 'XMINUS', 'EQUALS', 'NOTEQUALS', 
            'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'POW', 'MOD', 'FLOORDIV',}
    
    literals = { '(', ')', '{', '}', '[', ']', ';', ','}

    def __init__(self):
        self.nesting_level = 0
    
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
    NAME['nation'] = 'ELEMENT'
    NAME['province'] = 'ELEMENT'
    NAME['neutral'] = 'ELEMENT'
    NAME['sea'] = 'ELEMENT'
    NAME['trait'] = 'ELEMENT'
    NAME['category'] = 'ELEMENT'
    NAME['distribution'] = 'ELEMENT'
    
    NAME['event'] = 'EVENT'
    NAME['decision'] = 'DECISION'
    NAME['return'] = 'RETURN'

    #SPECIAL FUNCTIONS
    NAME['show'] = 'FUNC'
    NAME['simulate'] = 'FUNC'
    NAME['size'] = 'FUNC'
    NAME['type'] = 'FUNC'
    NAME['pos'] = 'FUNC'

    NAME['random'] = 'FUNC'
    # NAME[''] = 'FUNC'

    #FUNCTIONS
    NAME['for'] = 'FOR'
    NAME['while'] = 'WHILE'
    NAME['if'] = 'IF'
    NAME['else'] = 'ELSE'

    #LOGIC
    NAME['not'] = 'NOT'
    NAME['and'] = 'AND'
    NAME['or'] = 'OR'
    NAME['xor'] = 'XOR'

    #TYPES
    NAME['number'] = 'TYPE'
    NAME['integer'] = 'TYPE'
    NAME['decimal'] = 'TYPE'
    NAME['string'] = 'TYPE'
    NAME['bool'] = 'TYPE'
    NAME['list'] = 'TYPE'
    NAME['time'] = 'TYPE'
    

    
    #OPERATORS
    EQUALS= r'=='
    NOTEQUALS= r'!='
    GREATER= r'>'
    LESS= r'<'
    EGREATER= r'>='
    ELESS= r'<='

    #CONSTANTS
    NUMBER = r'\d+(\.\d+)?'
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
    FLOORDIV = r'//'
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

class NDSParser(Parser):
    tokens = NDSLexer.tokens
    debugfile = 'parser.out'
    

    precedence = (
        ('left', 'ELEMENT', 'EVENT'),
        ('left', 'NAME', 'NUMBER', 'STRING', 'BOOL', 'TIME'),
        ('left', 'ASSIGN', 'PARAMASSIGN'),
        ('left', 'ARROW'),
        ('left', 'FUNC'),
        ('left', 'FOR', 'WHILE', 'IF', 'ELSE'),

        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULTIPLY', 'FLOORDIV', 'DIVIDE', 'MOD', 'POW'),

        ('left', 'AND', 'OR', 'XOR'),
        ('left', 'EQUALS', 'NOTEQUALS', 'GREATER', 'LESS', 'EGREATER', 'ELESS'),

        ('left', 'XPLUS', 'XMINUS'),
        ('left', 'UMINUS', 'UPLUS'),
        ('left', 'NOT'),
        #todo: precedences
        )


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
    
    #todo: here
    @_('func')
    def code(self, p):
        return [p.func]
    
    @_('var')
    def code(self, p):
        return [p.var]
    


    @_('inside_code inside_script')
    def inside_script(self, p):
        return p.inside_code + p.inside_script

    @_('')
    def inside_script(self, p):
        return []
    
    @_('code')
    def inside_code(self, p):
        return p.code

    @_('RETURN expr')
    def inside_code(self, p):
        return [pobj(type='return', value=p.expr)]

    
    #todo: add return

    #ELEMENTS
    @_('ELEMENT NAME "(" exeparams ")"')
    def element(self, p):
        return pobj(type='element', subtype=p[0], name=p.NAME, params=p.exeparams)
    


    #VARS
    @_('NAME ASSIGN expr')
    def var(self, p):
        return pobj(type='var', subtype= 'expr', name=p.NAME, value=p.expr)
    


    #ELEMENTS VARS
    @_('NAME ARROW NAME PARAMASSIGN expr')
    def var(self, p):
        return pobj(type='var', subtype='element', name=p.NAME0, var=p.NAME1, value=p.expr)
    
    @_('NAME ARROW NAME PARAMASSIGN XPLUS expr', 'NAME ARROW NAME PARAMASSIGN XMINUS expr')
    def var(self, p):
        return pobj(type='var', subtype='element', name=p.NAME0, var=p.NAME1, value=p.expr, op=p[4])
    


    #FUNC PARAMETERS
    @_('param "," params')
    def params(self, p):
        return [p.param] + p.params
    
    @_('param')
    def params(self, p):
        return [p.param]
    
    @_('')
    def params(self, p):
        return []

    @_('NAME PARAMASSIGN TYPE')
    def param(self, p):
        return pobj(type='func param', subtype='assign', value=p.NAME, vartype=p[1])
    
    @_('NAME')
    def param(self, p):
        return pobj(type='func param', value=p.NAME)
    
    

    #EXECUTION PARAMETERS
    @_('exeparam "," exeparams')
    def exeparams(self, p):
        return [p.exeparam] + p.exeparams
    
    @_('exeparam')
    def exeparams(self, p):
        return [p.exeparam]
    
    @_('')
    def exeparams(self, p):
        return []
    
    @_('NAME PARAMASSIGN expr')
    def exeparam(self, p):
        return pobj(type='exe param', subtype='assign', name=p.NAME, value=p.expr)
    
    @_('expr')
    def exeparam(self, p):
        return pobj(type='exe param', value=p.expr)
    
    

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
        try:
            return pobj(type='expr', subtype='integer', value=int(p.NUMBER))
        except:
            return pobj(type='expr', subtype='decimal', value=float(p.NUMBER))
    
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
    
    
    @_('func')
    def expr(self, p):
        return p.func
    


    #ARITHMETIC
    @_('expr PLUS expr', 'expr MINUS expr', 'expr MULTIPLY expr', 'expr DIVIDE expr', 'expr POW expr', 'expr MOD expr', 'expr FLOORDIV expr')
    def expr(self, p):
        return pobj(type='arithmetic', subtype=p[1], left=p.expr0, right=p.expr1)
    
    
    @_('PLUS expr %prec UPLUS', 'MINUS expr %prec UMINUS')
    def expr(self, p):
        return pobj(type='uarithmetic', subtype=p[0], value=p.expr)
    
    #todo: expr to name
    @_('NAME ARROW NAME')
    def expr(self, p):
        return pobj(type='expr', subtype='arrow', name=p.NAME0, var=p.NAME1)
    
    @_('NAME ARROW NAME "(" exeparams ")"')
    def expr(self, p):
        return pobj(type='expr', subtype='arrow', name=p.NAME0, var=p.NAME1, params= p.exeparams)

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
    


    #FUNC
    @_('FUNC "(" exeparams ")"')
    def func(self, p):
        return pobj(type='func', subtype=p[0], params=p.exeparams)
    


    #FUNCTIONS
    @_('EVENT NAME "(" exeparams ")" "(" params ")" "{" inside_script "}"')
    def function(self, p):
        return pobj(type='function', subtype=p[0], name=p.NAME, params=p.exeparams, args=p.params, script=p.inside_script)
    
    @_('DECISION NAME "(" func_condition "," exeparams ")" "(" params ")"')
    def function(self, p):
        return pobj(type='function', subtype=p[0], name=p.NAME, params=p.exeparams, condition=p.func_condition, args=p.params)

    @_('condition')
    def func_condition(self, p):
        return [pobj(type='func condition', value=p.condition)]
    


    #EXECUTION
    @_('NAME "(" exeparams ")"')
    def func(self, p):
        return pobj(type= 'execution', name=p.NAME, params=p.exeparams)


    #LOOPS
    @_('IF "(" condition ")" "{" inside_script "}" ELSE "{" inside_script "}"')
    def function(self, p):
        return pobj(type='loop', subtype='if else', condition=p.condition, script=p.inside_script0, else_script=p.inside_script1)
    
    @_('IF "(" condition ")" "{" inside_script "}"')
    def function(self, p):
        return pobj(type='loop', subtype=p[0], condition=p.condition, script=p.inside_script)

    @_('WHILE "(" condition ")" "{" inside_script "}"')
    def function(self, p):
        return pobj(type='loop', subtype=p[0], condition=p.condition, script=p.inside_script)

    @_('FOR "(" NAME "," exeparams ")" "{" inside_script "}"')
    def function(self, p):
        return pobj(type='loop', subtype=p[0], var=p.NAME, params=p.exeparams, script=p.inside_script)


    
    #ERRORS
    def error(self, p):
        if p:
            raise Exception("Syntax error at token %s in line %s" % (p.value, p.lineno))
        else:
            raise Exception("Syntax error at EOF")
    
    # def error(self, p):
    #     if not p:
    #         return

    #     while True:
    #         tok = next(self.tokens, None)
    #         if not tok or tok.type == ';':
    #             break
    #     self.restart()


def compile(code: str):
    lexer = NDSLexer()
    parser = NDSParser()
    tokens = lexer.tokenize(code)
    return parser.parse(tokens)

# for i in compile(
#     '''
#     # province New_York(2056, 20, 103856)

#     a= 2+2

#     # province Havana(extension: 10, development: 20, population: 30)
#     # event c(d: 1)(){
#     #     a=2
#     #     d=2
#     # }
#     # c(c:2)
#     '''
# ):
#     print(i)



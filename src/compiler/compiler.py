from sly import Lexer, Parser

#todo: add floordiv
#todo: add, sub, mul, div to arrays
class NDSLexer(Lexer):
    tokens = {'ELEMENT', 'EVENT', 'DECISION',
            'IPLUS', 'IMINUS', 'IMULTIPLY', 'IDIVIDE', 'IPOW', 'IMOD', 'IFLOORDIV',
            'FUNC', 'RETURN',
            'NAME','NUMBER', 'STRING', 'BOOL', 'TIME', 'TYPE',
            'ASSIGN', 'ARROW', 'PARAMASSIGN', 'LF', 'RF',
            'FOR', 'WHILE', 'IF', 'ELSE',
            'NOT', 'AND', 'OR', 'XOR',
            'GREATER', 'EGREATER', 'LESS', 'ELESS', 'XPLUS', 'XMINUS', 'EQUALS', 'NOTEQUALS', 
            'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'POW', 'MOD', 'FLOORDIV',}
    
    literals = { '(', ')', '{', '}', '[', ']', ';', ','}

    def __init__(self):
        self.nesting_level = 0
    
    ignore = "\t "
    ignore_comment = r'\#.*'

    newline = r'\n+'
    def newline(self, t):
        self.lineno += t.value.count('\n')
    

    LF= r'<<'
    RF= r'>>'
    
    #OPERATORS
    EQUALS= r'=='
    NOTEQUALS= r'!='
    EGREATER= r'>='
    GREATER= r'>'
    ELESS= r'<='
    LESS= r'<'
    

    # Special symbols
    ASSIGN = r'='
    PARAMASSIGN= r':'
    ARROW = r'->'

    #ELEMENTS VARS UPDATES
    XPLUS= r'\+\+'
    XMINUS= r'--'

    #ARIHTMETIC
    IPLUS = r'\+='
    PLUS = r'\+'
    IMINUS = r'-='
    MINUS = r'-'
    IPOW = r'\*\*='
    POW = r'\*\*'
    IMULTIPLY = r'\*='
    MULTIPLY = r'\*'
    IMOD = r'\%='
    MOD= r'\%'
    IFLOORDIV = r'//='
    FLOORDIV = r'//'
    IDIVIDE = r'/='
    DIVIDE = r'/'
    

    #VARIABLES
    NAME= r'[_]*[a-zA-Z][a-zA-Z0-9_]*'

    NUMBER = r'\d+(\.\d+)?'

    STRING = r'\'.*?\''
    def STRING(self, t):
        t.value = str(t.value).strip('\'')
        return t

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
    NAME['params'] = 'FUNC'
    NAME['size'] = 'FUNC'
    NAME['type'] = 'FUNC'
    NAME['pos'] = 'FUNC'

    NAME['rvs'] = 'FUNC'
    NAME['irvs'] = 'FUNC'

    NAME['gen_dist'] = 'FUNC'

    NAME['simulate'] = 'FUNC'
    NAME['enable'] = 'FUNC'
    NAME['disable'] = 'FUNC'

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
    NAME['boolean'] = 'TYPE'
    NAME['list'] = 'TYPE'
    NAME['time'] = 'TYPE'
    

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




class NDSParser(Parser):
    tokens = NDSLexer.tokens
    debugfile = 'parser.out'
    

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULTIPLY', 'FLOORDIV', 'DIVIDE', 'MOD', 'POW'),

        ('left', 'OR', 'XOR'),
        ('left', 'AND'),

        ('left', 'EQUALS', 'NOTEQUALS'),
        ('left', 'GREATER', 'LESS', 'EGREATER', 'ELESS'),

        ('right', 'XPLUS', 'XMINUS'),
        ('right', 'UMINUS', 'UPLUS'),

        ('right', 'NOT'),
        )


    #SCRIPT
    @_('code script')
    def script(self, p):
        return p.code + p.script
    
    @_('')
    def script(self, p):
        return []
    
    

    #LINE OF CODE 
    @_('element')
    def code(self, p):
        return [p.element]
    
    @_('function')
    def code(self, p):
        return [p.function]
    
    @_('func')
    def code(self, p):
        return [p.func]
    
    @_('var')
    def code(self, p):
        return [p.var]
    


    #FUNCTIONS CODE
    @_('function_code function_script')
    def function_script(self, p):
        return p.function_code + p.function_script

    @_('')
    def function_script(self, p):
        return []
    
    @_('code')
    def function_code(self, p):
        return p.code

    @_('RETURN expr')
    def function_code(self, p):
        return [pobj(type='return', value=p.expr)]

    

    #ELEMENTS
    @_('ELEMENT NAME "(" args ")"')
    def element(self, p):
        return pobj(type='element', subtype=p[0], name=p.NAME, params=p.args)
    
    @_('EVENT NAME LF params RF "{" function_script "}"')
    def element(self, p):
        return pobj(type='element', subtype=p[0], name=p.NAME, args=p.params, script=p.function_script)
    
    @_('EVENT NAME "(" args ")" "{" function_script "}"')
    def element(self, p):
        return pobj(type='element', subtype=p[0], name=p.NAME, params=p.args, script=p.function_script)

    @_('DECISION NAME "(" condition "," args ")" LF params RF')
    def element(self, p):
        return pobj(type='element', subtype=p[0], name=p.NAME, params=p.args, condition=p.condition, args=p.params)
    


    #fix: name to expr
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
    


    #FUNC PARAMS
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
    
    

    #FUNTION ARGS
    @_('arg "," args')
    def args(self, p):
        return [p.arg] + p.args
    
    @_('arg')
    def args(self, p):
        return [p.arg]
    
    @_('')
    def args(self, p):
        return []
    
    @_('NAME PARAMASSIGN expr')
    def arg(self, p):
        return pobj(type='args', subtype='assign', name=p.NAME, value=p.expr)
    
    @_('expr')
    def arg(self, p):
        return pobj(type='args', value=p.expr)
    
    

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
      
    @_('ELEMENT')
    def expr(self, p):
        return pobj(type='type', value=p.ELEMENT)
    
    @_('EVENT')
    def expr(self, p):
        return pobj(type='type', value=p.EVENT)
    
    @_('DECISION')
    def expr(self, p):
        return pobj(type='type', value=p.DECISION)
    
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
    
    @_('NAME ARROW NAME "(" args ")"')
    def expr(self, p):
        return pobj(type='expr', subtype='arrow', name=p.NAME0, var=p.NAME1, params= p.args)

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
    @_('FUNC "(" args ")"')
    def func(self, p):
        return pobj(type='func', subtype=p[0], params=p.args)
    


   


    #EXECUTION
    @_('NAME "(" args ")"')
    def func(self, p):
        return pobj(type= 'execution', name=p.NAME, params=p.args)


    #LOOPS
    @_('IF "(" condition ")" "{" function_script "}" ELSE "{" function_script "}"')
    def function(self, p):
        return pobj(type='loop', subtype='if else', condition=p.condition, script=p.function_script0, else_script=p.function_script1)
    
    @_('IF "(" condition ")" "{" function_script "}"')
    def function(self, p):
        return pobj(type='loop', subtype=p[0], condition=p.condition, script=p.function_script)

    @_('WHILE "(" condition ")" "{" function_script "}"')
    def function(self, p):
        return pobj(type='loop', subtype=p[0], condition=p.condition, script=p.function_script)

    @_('FOR "(" NAME "," args ")" "{" function_script "}"')
    def function(self, p):
        return pobj(type='loop', subtype=p[0], var=p.NAME, params=p.args, script=p.function_script)


    
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



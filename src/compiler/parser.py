from sly import Parser
from compiler.lexer import NDSLexer
from compiler.parser_obj import *

class NDSParser(Parser):
    tokens = NDSLexer.tokens
    debugfile = 'parser.out'
    start = 'script'

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
    
    @_('empty')
    def script(self, p):
        return []
    

    
    #LINE OF CODE 
    @_('element')
    def code(self, p):
        return [p.element]
    
    @_('var')
    def code(self, p):
        return [p.var]
    
    @_('loop')
    def code(self, p):
        return [p.loop]
    
    @_('conditional')
    def code(self, p):
        return [p.conditional]
    
    @_('function')
    def code(self, p):
        return [p.function]
    
    @_('')
    def empty(self, p):
        return []



    #FUNCTIONS CODE
    @_('function_code function_script')
    def function_script(self, p):
        return p.function_code + p.function_script

    @_('empty')
    def function_script(self, p):
        return []
    
    @_('code')
    def function_code(self, p):
        return p.code

    @_('RETURN expr END')
    def function_code(self, p):
        return [ParserObj(type='out', subtype='return', value=p.expr)]
    
    @_('ENABLE expr END')
    def function_code(self, p):
        return [ParserObj(type='out', subtype='enable', value=p.expr)]
    
    @_('DISABLE expr END')
    def function_code(self, p):
        return [ParserObj(type='out', subtype='disable', value=p.expr)]

    

    #ELEMENTS
    @_('ELEMENT NAME "(" args ")" END')
    def element(self, p):
        return ParserObj(type='element', subtype=p[0], name=p.NAME, params=p.args)
    
    @_('EVENT NAME LF params RF "{" function_script "}"')
    def element(self, p):
        return ParserObj(type='element', subtype=p[0], name=p.NAME, args=p.params, script=p.function_script)
    
    @_('EVENT NAME "(" args ")" "{" function_script "}"')
    def element(self, p):
        return ParserObj(type='element', subtype=p[0], name=p.NAME, params=p.args, script=p.function_script)

    #check
    @_('DECISION NAME "(" expr "," args ")" LF params RF END')
    def element(self, p):
        return ParserObj(type='element', subtype=p[0], name=p.NAME, params=p.args, condition=p.expr, args=p.params)
    


    #VARS
    @_('NAME VARASSIGN expr END')
    def var(self, p):
        return ParserObj(type='var', subtype= 'expr', name=p.NAME, value=p.expr)
    
    @_('expr ARROW NAME VARASSIGN expr END')
    def var(self, p):
        return ParserObj(type='var', subtype='element', name=p.expr0, var=p.NAME, value=p.expr1)
    
    @_('expr ARROW NAME VARASSIGN XPLUS expr END', 'expr ARROW NAME VARASSIGN XMINUS expr END')
    def var(self, p):
        return ParserObj(type='var', subtype='element', name=p.expr0, var=p.NAME, value=p.expr1, op=p[4])
    


    #LOOPS
    @_('WHILE expr "{" function_script "}"')
    def loop(self, p):
        return ParserObj(type='loop', subtype=p[0], condition=p.expr, script=p.function_script)

    @_('REPEAT LF NAME RF "(" expr "," expr ")" "{" function_script "}"')
    def loop(self, p):
        return ParserObj(type='loop', subtype=p[0], var=p.NAME, init=p.expr0, end=p.expr1, script=p.function_script)
    
    @_('FOREACH LF NAME RF "(" expr ")" "{" function_script "}"')
    def loop(self, p):
        return ParserObj(type='loop', subtype=p[0], var=p.NAME, param=p.expr, script=p.function_script)
    


    #CONDITIONALS
    @_('IF expr "{" function_script "}" ELSE "{" function_script "}"')
    def conditional(self, p):
        return ParserObj(type='conditional', subtype='if else', condition=p.expr, script=p.function_script0, else_script=p.function_script1)
    
    @_('IF expr "{" function_script "}"')
    def conditional(self, p):
        return ParserObj(type='conditional', subtype=p[0], condition=p.expr, script=p.function_script)
    


    #FUNC
    @_('func END')
    def function(self, p):
        return p.func

    @_('FUNC "(" args ")"')
    def func(self, p):
        return ParserObj(type='func', subtype=p[0], params=p.args)

    #EXECUTION
    @_('NAME "(" args ")"')
    def func(self, p):
        return ParserObj(type= 'execution', name=p.NAME, params=p.args)



    #FUNC PARAMS
    @_('param "," params')
    def params(self, p):
        return [p.param] + p.params
    
    @_('param')
    def params(self, p):
        return [p.param]
    
    @_('empty')
    def params(self, p):
        return []

    @_('NAME PARAMASSIGN TYPE')
    def param(self, p):
        return ParserObj(type='func param', subtype='assign', value=p.NAME, vartype=p[1])
    
    @_('NAME')
    def param(self, p):
        return ParserObj(type='func param', value=p.NAME)
    


    #FUNTION ARGS
    @_('arg "," args')
    def args(self, p):
        return [p.arg] + p.args
    
    @_('arg')
    def args(self, p):
        return [p.arg]
    
    @_('empty')
    def args(self, p):
        return []
    
    @_('NAME PARAMASSIGN expr')
    def arg(self, p):
        return ParserObj(type='args', subtype='assign', name=p.NAME, value=p.expr)
    
    @_('expr')
    def arg(self, p):
        return ParserObj(type='args', value=p.expr)
    
    

    #CONDITIONS
    @_('expr AND expr', 'expr OR expr', 'expr XOR expr')
    def condition(self, p):
        return ParserObj(type='condition', subtype=p[1], left=p.expr0, right=p.expr1)
    
    @_('NOT expr')
    def condition(self, p):
        return ParserObj(type='ucondition', subtype=p[0], value=p.expr)
    

    #COMPARATIONS
    @_('expr EQUALS expr', 'expr NOTEQUALS expr', 'expr GREATER expr', 'expr LESS expr', 'expr EGREATER expr', 'expr ELESS expr')
    def condition(self, p):
        return ParserObj(type='comparation', subtype=p[1], left=p.expr0, right=p.expr1)



    #EXPRESSIONS
    @_('NAME')
    def expr(self, p):
        return ParserObj(type='expr', subtype='name', value=str(p.NAME))

    @_('NUMBER')
    def expr(self, p):
        try:
            return ParserObj(type='expr', subtype='integer', value=int(p.NUMBER))
        except:
            return ParserObj(type='expr', subtype='decimal', value=float(p.NUMBER))
    
    @_('STRING')
    def expr(self, p):
        return ParserObj(type='expr', subtype='string', value=str(p.STRING))
    
    @_('BOOL')
    def expr(self, p):
        return ParserObj(type='expr', subtype='bool', value=str(p.BOOL))
    
    @_('TIME')
    def expr(self, p):
        return ParserObj(type='expr', subtype='time', value=str(p.TIME))
    
    @_('ELEMENT')
    def expr(self, p):
        return ParserObj(type='type', value=p.ELEMENT)
    
    @_('EVENT')
    def expr(self, p):
        return ParserObj(type='type', value=p.EVENT)
    
    @_('DECISION')
    def expr(self, p):
        return ParserObj(type='type', value=p.DECISION)
    
    @_('expr ARROW NAME')
    def expr(self, p):
        return ParserObj(type='expr', subtype='arrow', name=p.expr, var=p.NAME)
    
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
        return ParserObj(type='arithmetic', subtype=p[1], left=p.expr0, right=p.expr1)
    
    @_('PLUS expr %prec UPLUS', 'MINUS expr %prec UMINUS')
    def expr(self, p):
        return ParserObj(type='uarithmetic', subtype=p[0], value=p.expr)



    #LIST
    @_('"[" list_expr "]"')
    def expr(self, p):
        return ParserObj(type='expr', subtype='list', value=p.list_expr)
    
    @_('expr "," list_expr')
    def list_expr(self, p):
        return [p.expr] + p.list_expr
    
    @_('empty')
    def list_expr(self, p):
        return []
    
    @_('expr')
    def list_expr(self, p):
        return [p.expr]


    
    #ERRORS
    def error(self, p):
        if p:
            raise Exception("Syntax error at token %s in line %s" % (p.value, p.lineno))
        else:
            raise Exception("Syntax error at EOF")
from sly import Lexer, Parser

class NDSLexer(Lexer):
    tokens = {'NATION', 'PROVINCE', 'SEA', 'NEUTRAL', 'TRAIT', 'EVENT', 'DISTRIBUTION',
            'NAME',
            'NUMBER', 'STRING',
            'ASSIGN', 'ARROW',
            'FOR', 'WHILE', 'IF', 'ELSE',
            'NOT', 'AND', 'OR', 'XOR',
            'GREATER', 'EGREATER', 'LESS', 'ELESS', 'XPLUS', 'XMINUS', 'EQUALS', 'NOTEQUALS', 
            'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE'}
    
    literals = { '(', ')', '{', '}', '[', ']', ';', ',' }

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



#bug: end with ; or not works. Must be only with ;.
class NDSParser(Parser):
    tokens = NDSLexer.tokens
    debugfile = 'parser.out'

    precedence = (

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
    

    #ELEMENTS
    @_('NATION NAME params', 'PROVINCE NAME params', 'SEA NAME params', 'NEUTRAL NAME params', 'TRAIT NAME params')
    def element(self, p):
        #{'name': <element name>, 'params': <element params>, 'type': <element type>}
        return {'name': p.NAME, 'params': p.params, 'type': p[0]}
    

    #VARS
    @_('NAME ASSIGN expr')
    def var(self, p):
        #{'name': <var name>, 'value': <var value>, 'type':'var'}
        return {'name': p.NAME, 'value': p.expr, 'type':'var'}
    

    #PARAMETERS
    @_('"(" param ")"')
    def params(self, p):
        return p.param

    @_('param "," param')
    def param(self, p):
        return p.param0 + p.param1
        
    @_('NUMBER')
    def param(self, p):
        return [int(p.NUMBER)]

    @_('expr')
    def param(self, p):
        return [p.expr]
    

    #CONDITIONS
    @_('expr AND expr', 'expr OR expr', 'expr XOR expr', 'expr EQUALS expr', 'expr NOTEQUALS expr', 'expr GREATER expr', 'expr LESS expr', 'expr EGREATER expr', 'expr ELESS expr')
    def condition(self, p):
        #{'type': <condition type>, 'left': <left side>, 'right': <right side>}
        return {'type': p[1], 'left': p.expr0, 'right': p.expr1}
    
    @_('NOT expr')
    def condition(self, p):
        #{'type': <condition type>, 'expr': <expr>}
        return {'type': p[0], 'value': p.expr}


    #EXPRESSIONS
    @_('NUMBER')
    def expr(self, p):
        return int(p.NUMBER)
    
    @_('STRING')
    def expr(self, p):
        return str(p.STRING)
    
    @_('"[" list_expr "]"')
    def expr(self, p):
        return p.list_expr
    
    @_('condition')
    def expr(self, p):
        return p.condition
    
    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr
    
    #ARIHTMETIC
    @_('expr PLUS expr', 'expr MINUS expr', 'expr MULTIPLY expr', 'expr DIVIDE expr')
    def expr(self, p):
        #{'type': <operation type>, 'left': <left side>, 'right': <right side>}
        return {'type': p[1], 'left': p.expr0, 'right': p.expr1}
    
    @_('XPLUS expr', 'XMINUS expr')
    def expr(self, p):
        #{'type': <operation type>, 'value': <value>}
        return {'type': p[0], 'value': p.expr}
    
    @_('expr ARROW expr')
    def expr(self, p):
        #{'type': <operation type>, 'left': <left side>, 'right': <right side>}
        return {'type': p[1], 'left': p.expr0, 'right': p.expr1}
    

    #LIST
    @_('list_expr "," list_expr')
    def list_expr(self, p):
        return p.list_expr0 + p.list_expr1
    
    @_('expr')
    def list_expr(self, p):
        return [p.expr]
    

    #FUNCTIONS
    @_('EVENT NAME params "{" script "}"', 'DISTRIBUTION NAME params "{" script "}"')
    def function(self, p):
        #{'name': <function name>, 'params': <function params>, 'type': <function type>, 'script': <function script>}
        if p[0] == 'event':
            return {'name': p.NAME, 'params': p.params, 'type': 'event', 'execution': p.script}
    
    @_('ELSE "{" script "}"')
    def function(self, p):
        #{'type': <function type>, 'script': <function script>}
        return {'type': 'else', 'execution': p.script}

    @_('IF "(" condition ")" "{" script "}"', 'WHILE "(" condition ")" "{" script "}"')
    def function(self, p):
            return {'type': p[0], 'condition': p.condition, 'execution': p.script}

    
    
    


def compile(code: str):
    lexer = NDSLexer()
    parser = NDSParser()

    tokens = lexer.tokenize(code)
    
    print(parser.parse(tokens))

compile(
    '''
    a= 2*4 +3;
    '''
)
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
    EQUALS= r'='
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
    ASSIGN = r':'
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
        self.elements = {
            'nations': {},
            'provinces': {},
            'seas': {},
            'neutrals': {},
            'traits': {},
        }
        self.vars = {}
    
    #SCRIPT
    @_('script ";" script')
    def script(self, p):
        return p.script0 + p.script1
    
    @_('script ";"')
    def script(self, p):
        return p.script
    
    @_('element')
    def script(self, p):
        return p.element
    
    @_('NAME ASSIGN expr')
    def script(self, p):
        self.vars[p.NAME] = p.expr
        return p.NAME

    #ELEMENTS
    @_('NATION NAME params', 'PROVINCE NAME params', 'SEA NAME params', 'NEUTRAL NAME params', 'TRAIT NAME params')
    def element(self, p):
        if p[0] == 'nation':
            self.elements['nations'][p.NAME] = p.params
            return p.NAME
        elif p[0] == 'province':
            self.elements['provinces'][p.NAME] = p.params
            return p.NAME
        elif p[0] == 'sea':
            self.elements['seas'][p.NAME] = p.params
            return p.NAME
        elif p[0] == 'neutral':
            self.elements['neutrals'][p.NAME] = p.params
            return p.NAME
        elif p[0] == 'trait':
            self.elements['traits'][p.NAME] = p.params
            return p.NAME
    

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
    
    #LIST
    @_('list_expr "," list_expr')
    def list_expr(self, p):
        return p.list_expr0 + p.list_expr1
    
    @_('expr')
    def list_expr(self, p):
        return [p.expr]




def compile(code: str):
    lexer = NDSLexer()
    parser = NDSParser()

    tokens = lexer.tokenize(code)
    parser.parse(tokens)
    print(parser.elements)
    print(parser.vars)

compile(
    '''
    #comment
    z: 2;
    y: 'Pez';
    nation a(2, 3,
    5);

            nation b(3, 'pollo');
    province c(4);

        nation d(5); #commnet2
    nation e(6);
    neutral f(7);

    trait g(5, [2,5,3]);
    '''
)
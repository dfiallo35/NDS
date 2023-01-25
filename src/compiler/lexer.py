from sly import Lexer

class NDSLexer(Lexer):
    tokens = {
            'ELEMENT', 'EVENT', 'DECISION', 'SIMULATION', 'FUNCTION', 'FUNC', 'RETURN', 'ENABLE', 'DISABLE',

            'NAME','NUMBER', 'STRING', 'BOOL', 'TIME', 'TYPE',

            'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'POW', 'MOD', 'FLOORDIV',
            
            'VARASSIGN', 'ARROW', 'PARAMASSIGN', 'LF', 'RF', 'END',

            'FOREACH', 'REPEAT', 'WHILE', 'IF', 'ELSE',
            
            'NOT', 'AND', 'OR', 'XOR',
            
            'GREATER', 'EGREATER', 'LESS', 'ELESS', 'XPLUS', 'XMINUS', 'EQUALS', 'NOTEQUALS', 
    }
    
    literals = { '(', ')', '{', '}', '[', ']', ','}

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
    VARASSIGN = r'='
    PARAMASSIGN= r':'
    ARROW = r'->'
    END= r';'

    #ELEMENTS VARS UPDATES
    XPLUS= r'\+\+'
    XMINUS= r'--'

    #ARIHTMETIC
    PLUS = r'\+'
    MINUS = r'-'
    POW = r'\*\*'
    MULTIPLY = r'\*'
    MOD= r'\%'
    FLOORDIV = r'//'
    DIVIDE = r'/'
    

    #VARIABLES
    TIME = r'\d+[dmy]'
    
    NAME= r'[_]*[a-zA-Z][a-zA-Z0-9_]*'

    NUMBER = r'\d+(\.\d+)?'

    STRING = r'\'.*?\''
    def STRING(self, t):
        t.value = str(t.value).strip('\'')
        return t

    

    #BOOLEANS
    NAME['true'] = 'BOOL'
    NAME['false'] = 'BOOL'

    #ELEMENTS
    NAME['nation'] = 'ELEMENT'
    NAME['sea'] = 'ELEMENT'
    NAME['trait'] = 'ELEMENT'
    NAME['category'] = 'ELEMENT'
    NAME['distribution'] = 'ELEMENT'
    
    NAME['event'] = 'EVENT'
    NAME['decision'] = 'DECISION'
    NAME['simulation'] = 'SIMULATION'
    NAME['function'] = 'FUNCTION'

    NAME['return'] = 'RETURN'
    NAME['enable'] = 'ENABLE'
    NAME['disable'] = 'DISABLE'

    #SPECIAL FUNCTIONS
    NAME['show'] = 'FUNC'
    NAME['len'] = 'FUNC'
    NAME['type'] = 'FUNC'
    NAME['pos'] = 'FUNC'

    NAME['rvs'] = 'FUNC'
    NAME['irvs'] = 'FUNC'

    #check
    NAME['gen_dist'] = 'FUNC'
    NAME['simulate'] = 'FUNC'

    NAME['neighbors'] = 'FUNC'

    NAME['plot'] = 'FUNC'
    NAME['dataframe'] = 'FUNC'
    NAME['info'] = 'FUNC'
    # NAME[''] = 'FUNC'

    #LOOPS
    NAME['foreach'] = 'FOREACH'
    NAME['repeat'] = 'REPEAT'
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
        raise Exception("Illegal character '%s'" % t.value[0])

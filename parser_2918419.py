import sys
import re

########################################
# TOKEN CLASS
########################################

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

########################################
# LEXER
########################################

class Lexer:
    def __init__(self, text):
        self.tokens = []
        self.tokenize(text)

    def tokenize(self, text):
        keywords = {'let','in','end','int','real','if','then','else'}

        token_spec = [
            ('NUMBER', r'\d+(\.\d+)?'),
            ('ID', r'[A-Za-z_][A-Za-z0-9_]*'),
            ('LE', r'<='),
            ('GE', r'>='),
            ('EQ', r'=='),
            ('NE', r'<>'),
            ('LT', r'<'),
            ('GT', r'>'),
            ('PLUS', r'\+'),
            ('MINUS', r'-'),
            ('MULT', r'\*'),
            ('DIV', r'/'),
            ('ASSIGN', r'='),
            ('COLON', r':'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('SEMI', r';'),
            ('SKIP', r'[ \t\n]+'),
            ('MISMATCH', r'.')
        ]

        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_spec)

        for mo in re.finditer(tok_regex, text):
            kind = mo.lastgroup
            value = mo.group()

            if kind == 'NUMBER':
                self.tokens.append(Token('NUMBER', value))

            elif kind == 'ID':
                if value in keywords:
                    self.tokens.append(Token(value.upper(), value))
                else:
                    self.tokens.append(Token('ID', value))

            elif kind in ('LE','GE','EQ','NE','LT','GT',
                          'PLUS','MINUS','MULT','DIV',
                          'ASSIGN','COLON','LPAREN',
                          'RPAREN','SEMI'):
                self.tokens.append(Token(kind, value))

            elif kind == 'SKIP':
                continue
            else:
                raise Exception("Error")

        self.tokens.append(Token('EOF', None))

########################################
# PARSER
########################################

class Parser:
    def __init__(self, lexer):
        self.tokens = lexer.tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]
        self.symbols = {}

    def error(self):
        raise Exception("Error")

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.pos += 1
            self.current_token = self.tokens[self.pos]
        else:
            self.error()

    ########################################
    # <let-in-end>
    ########################################
    def let_in_end(self):
        self.eat('LET')
        self.symbols = {}

        self.decl_list()

        self.eat('IN')

        final_type = self.type_rule()

        self.eat('LPAREN')
        value = self.expr()
        self.eat('RPAREN')

        self.eat('END')
        self.eat('SEMI')

        if final_type == 'int':
            return int(value)
        else:
            return float(value)

    ########################################
    def decl_list(self):
        while self.current_token.type == 'ID':
            self.decl()

    ########################################
    def decl(self):
        var_name = self.current_token.value
        self.eat('ID')
        self.eat('COLON')

        var_type = self.type_rule()

        self.eat('ASSIGN')
        value = self.expr()
        self.eat('SEMI')

        if var_type == 'int':
            value = int(value)
        else:
            value = float(value)

        self.symbols[var_name] = (var_type, value)

    ########################################
    def type_rule(self):
        if self.current_token.type == 'INT':
            self.eat('INT')
            return 'int'
        elif self.current_token.type == 'REAL':
            self.eat('REAL')
            return 'real'
        else:
            self.error()

    ########################################
    def expr(self):
        if self.current_token.type == 'IF':
            return self.if_expr()

        result = self.term()

        while self.current_token.type in ('PLUS','MINUS'):
            if self.current_token.type == 'PLUS':
                self.eat('PLUS')
                result += self.term()
            else:
                self.eat('MINUS')
                result -= self.term()

        return result

    ########################################
    def term(self):
        result = self.factor()

        while self.current_token.type in ('MULT','DIV'):
            if self.current_token.type == 'MULT':
                self.eat('MULT')
                result *= self.factor()
            else:
                self.eat('DIV')
                result /= self.factor()

        return result

    ########################################
    def factor(self):
        token = self.current_token

        if token.type == 'NUMBER':
            self.eat('NUMBER')
            return float(token.value) if '.' in token.value else int(token.value)

        elif token.type == 'ID':
            var_name = token.value
            if var_name not in self.symbols:
                self.error()
            value = self.symbols[var_name][1]
            self.eat('ID')
            return value

        elif token.type in ('INT','REAL'):
            return self.cast_expr()

        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            value = self.expr()
            self.eat('RPAREN')
            return value

        else:
            self.error()

    ########################################
    def cast_expr(self):
        cast_type = self.current_token.type
        self.eat(cast_type)
        self.eat('LPAREN')

        var_name = self.current_token.value
        if var_name not in self.symbols:
            self.error()

        value = self.symbols[var_name][1]
        self.eat('ID')
        self.eat('RPAREN')

        return int(value) if cast_type == 'INT' else float(value)

    ########################################
    def if_expr(self):
        self.eat('IF')
        condition = self.cond()
        self.eat('THEN')
        true_expr = self.expr()
        self.eat('ELSE')
        false_expr = self.expr()
        return true_expr if condition else false_expr

    ########################################
    def cond(self):
        left = self.expr()
        token_type = self.current_token.type
        self.eat(token_type)
        right = self.expr()

        if token_type == 'LT': return left < right
        if token_type == 'LE': return left <= right
        if token_type == 'GT': return left > right
        if token_type == 'GE': return left >= right
        if token_type == 'EQ': return left == right
        if token_type == 'NE': return left != right

        self.error()

########################################
# MAIN (PDF-Correct Behavior)

if __name__ == "__main__":

    filename = sys.argv[1]

    with open(filename, 'r') as file:
        text = file.read()

    lexer = Lexer(text)
    parser = Parser(lexer)

    while parser.current_token.type != 'EOF':
        try:
            result = parser.let_in_end()
            print(result)
        except:
            print("Error")

            # Skip until next LET or EOF
            while parser.current_token.type not in ('LET','EOF'):
                parser.pos += 1
                parser.current_token = parser.tokens[parser.pos]